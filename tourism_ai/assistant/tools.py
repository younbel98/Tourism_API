import random

from .models import QuizAttempt, Badge, VisitedSite, BehaviorAlert
from .datasets import ECO_INSIGHTS, QUIZZES, RISK_ALERTS, BADGES


def tool_definitions():
    return [
        {
            "type": "function",
            "function": {
                "name": "get_site_info",
                "description": "Get ecological information and details about a tourist site.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "site_name": {
                            "type": "string",
                            "description": "Name of the site to look up (e.g., 'Djebel Tazaanount')",
                        }
                    },
                    "required": ["site_name"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_coordinates",
                "description": "Get the GPS coordinates, region, and city of a tourist site.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "site_name": {
                            "type": "string",
                            "description": "The site to get coordinates for.",
                        }
                    },
                    "required": ["site_name"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "run_quiz",
                "description": "Get 3 randomized quiz questions for a specific site type.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "site_type": {
                            "type": "string",
                            "description": "The type of site (e.g., 'Mountain', 'Forest')",
                        }
                    },
                    "required": ["site_type"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "submit_answer",
                "description": "Check if the given answer index is correct for the specified question.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "site_type": {"type": "string"},
                        "question_index": {"type": "integer"},
                        "answer_index": {"type": "integer"},
                    },
                    "required": ["site_type", "question_index", "answer_index"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "submit_score",
                "description": "Record a user’s quiz score for a site type.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "site_type": {"type": "string"},
                        "score": {"type": "integer"},
                    },
                    "required": ["site_type", "score"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "log_alert",
                "description": "Log a risky or harmful behavior observed at a tourist site.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "behavior": {
                            "type": "string",
                            "description": "The risky behavior observed (e.g., 'littering', 'off_path')",
                        },
                        "site_name": {
                            "type": "string",
                            "description": "Name of the site where it occurred",
                        },
                    },
                    "required": ["behavior", "site_name"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "check_badges",
                "description": "Check which environmental badges the user has earned.",
                "parameters": {"type": "object", "properties": {}},
            },
        },
    ]


import random
import difflib
from .datasets import ECO_INSIGHTS, QUIZZES, BADGES, RISK_ALERTS
from .models import QuizAttempt, Badge, BehaviorAlert, VisitedSite


def find_site_by_name(name):
    name = name.lower()
    for site in ECO_INSIGHTS:
        if site["name"].lower() == name:
            return site
        if "aliases" in site:
            for alias in site["aliases"].values():
                if alias.lower() == name:
                    return site
    # Fuzzy match fallback
    names = [site["name"] for site in ECO_INSIGHTS]
    matches = difflib.get_close_matches(name, names, n=1, cutoff=0.6)
    if matches:
        return next((s for s in ECO_INSIGHTS if s["name"] == matches[0]), None)
    return None


def execute_tool(user_id, name, args):
    if name == "get_site_info":
        site = find_site_by_name(args["site_name"])
        return site or {"error": "Site not found"}

    elif name == "get_coordinates":
        site = find_site_by_name(args["site_name"])
        if site:
            return site["location"]
        return {"error": "Coordinates not found"}

    elif name == "run_quiz":
        quiz_data = QUIZZES.get(args["site_type"].capitalize(), {})
        questions = quiz_data.get("questions", [])
        random.shuffle(questions)
        return questions[:3] if questions else {"error": "No quiz available"}

    elif name == "submit_answer":
        site_type = args["site_type"].capitalize()
        question_index = args["question_index"]
        answer_index = args["answer_index"]
        quiz = QUIZZES.get(site_type, {}).get("questions", [])
        if question_index < len(quiz):
            correct_index = quiz[question_index]["answer_index"]
            return {
                "correct": answer_index == correct_index,
                "correct_answer": correct_index,
            }
        return {"error": "Invalid question index"}

    elif name == "submit_score":
        score = args["score"]
        site_type = args["site_type"].capitalize()
        QuizAttempt.objects.create(user_id=user_id, site_type=site_type, score=score)
        return {"message": f"Score {score} for {site_type} recorded."}

    elif name == "log_alert":
        behavior = args["behavior"].lower()
        site_name = args.get("site_name", "Unknown")
        BehaviorAlert.objects.create(
            user_id=user_id, behavior=behavior, site_name=site_name
        )
        return {"response": RISK_ALERTS.get(behavior, RISK_ALERTS.get("general", {}))}

    elif name == "check_badges":
        visit_count = VisitedSite.objects.filter(user_id=user_id).count()
        quiz_scores = list(
            QuizAttempt.objects.filter(user_id=user_id).values_list("score", flat=True)
        )
        earned = []
        for badge_id, badge_data in BADGES.items():
            if badge_id == "eco_explorer" and visit_count >= 5:
                earned.append(badge_id)
            if badge_id == "green_guardian" and any(
                score == 100 for score in quiz_scores
            ):
                earned.append(badge_id)
        for badge_id in earned:
            if not Badge.objects.filter(user_id=user_id, badge_id=badge_id).exists():
                Badge.objects.create(user_id=user_id, badge_id=badge_id)
        return {"badges": earned}

    return {"error": f"Tool '{name}' not implemented"}
