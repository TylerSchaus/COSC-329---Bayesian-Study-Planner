import json 
import datetime

DIFFICULTY_STATES = ["easy", "hard"]
LEVEL_STATES = ["low", "high"] 
DAYS_STATES = ["few", "some", "many"] 

QUIZ_CUTOFF = 70 
DAYS_FEW_MAX = 3 
DAYS_SOME_MAX = 10 

DAYS_AWAY_MAX = 75

def convert_quiz_score(score): 
    if score < 0 or score > 100:
        raise ValueError("Quiz score out of range. Must be between 0 and 100.")
    if score >= QUIZ_CUTOFF: 
        return LEVEL_STATES[1]
    else: 
        return LEVEL_STATES[0]

def convert_days_remaining(days): 
    if days < 0 or days > DAYS_AWAY_MAX:
        raise ValueError(f"Days out of range. Must be between 0 and {DAYS_AWAY_MAX}.")
    if days <= DAYS_FEW_MAX: 
        return DAYS_STATES[0]
    elif days <= DAYS_SOME_MAX: 
        return DAYS_STATES[1]
    else: 
        return DAYS_STATES[2]

def load_scenario(file_path): 
    with open(file_path, "r") as f: 
        scenario = json.load(f) 

    days_remaining = convert_days_remaining((datetime.date.fromisoformat(scenario["exam_date"]) - datetime.date.fromisoformat(scenario["start_date"])).days)

    quiz_score_c1 = convert_quiz_score(scenario["concepts"][0]["quiz_score"]) 
    quiz_score_c2 = convert_quiz_score(scenario["concepts"][1]["quiz_score"]) 
    quiz_score_c3 = convert_quiz_score(scenario["concepts"][2]["quiz_score"]) 

    difficulty_c1 = scenario["concepts"][0]["difficulty"]
    if difficulty_c1 not in DIFFICULTY_STATES:
        raise ValueError(f"Invalid difficulty state for concept 1: {difficulty_c1}")
    difficulty_c2 = scenario["concepts"][1]["difficulty"]
    if difficulty_c2 not in DIFFICULTY_STATES:
        raise ValueError(f"Invalid difficulty state for concept 2: {difficulty_c2}")
    difficulty_c3 = scenario["concepts"][2]["difficulty"]
    if difficulty_c3 not in DIFFICULTY_STATES:
        raise ValueError(f"Invalid difficulty state for concept 3: {difficulty_c3}")

    return {
        "DaysRemaining": days_remaining,
        "QuizScore_C1": quiz_score_c1,
        "QuizScore_C2": quiz_score_c2,
        "QuizScore_C3": quiz_score_c3,
        "Difficulty_C1": difficulty_c1,
        "Difficulty_C2": difficulty_c2,
        "Difficulty_C3": difficulty_c3
    }
