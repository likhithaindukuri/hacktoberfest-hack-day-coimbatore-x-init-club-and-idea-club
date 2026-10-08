import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def analyze_incident(image_path, context):

    my_file = client.files.upload(file=image_path)

    prompt = f"""
You are an incident evidence extraction system.

Analyze the uploaded incident image together with the provided context.

Identify only information that can be visually supported by the image.
Do not invent people, actions, causes, times, or events that cannot be observed.

Return ONLY valid JSON in exactly this structure:

{{
  "visible_objects": [
    "object 1",
    "object 2"
  ],
  "visible_conditions": [
    "condition 1",
    "condition 2"
  ],
  "evidence": [
    "evidence 1",
    "evidence 2"
  ],
  "uncertainties": [
    "uncertainty 1",
    "uncertainty 2"
  ]
}}

Incident context:
{context}
"""

    response = client.models.generate_content(
        model="gemma-4-26b-a4b-it",
        contents=[
            my_file,
            prompt
        ]
    )

    result = json.loads(
        response.text.replace("```json", "").replace("```", "").strip()
    )

    return result


if __name__ == "__main__":

    image_path = "gemma/test_images/incident.jpg"

    context = """
    This incident happened in an electronics laboratory.
    """

    evidence = analyze_incident(image_path, context)

    print("\nGemma 4 Incident Evidence\n")

    print("Visible Objects:")
    for item in evidence["visible_objects"]:
        print("-", item)

    print("\nVisible Conditions:")
    for item in evidence["visible_conditions"]:
        print("-", item)

    print("\nEvidence:")
    for item in evidence["evidence"]:
        print("-", item)

    print("\nUncertainties:")
    for item in evidence["uncertainties"]:
        print("-", item)