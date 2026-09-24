import json
from ml.feature_extraction_prompt import FEATURE_EXTRACTION_PROMPT
from ml.process_features import process_features
from ml.predict_wellbeing import predict_wellbeing
from ml.save_prediction import save_prediction
from ml.check_student_history import check_student_history
import psycopg
import os
from dotenv import load_dotenv
from google import genai


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def run_wellbeing_analysis(student_roll_no, reflection):

    # 1. Send reflection to Gemini
    prompt = FEATURE_EXTRACTION_PROMPT.format(
        reflection=reflection
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    # 2. Convert Gemini JSON response into Python dictionary
    extracted_features = json.loads(response.text)

    # Extract human-readable analysis
    summary = extracted_features["summary"]
    indicator = extracted_features["indicator"]

    # 3. Fill missing features using dataset medians
    final_features = process_features(extracted_features)

    # 4. Predict stress level
    stress_level = predict_wellbeing(final_features)

    # 5. Save today's prediction
    save_result = save_prediction(
        student_roll_no,
        stress_level
    )

    # Stop if the student already submitted today
    if not save_result["saved"]:
        return {
            "student_roll_no": student_roll_no,
            "message": save_result["message"],
            "already_submitted": True
        }

    # Check recent history
    history_result = check_student_history(
        student_roll_no
    )

    # Save the current analysis
    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO wellbeing_analysis
                (student_roll_no, summary, indicator)
                VALUES (%s, %s, %s)
                ON CONFLICT (student_roll_no)
                DO UPDATE SET
                    summary = EXCLUDED.summary,
                    indicator = EXCLUDED.indicator,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    student_roll_no,
                    summary,
                    indicator
                )
            )

    return {
        "student_roll_no": student_roll_no,
        "stress_level": stress_level,
        "summary": summary,
        "indicator": indicator,
        "history_analysis": history_result
    }   