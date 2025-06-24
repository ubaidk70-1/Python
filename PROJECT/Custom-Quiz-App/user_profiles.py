# user_profiles.py
# Purpose: Handles storing and retrieving user scores.

import json
import os
from datetime import datetime

# Define absolute path to data directory relative to this file
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
USER_PROFILES_FILE = os.path.join(DATA_DIR, "user_profiles.json")

def save_user_score(username, score_data):
    """Saves user score to a JSON file."""
    os.makedirs(DATA_DIR, exist_ok=True)  # Ensure the data directory exists

    try:
        with open(USER_PROFILES_FILE, "r") as f:
            profiles = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        profiles = {}

    if username not in profiles:
        profiles[username] = []

    score_entry = {
        "timestamp": datetime.now().isoformat(),
        "category": score_data["category"],
        "difficulty": score_data["difficulty"],
        "score_percent": score_data["score_percent"],
        "time_taken": score_data["time_taken"]
    }
    profiles[username].append(score_entry)

    with open(USER_PROFILES_FILE, "w") as f:
        json.dump(profiles, f, indent=4)

def load_user_score(username):
    """Retrieves past scores for a user."""
    try:
        with open(USER_PROFILES_FILE, "r") as f:
            profiles = json.load(f)
        return profiles.get(username, [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def display_user_scores(username):
    """Displays all past scores for a user."""
    scores = load_user_score(username)
    if not scores:
        print(f"\nNo scores found for {username}.")
        return

    print(f"\n--- Past Scores for {username} ---")
    for score in scores:
        print(
            f"Date: {datetime.fromisoformat(score['timestamp']).strftime('%Y-%m-%d %H:%M')}, "
            f"Category: {score['category']}, "
            f"Difficulty: {score['difficulty']}, "
            f"Score: {score['score_percent']:.2f}%, "
            f"Time: {score['time_taken']}"
        )
    print("---------------------------------")
