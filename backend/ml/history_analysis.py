def analyze_history(predictions):
    """
    predictions:
        List of recent stress-level predictions.
        Example: [0, 1, 1, 1]

    Returns:
        Dictionary containing the recent pattern and alert decision.
    """

    if not predictions:
        return {
            "alert": False,
            "reason": "No prediction history available"
        }

    # Look at the most recent 4 days
    recent_predictions = predictions[-4:]

    # Count concerning days
    concerning_days = sum(
        prediction >= 1
        for prediction in recent_predictions
    )

    # Require at least 3 concerning days
    alert = concerning_days >= 3

    return {
        "recent_predictions": recent_predictions,
        "concerning_days": concerning_days,
        "alert": alert
    }