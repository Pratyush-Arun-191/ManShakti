from history_analysis import analyze_history


test_cases = [
    [2],
    [1, 1],
    [1, 1, 1],
    [0, 2, 1, 1],
    [0, 0, 1, 2],
]


for predictions in test_cases:
    result = analyze_history(predictions)

    print(
        f"Predictions: {predictions} "
        f"→ Concerning days: {result['concerning_days']} "
        f"→ Alert: {result['alert']}"
    )