from get_prediction_history import get_prediction_history


history = get_prediction_history("AI001")

print("Prediction history:")

for record in history:
    print(record)