import os
from dotenv import load_dotenv
from google import genai

from feature_extraction_prompt import FEATURE_EXTRACTION_PROMPT

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

reflection = """
I had a very stressful day. I have several assignments due this week
and I'm worried about my upcoming exams. I couldn't concentrate properly.
I feel supported by my friends, but I'm worried about my future career.
"""

prompt = FEATURE_EXTRACTION_PROMPT.format(
    reflection=reflection
)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

print("Gemini response:")
print(response.text)