import os
import json
from dotenv import load_dotenv
from google import genai
from laya_decision import rank_incident_explanations

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
  "visible_objects": [],
  "visible_conditions": [],
  "evidence": [],
  "possible_explanations": [],
  "uncertainties": []
}}

The arrays are dynamic. Include all relevant observations supported by the image.
Do not limit the number of objects, conditions, evidence items,
possible explanations, or uncertainties to a fixed number.

Based on the visible evidence and incident context, suggest 2 to 4
meaningful plausible explanations for what may have happened.

The possible explanations are hypotheses, not confirmed facts.
Do not present any explanation as certain.
Only suggest explanations that are reasonably supported by the
visible evidence and provided context.

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

    image_path = "test_images/incident.jpg"

    context = """
    This incident happened in an electronics laboratory.
    """

    gemma_evidence = analyze_incident(image_path, context)

    print("\nGemma 4 Incident Evidence\n")

    print("Visible Objects:")
    for item in gemma_evidence["visible_objects"]:
        print("-", item)

    print("\nVisible Conditions:")
    for item in gemma_evidence["visible_conditions"]:
        print("-", item)

    print("\nEvidence:")
    for item in gemma_evidence["evidence"]:
        print("-", item)

    print("\nPossible Explanations:")
    for index, item in enumerate(
        gemma_evidence["possible_explanations"],
        start=1
    ):
        print(f"{index}. {item}")

    print("\nUncertainties:")
    for item in gemma_evidence["uncertainties"]:
        print("-", item)

    laya_result = rank_incident_explanations(
        gemma_result=gemma_evidence,
        context=context
    )

    print("\n" + "=" * 55)
    print("Laya Decision and Confidence")
    print("=" * 55)

    print("\nMost likely explanation:")
    print("-", laya_result["selected_explanation"])

    print("\nLaya choice confidence:")
    print("-", laya_result["choice_confidence"])

    print("\nAll explanation probabilities:")

    for key, probability in laya_result["all_probabilities"].items():
        print(f"- {key}: {probability:.2%}")

    print("\nEvidence support score:")
    print("-", laya_result["support_score"])

    print("\nHuman review decision:")
    print("-", laya_result["human_review"])