from save_prediction import save_prediction
from check_student_history import check_student_history


# Add two more concerning days
save_prediction("AI001", 1)
save_prediction("AI001", 1)


result = check_student_history("AI001")

print("3-day history analysis:")
print(result)