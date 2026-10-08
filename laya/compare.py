import warnings
import laya

warnings.filterwarnings("ignore", message="laya: this checkpoint ships invalid")

QUESTIONS = {
    "cause": {
        "type": "choice",
        "instructions": "What is the most likely cause of this incident?",
        "criteria": {
            "spill": "unmarked liquid spill or wet floor",
            "obstruction": "object blocking a walkway",
            "lighting": "poor lighting or visibility",
            "equipment": "equipment failure",
            "electrical": "electrical fault or exposed wiring",
            "storage": "improper or unstable storage of items",
            "human_error": "worker error or rushing",
            "insufficient": "not enough evidence to tell",
        },
    }
}

cases = [
    ("Wet patch on floor near aisle 3. No warning sign visible.", "spill"),
    ("Cardboard boxes stacked across the aisle. Worker tripped.", "obstruction"),
    ("Corridor very dark. Bulb missing in ceiling fixture.", "lighting"),
    ("Forklift brake failed during unloading.", "equipment"),
    ("Exposed wires near the socket. Sparks seen.", "electrical"),
    ("Tall shelf tilted and boxes fell. Items stacked unevenly.", "storage"),
    ("Worker was running to finish the shift and skipped the check.", "human_error"),
    ("The sky is blue today.", "insufficient"),
]

for name, kwargs in [("typed-decisions", {"subfolder": "typed-decisions"}), ("base", {})]:
    agent = laya.load("convaiinnovations/laya", **kwargs)
    correct = 0
    print(f"\n=== {name} ===")
    for text, expected in cases:
        a = agent.predict(text, QUESTIONS)["answers"]["cause"]
        ok = a["choice"] == expected
        correct += ok
        print(f"{'OK ' if ok else 'BAD'} expected={expected:12} got={a['choice']:12} p={a['probabilities'][a['choice']]:.2f}")
    print(f"accuracy: {correct}/{len(cases)}")