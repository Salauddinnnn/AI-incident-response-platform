from openai import OpenAI
from config import OPENROUTER_API_KEY


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

MODEL_NAME = "deepseek/deepseek-chat-v3.1"


def _ask_ai(prompt: str) -> str:
    """
    Send a prompt to the AI model and return the response.
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as error:
        return f"AI analysis unavailable: {error}"


def analyze_incident_with_ai(incident_data):
    """
    Analyze website incidents using AI.
    """

    prompt = f"""
You are a Senior DevOps Site Reliability Engineer.

Analyze this production incident.

URL: {incident_data.get("url")}
Status: {incident_data.get("status")}
Severity: {incident_data.get("severity")}
Status Code: {incident_data.get("status_code")}
Response Time: {incident_data.get("response_time_seconds")}
Error: {incident_data.get("error")}

Provide:

1. Root Cause
2. Business Impact
3. Immediate Action
4. Long-Term Prevention

Keep the response short and practical.
"""

    return _ask_ai(prompt)


def analyze_generic_incident(title, details):
    """
    Analyze any infrastructure incident.
    """

    prompt = f"""
You are a Senior DevOps Site Reliability Engineer.

Analyze this production incident.

Incident:
{title}

Details:
{details}

Provide:

1. Root Cause
2. Business Impact
3. Immediate Action
4. Long-Term Prevention

Keep the response short and practical.
"""

    return _ask_ai(prompt)