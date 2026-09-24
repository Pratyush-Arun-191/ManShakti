import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def save_prediction(student_roll_no, stress_level):

    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:

            # Check whether a prediction already exists today
            cursor.execute(
                """
                SELECT id
                FROM wellbeing_predictions
                WHERE student_roll_no = %s
                  AND response_date = CURRENT_DATE
                """,
                (student_roll_no,)
            )

            existing_prediction = cursor.fetchone()

            if existing_prediction is not None:
                return {
                    "saved": False,
                    "message": "Prediction already exists for today"
                }

            # Save today's prediction
            cursor.execute(
                """
                INSERT INTO wellbeing_predictions
                (student_roll_no, stress_level, response_date)
                VALUES (%s, %s, CURRENT_DATE)
                """,
                (student_roll_no, stress_level)
            )

    return {
        "saved": True,
        "student_roll_no": student_roll_no,
        "stress_level": stress_level
    }