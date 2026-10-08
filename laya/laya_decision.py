import json
import laya


laya_agent = laya.load(
    "convaiinnovations/laya",
    subfolder="typed-decisions"
)


def build_laya_state(gemma_result, context):
    """
    Converts Gemma's evidence JSON into a compact state that Laya can score.
    """

    state = {
        "incident_context": context,
        "visible_objects": gemma_result.get("visible_objects", []),
        "visible_conditions": gemma_result.get("visible_conditions", []),
        "evidence": gemma_result.get("evidence", []),
        "uncertainties": gemma_result.get("uncertainties", []),
        "possible_explanations": gemma_result.get(
            "possible_explanations", []
        )
    }

    return json.dumps(state, ensure_ascii=False, indent=2)


def build_explanation_criteria(explanations):
    """
    Laya choice questions need named options.
    Each key is a stable label and each value is the explanation.
    """

    criteria = {}

    for index, explanation in enumerate(explanations, start=1):
        criteria[f"explanation_{index}"] = explanation

    criteria["insufficient_evidence"] = (
        "The available extracted evidence is too limited, ambiguous, "
        "or contradictory to select one explanation reliably."
    )

    return criteria


def rank_incident_explanations(gemma_result, context):
    """
    Uses text-only Laya to rank Gemma's possible incident explanations.
    """

    explanations = gemma_result.get("possible_explanations", [])

    if len(explanations) < 2:
        raise ValueError(
            "Gemma must return at least two possible_explanations "
            "before Laya can rank them."
        )

    state = build_laya_state(gemma_result, context)
    criteria = build_explanation_criteria(explanations)

    questions = {
        "most_likely_explanation": {
            "type": "choice",
            "instructions": (
                "Using only the incident context, visible objects, visible "
                "conditions, evidence, and uncertainties in the state, choose "
                "the explanation that is best supported. Do not assume facts "
                "that are absent from the extracted evidence. Choose "
                "'insufficient_evidence' if no explanation is adequately "
                "supported."
            ),
            "criteria": criteria
        },
        "decision_confidence": {
            "type": "score",
            "instructions": (
                "How strongly does the extracted evidence support the selected "
                "explanation?"
            ),
            "criteria": [
                "very weak support",
                "weak support",
                "moderate support",
                "strong support",
                "very strong support"
            ]
        },
        "needs_human_review": {
            "type": "choice",
            "instructions": (
                "Should a human review this incident before any alert or "
                "conclusion is acted upon?"
            ),
            "criteria": {
                "review_required": (
                    "Evidence is uncertain, incomplete, ambiguous, "
                    "or concerns a potentially safety-critical incident."
                ),
                "review_not_required": (
                    "The extracted evidence is clear enough for low-risk "
                    "informational classification only."
                )
            }
        }
    }

    result = laya_agent.predict(state, questions)

    answer = result["answers"]["most_likely_explanation"]
    selected_key = answer["choice"]
    return {
    "selected_key": selected_key,
    "selected_explanation": criteria.get(
        selected_key,
        "No explanation could be selected safely."
    ),
    "choice_confidence": answer.get("confidence"),
    "all_probabilities": answer.get("probabilities", {}),
    "support_score": result["answers"]["decision_confidence"].get(
        "score"
    ),
    "support_confidence": result["answers"]["decision_confidence"].get(
        "confidence"
    ),
    "human_review": result["answers"]["needs_human_review"]["choice"],
    "human_review_confidence": result["answers"][
        "needs_human_review"
    ].get("confidence"),
    "raw_laya_result": result
}