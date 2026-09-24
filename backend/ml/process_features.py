FEATURE_MEDIANS = {
    "anxiety_level": 11,
    "self_esteem": 19,
    "living_conditions": 2,
    "basic_needs": 3,
    "academic_performance": 2,
    "study_load": 2,
    "teacher_student_relationship": 2,
    "future_career_concerns": 2,
    "social_support": 2,
    "peer_pressure": 2,
    "extracurricular_activities": 2.5,
    "bullying": 3
}


def process_features(extracted_features):
    final_features = {}

    for feature, median in FEATURE_MEDIANS.items():
        value = extracted_features[feature]["value"]
        mentioned = extracted_features[feature]["mentioned"]

        if mentioned and value is not None:
            final_features[feature] = value
        else:
            final_features[feature] = median

    return final_features