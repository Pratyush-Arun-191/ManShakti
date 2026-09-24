import joblib


MODEL_PATH = "ml/wellbeing_model.pkl"

FEATURE_ORDER = [
    "anxiety_level",
    "self_esteem",
    "living_conditions",
    "basic_needs",
    "academic_performance",
    "study_load",
    "teacher_student_relationship",
    "future_career_concerns",
    "social_support",
    "peer_pressure",
    "extracurricular_activities",
    "bullying"
]


model = joblib.load(MODEL_PATH)


def predict_wellbeing(features):
    values = [[features[feature] for feature in FEATURE_ORDER]]

    prediction = model.predict(values)[0]

    return int(prediction)