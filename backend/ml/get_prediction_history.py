import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_prediction_history(student_roll_no):
    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT stress_level, created_at
                FROM wellbeing_predictions
                WHERE student_roll_no = %s
                ORDER BY created_at ASC
                """,
                (student_roll_no,)
            )

            rows = cursor.fetchall()

    return [
        {
            "stress_level": row[0],
            "created_at": row[1]
        }
        for row in rows
    ]