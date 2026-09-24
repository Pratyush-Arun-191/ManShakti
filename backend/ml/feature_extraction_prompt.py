FEATURE_EXTRACTION_PROMPT = """
You are a student wellbeing feature extraction system.

Read the student's reflection and extract information that is supported
by the text.

Return ONLY valid JSON.

The JSON must contain exactly these 14 fields:

{{
    "anxiety_level": {{
        "value": null,
        "mentioned": false
    }},
    "self_esteem": {{
        "value": null,
        "mentioned": false
    }},
    "living_conditions": {{
        "value": null,
        "mentioned": false
    }},
    "basic_needs": {{
        "value": null,
        "mentioned": false
    }},
    "academic_performance": {{
        "value": null,
        "mentioned": false
    }},
    "study_load": {{
        "value": null,
        "mentioned": false
    }},
    "teacher_student_relationship": {{
        "value": null,
        "mentioned": false
    }},
    "future_career_concerns": {{
        "value": null,
        "mentioned": false
    }},
    "social_support": {{
        "value": null,
        "mentioned": false
    }},
    "peer_pressure": {{
        "value": null,
        "mentioned": false
    }},
    "extracurricular_activities": {{
        "value": null,
        "mentioned": false
    }},
    "bullying": {{
        "value": null,
        "mentioned": false
    }},
    "summary": "",
    "indicator": ""
}}

Allowed ranges:

- anxiety_level: 0-21
- self_esteem: 0-30
- living_conditions: 0-5
- basic_needs: 0-5
- academic_performance: 0-5
- study_load: 0-5
- teacher_student_relationship: 0-5
- future_career_concerns: 0-5
- social_support: 0-3
- peer_pressure: 0-5
- extracurricular_activities: 0-5
- bullying: 0-5

Rules:

1. "mentioned" must be true only when the reflection provides evidence
   about that feature.

2. If the feature is not mentioned or there is insufficient evidence,
   set "value" to null and "mentioned" to false.

3. If the feature is mentioned, provide an integer value within its
   allowed range.

4. Do not invent information that is not supported by the reflection.

5. Do not diagnose any mental-health condition.

6. These values are feature estimates for an ML model, not medical measurements.

7. "summary" must be a short factual summary of what the student
   expressed in the reflection.

8. "indicator" must identify the main observable concern, if any,
   such as "academic pressure", "future career concern",
   "social pressure", or "no clear concern".

9. Do not use medical diagnoses in "summary" or "indicator".

10. Keep "summary" and "indicator" concise.

11. Return JSON only. Do not include explanations.

Student reflection:
{reflection}
"""

if __name__ == "__main__":
    reflection = """
    I had a very stressful day. I have several assignments due this week
    and I'm worried about my upcoming exams. I couldn't concentrate properly.
    I feel supported by my friends, but I'm worried about my future career.
    """

    prompt = FEATURE_EXTRACTION_PROMPT.format(
        reflection=reflection
    )

    print(prompt)