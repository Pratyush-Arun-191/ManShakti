import joblib
import pandas as pd

# Load the saved model
model = joblib.load("ml/wellbeing_model.pkl")

# One sample student
sample = pd.DataFrame([{
    "anxiety_level": 15,
    "self_esteem": 10,
    "living_conditions": 2,
    "basic_needs": 2,
    "academic_performance": 2,
    "study_load": 4,
    "teacher_student_relationship": 2,
    "future_career_concerns": 4,
    "social_support": 1,
    "peer_pressure": 4,
    "extracurricular_activities": 2,
    "bullying": 3
}])

# Make prediction
prediction = model.predict(sample)

print("Predicted stress level:", prediction[0])