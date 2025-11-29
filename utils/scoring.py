# scoring.py
from openai import OpenAI
import json

def score_resume(resume_text, jd_text, api_key):

    # Create client only AFTER the API key is available
    client = OpenAI(api_key=api_key)

    prompt = f"""
You are an expert HR evaluator. Compare the resume and job description.

Return a JSON object EXACTLY in this format:

{{
  "score": <1-100>,
  "explanation": "<short explanation>"
}}

Evaluation rules:
- Base score on skill match, experience relevance, and strengths.
- Explanation must be 2–5 sentences.

Resume:
{resume_text}

Job Description:
{jd_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    raw = response.choices[0].message.content

    # Safe JSON load
    try:
        result = json.loads(raw)
    except:
        cleaned = raw.strip().split("```")[-1]
        result = json.loads(cleaned)

    return result
