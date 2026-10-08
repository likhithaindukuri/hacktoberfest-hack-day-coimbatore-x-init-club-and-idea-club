import laya

agent = laya.load("convaiinnovations/laya")

state = "Wet patch on floor near aisle 3. No warning sign visible. Worker slipped."

questions = {
    "cause": {
        "type": "choice",
        "instructions": "What is the most likely cause of this incident?",
        "criteria": {
            "spill": "unmarked liquid spill or wet floor",
            "obstruction": "object blocking a walkway",
            "lighting": "poor lighting or visibility",
            "equipment": "equipment failure",
            "human_error": "worker error or rushing",
            "insufficient": "not enough evidence to tell",
        },
    }
}

result = agent.predict(state, questions)
print(result)