import json
from google import genai
from psycopg.errors import UniqueViolation
from ml.run_wellbeing_analysis import run_wellbeing_analysis
import os
from dotenv import load_dotenv
import psycopg
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel   

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

DATABASE_URL = os.getenv("DATABASE_URL")

with psycopg.connect(DATABASE_URL) as connection:
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                roll_no VARCHAR(30) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS wellbeing_responses (
                id SERIAL PRIMARY KEY,
                student_roll_no VARCHAR(30) REFERENCES students(roll_no),
                reflection_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS wellbeing_analysis (
                student_roll_no VARCHAR(30) PRIMARY KEY
                    REFERENCES students(roll_no),
                category VARCHAR(50),
                summary TEXT,
                indicator TEXT,
                confidence VARCHAR(20),
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS wellbeing_predictions (
                id SERIAL PRIMARY KEY,
                student_roll_no VARCHAR(30)
                    REFERENCES students(roll_no),
                stress_level INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

print("Database tables ready!")

app = FastAPI(title="ManShakti API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Student(BaseModel):
    roll_no: str
    name: str
    email: str


@app.post("/student")
def create_student(student: Student):

    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO students (roll_no, name, email)
                VALUES (%s, %s, %s)
                """,
                (student.roll_no, student.name, student.email)
            )

    return {
        "message": "Student created successfully",
        "roll_no": student.roll_no
    }

class Reflection(BaseModel):
    student_roll_no: str
    text: str

class AcademicAnswer(BaseModel):
    student_roll_no: str
    question: str
    answer: str


@app.post("/reflection")
def submit_reflection(reflection: Reflection):

    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT roll_no
                FROM students
                WHERE roll_no = %s
                """,
                (reflection.student_roll_no,)
            )

            student = cursor.fetchone()

            if student is None:
                return {
                    "message": "Student not found",
                    "student_roll_no": reflection.student_roll_no
                }


            cursor.execute(
                """
                SELECT id
                FROM wellbeing_responses
                WHERE student_roll_no = %s
                AND created_at::date = CURRENT_DATE
                """,
                (reflection.student_roll_no,)
            )

            existing_response = cursor.fetchone()

            if existing_response is not None:
                return {
                    "message": "You have already submitted today's reflection.",
                    "student_roll_no": reflection.student_roll_no,
                    "already_submitted": True
                }

            # Save the raw reflection
            cursor.execute(
                """
                INSERT INTO wellbeing_responses
                (student_roll_no, reflection_text)
                VALUES (%s, %s)
                """,
                (
                    reflection.student_roll_no,
                    reflection.text
                )
            )

    # Run the AI + ML pipeline
    analysis = run_wellbeing_analysis(
        reflection.student_roll_no,
        reflection.text
    )

    if analysis.get("already_submitted"):
        return {
            "message": analysis["message"],
            "student_roll_no": reflection.student_roll_no,
            "already_submitted": True
        }

    return {
        "message": "Reflection analyzed successfully",
        "student_roll_no": reflection.student_roll_no,
        "stress_level": analysis["stress_level"],
        "summary": analysis["summary"],
        "indicator": analysis["indicator"],
        "history_analysis": analysis["history_analysis"]
    }

@app.get("/student/{roll_no}/reflections")
def get_reflections(roll_no: str):

    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT reflection_text, created_at
                FROM wellbeing_responses
                WHERE student_roll_no = %s
                ORDER BY created_at ASC
                """,
                (roll_no,)
            )

            reflections = cursor.fetchall()

    return {
        "student_roll_no": roll_no,
        "reflections": [
            {
                "text": row[0],
                "created_at": row[1]
            }
            for row in reflections
        ]
    }


@app.get("/student/{roll_no}/analysis")
def get_analysis(roll_no: str):

    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT category, summary, indicator, confidence, updated_at
                FROM wellbeing_analysis
                WHERE student_roll_no = %s
                """,
                (roll_no,)
            )

            analysis = cursor.fetchone()

    if analysis is None:
        return {
            "message": "No wellbeing analysis available yet"
        }

    return {
        "student_roll_no": roll_no,
        "category": analysis[0],
        "summary": analysis[1],
        "indicator": analysis[2],
        "confidence": analysis[3],
        "updated_at": analysis[4]
    }


class WellbeingAnalysis(BaseModel):
    student_roll_no: str
    category: str
    summary: str
    indicator: str
    confidence: str


@app.post("/student/{roll_no}/analysis")
def update_analysis(roll_no: str, analysis: WellbeingAnalysis):

    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:

            # Check whether student exists
            cursor.execute(
                """
                SELECT roll_no
                FROM students
                WHERE roll_no = %s
                """,
                (roll_no,)
            )

            student = cursor.fetchone()

            if student is None:
                return {
                    "message": "Student not found",
                    "student_roll_no": roll_no
                }

            # Insert or update analysis
            cursor.execute(
                """
                INSERT INTO wellbeing_analysis
                (student_roll_no, category, summary, indicator, confidence)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (student_roll_no)
                DO UPDATE SET
                    category = EXCLUDED.category,
                    summary = EXCLUDED.summary,
                    indicator = EXCLUDED.indicator,
                    confidence = EXCLUDED.confidence,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    roll_no,
                    analysis.category,
                    analysis.summary,
                    analysis.indicator,
                    analysis.confidence
                )
            )

    return {
        "message": "Wellbeing analysis updated successfully",
        "student_roll_no": roll_no
    }


@app.get("/student/{roll_no}")
def get_student(roll_no: str):

    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT roll_no, name, email
                FROM students
                WHERE roll_no = %s
                """,
                (roll_no,)
            )

            student = cursor.fetchone()

    if student is None:
        return {
            "message": "Student not found",
            "student_roll_no": roll_no
        }

    return {
        "roll_no": student[0],
        "name": student[1],
        "email": student[2]
    }


@app.post("/academic/evaluate")
def evaluate_academic_answer(data: AcademicAnswer):

    prompt = f"""
You are an academic understanding evaluation system.

Evaluate the student's answer to the question below.

Question:
{data.question}

Student answer:
{data.answer}

Return ONLY valid JSON with exactly these fields:

{{
    "understanding": "",
    "missing_concept": "",
    "feedback": "",
    "resource_query": ""
}}

Rules:

1. "understanding" must be exactly one of:
   - "Strong"
   - "Partial"
   - "Weak"

2. "missing_concept" should identify the specific concept the student
   appears to misunderstand or has not explained adequately.

3. If the answer is correct and complete, use:
   "No major concept gap identified"

4. "feedback" should briefly explain what the student understood
   and what they should improve.

5. "resource_query" should be a concise search query that the student
   can use to learn the missing concept.

6. Do not invent mistakes that are not present in the answer.

7. Do not give a numerical score.

8. Return JSON only.

"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    result = json.loads(response.text)

    return {
        "student_roll_no": data.student_roll_no,
        "question": data.question,
        "understanding": result["understanding"],
        "missing_concept": result["missing_concept"],
        "feedback": result["feedback"],
        "resource_query": result["resource_query"]
    }