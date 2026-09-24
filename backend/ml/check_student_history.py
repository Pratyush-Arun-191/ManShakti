from ml.get_prediction_history import get_prediction_history
from ml.history_analysis import analyze_history


def check_student_history(student_roll_no):
    history = get_prediction_history(student_roll_no)

    predictions = [
        record["stress_level"]
        for record in history
    ]

    result = analyze_history(predictions)

    return result