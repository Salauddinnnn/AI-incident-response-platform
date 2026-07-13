import os
from google import genai
from config import GEMINI_API_KEY
client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3.5-flash"


def _ask_ai(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        return response.text

    except Exception as e:
        return f"AI analysis unavailable: {e}"


def analyze_incident_with_ai(incident_data):
    prompt = f"""
You are a Senior DevOps Site Reliability Engineer.

Analyze this production incident.

URL: {incident_data.get("url")}
Status: {incident_data.get("status")}
Severity: {incident_data.get("severity")}
Status Code: {incident_data.get("status_code")}
Response Time: {incident_data.get("response_time_seconds")}
Error: {incident_data.get("error")}

Provide exactly these 4 lines:

Root Cause: one short professional sentence.
Business Impact: one short professional sentence.
Immediate Action: one short professional sentence.
Prevention: one short professional sentence.

Do not use markdown, headings, bullets, numbering, assumptions, or extra explanation.
Each line must contain no more than 18 words.
"""

    return _ask_ai(prompt)


def analyze_generic_incident(title, details):
    prompt = f"""
You are a Senior DevOps Site Reliability Engineer.

Analyze this production incident.

Incident:
{title}

Details:
{details}

Provide exactly these 4 lines:

Root Cause: one short professional sentence.
Business Impact: one short professional sentence.
Immediate Action: one short professional sentence.
Prevention: one short professional sentence.

Do not use markdown, headings, bullets, numbering, assumptions, or extra explanation.
Each line must contain no more than 18 words.
"""

    return _ask_ai(prompt)