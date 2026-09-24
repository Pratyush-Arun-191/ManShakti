from run_wellbeing_analysis import run_wellbeing_analysis


reflection = """
I had a stressful day. I have several assignments due this week
and I am worried about my upcoming exams. I could not concentrate
properly. I feel supported by my friends, but I am worried about
my future career.
"""


result = run_wellbeing_analysis(
    "AI001",
    reflection
)

print("Wellbeing analysis:")
print(result)