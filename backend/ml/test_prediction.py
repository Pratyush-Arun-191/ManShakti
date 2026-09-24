from predict_wellbeing import predict_wellbeing


sample_features = {
    "anxiety_level": 15,
    "self_esteem": 19,
    "living_conditions": 2,
    "basic_needs": 3,
    "academic_performance": 2,
    "study_load": 4,
    "teacher_student_relationship": 2,
    "future_career_concerns": 4,
    "social_support": 2,
    "peer_pressure": 2,
    "extracurricular_activities": 2.5,
    "bullying": 3
}


prediction = predict_wellbeing(sample_features)

print("Predicted stress level:", prediction)