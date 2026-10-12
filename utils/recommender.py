"""Career recommendation logic.

Scoring (out of 100):
  45% interest match + 40% skill match + 15% education fit
"""

import json
from pathlib import Path

# Path to data/careers.json, no matter where you run the app from
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "careers.json"

# Options shown in the form (kept here so app and tests share them)
INTERESTS = [
    "Technology", "Data & Analytics", "Design & Creativity", "Business",
    "Healthcare", "Science & Research", "Education", "Writing & Media",
    "Engineering",
]
SKILLS = [
    "Programming", "Mathematics", "Communication", "Problem Solving",
    "Creativity", "Leadership", "Analytical Thinking", "Teamwork",
    "Writing", "Empathy",
]
EDUCATION_LEVELS = [
    "High School", "Diploma", "Undergraduate", "Graduate", "Postgraduate",
]
GOALS = [
    "Get a job quickly",
    "Pursue higher studies",
    "Start my own business",
    "Switch to a new field",
    "Build a research career",
]

GOAL_TIPS = {
    "Get a job quickly": "Short certificates and a small portfolio of projects can get you job-ready fastest.",
    "Pursue higher studies": "Look for entrance exams, scholarships and university programmes in this field.",
    "Start my own business": "Practise this skill through freelance or side projects to build a client base early.",
    "Switch to a new field": "Start with a beginner certificate and build 2-3 projects to show your new skills.",
    "Build a research career": "Seek internships with professors and read recent papers in this area.",
}


def load_careers(path=DATA_FILE):
    """Load the career list from JSON, with clear errors if something is wrong."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            careers = json.load(file)
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Career data file not found: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"Career data file is not valid JSON: {error}") from error

    if not isinstance(careers, list) or not careers:
        raise ValueError("Career data must be a non-empty list.")
    return careers


def build_explanation(career, profile):
    """Write a plain-English reason for the recommendation."""
    parts = []

    if career["matched_interests"]:
        parts.append(
            "It matches your interest in " + ", ".join(career["matched_interests"]) + "."
        )
    else:
        parts.append("It does not directly match your chosen interests, but your skills fit.")

    if career["matched_skills"]:
        parts.append(
            "You already have useful skills for it: "
            + ", ".join(career["matched_skills"]) + "."
        )

    if profile["education"] in career["education_levels"]:
        parts.append(f"Your education level ({profile['education']}) is a good starting point.")
    else:
        parts.append(
            "You may need further study first, as this path usually needs a different education level."
        )

    tip = GOAL_TIPS.get(profile["goal"])
    if tip:
        parts.append(f"For your goal ('{profile['goal']}'): {tip}")

    return " ".join(parts)


def recommend_careers(profile, careers, top_n=3):
    """Score every career and return the best `top_n`.

    profile = {"interests": [...], "skills": [...], "education": "...", "goal": "..."}
    """
    user_interests = set(profile["interests"])
    user_skills = set(profile["skills"])
    results = []

    for career in careers:
        career_interests = set(career["interests"])
        career_skills = set(career["skills"])

        matched_interests = sorted(user_interests & career_interests)
        matched_skills = sorted(user_skills & career_skills)
        missing_skills = sorted(career_skills - user_skills)

        # Interest score: matching 2 interests (or all, if fewer) = full marks
        if career_interests:
            interest_score = min(1.0, len(matched_interests) / min(len(career_interests), 2))
        else:
            interest_score = 0.0

        skill_score = len(matched_skills) / len(career_skills) if career_skills else 0.0
        education_score = 1.0 if profile["education"] in career["education_levels"] else 0.4

        total = 0.45 * interest_score + 0.40 * skill_score + 0.15 * education_score

        item = dict(career)  # copy so we don't change the original data
        item["score"] = round(total * 100)
        item["matched_interests"] = matched_interests
        item["matched_skills"] = matched_skills
        item["missing_skills"] = missing_skills
        item["explanation"] = build_explanation(item, profile)
        results.append(item)

    # Highest score first; ties are sorted alphabetically
    results.sort(key=lambda r: (-r["score"], r["name"]))
    return results[:top_n]