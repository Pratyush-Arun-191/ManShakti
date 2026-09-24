from process_features import process_features


sample_features = {
    "anxiety_level": {
        "value": 15,
        "mentioned": True
    },
    "self_esteem": {
        "value": None,
        "mentioned": False
    },
    "living_conditions": {
        "value": None,
        "mentioned": False
    },
    "basic_needs": {
        "value": None,
        "mentioned": False
    },
    "academic_performance": {
        "value": None,
        "mentioned": False
    },
    "study_load": {
        "value": 4,
        "mentioned": True
    },
    "teacher_student_relationship": {
        "value": None,
        "mentioned": False
    },
    "future_career_concerns": {
        "value": 4,
        "mentioned": True
    },
    "social_support": {
        "value": 2,
        "mentioned": True
    },
    "peer_pressure": {
        "value": None,
        "mentioned": False
    },
    "extracurricular_activities": {
        "value": None,
        "mentioned": False
    },
    "bullying": {
        "value": None,
        "mentioned": False
    }
}


final_features = process_features(sample_features)

print("Final features:")
print(final_features)