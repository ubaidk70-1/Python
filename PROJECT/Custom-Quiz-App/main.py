# main.py
# Purpose: Entry point of the App

import time
import json
import os
import sys
from quiz_data import quiz_data
from quiz_engine import run_quiz, retry_incorrect_questions
from user_profiles import save_user_score, display_user_scores
from utils import format_time, validate_input

# Get absolute path to the current directory (Custom-Quiz-App)
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_FILE = os.path.join(DATA_DIR, "quiz_results.json")

def validate_quiz_data():
    """
    Checks the integrity of the quiz_data structure before starting.
    Exits the application if any question is malformed.
    """
    required_keys = ['question', 'options', 'answer']
    for category, difficulties in quiz_data.items():
        for difficulty, questions in difficulties.items():
            if not questions:
                continue
            for i, question_data in enumerate(questions):
                if not all(key in question_data for key in required_keys):
                    print(f"FATAL ERROR: Malformed question in '{category}' -> '{difficulty}' at index {i}.")
                    print(f"Missing one or more keys: {required_keys}")
                    print(f"Problem data: {question_data}")
                    sys.exit(1)
    return True


def select_category():
    """Lets the user select a quiz category."""
    print("\nSelect a category:")
    categories = list(quiz_data.keys())
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= len(categories):
                return categories[choice - 1]
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a number.")

def select_difficulty(category):
    """Lets the user select a quiz difficulty level or 'all'."""
    print("\nSelect a difficulty:")
    difficulties = list(quiz_data[category].keys())
    difficulties.append("All")

    for i, difficulty in enumerate(difficulties, 1):
        print(f"{i}. {difficulty.capitalize()}")

    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= len(difficulties):
                selected = difficulties[choice - 1]
                return selected.lower() if selected == "All" else selected
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a number.")


def main():
    """Main function to run the quiz application."""
    validate_quiz_data()
    print("Quiz data validated successfully.")

    while True:
        username = input("Enter your username: ").strip()
        if username:
            break
        print("Username cannot be empty. Please try again.")

    while True:
        print(f"\nWelcome, {username}!")
        print("1. Start a new quiz")
        print("2. View my past scores")
        print("3. Exit")

        menu_choice = validate_input("Choose an option: ", ["1", "2", "3"])

        if menu_choice == "1":
            category = select_category()
            difficulty_choice = select_difficulty(category)

            questions = []
            if difficulty_choice == "all":
                for level in quiz_data[category]:
                    questions.extend(quiz_data[category][level])
            else:
                questions = quiz_data[category][difficulty_choice]

            if not questions:
                print("\nSorry, no questions available for this selection.")
                continue

            start_time = time.time()
            score, incorrect_questions, aborted = run_quiz(questions)
            end_time = time.time()

            if aborted:
                print("\nQuiz aborted. Returning to menu.")
                continue

            time_taken_seconds = end_time - start_time
            time_taken_formatted = format_time(time_taken_seconds)
            total_questions = len(questions)
            score_percent = (score / total_questions) * 100 if total_questions > 0 else 0

            print("\n--- Quiz Over! ---")
            print(f"Your score: {score}/{total_questions} ({score_percent:.2f}%)")
            print(f"Time taken: {time_taken_formatted}")

            score_data = {
                "category": category,
                "difficulty": difficulty_choice.capitalize(),
                "score_percent": score_percent,
                "time_taken": time_taken_formatted
            }
            save_user_score(username, score_data)

            # Ensure data directory exists
            os.makedirs(DATA_DIR, exist_ok=True)

            try:
                with open(RESULTS_FILE, "r") as f:
                    all_results = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                all_results = []

            all_results.append({
                "username": username,
                **score_data,
                "incorrect_questions": [q["question"] for q in incorrect_questions]
            })

            with open(RESULTS_FILE, "w") as f:
                json.dump(all_results, f, indent=4)

            if incorrect_questions:
                retry_choice = validate_input("\nRetry incorrect questions? (yes/no): ", ["yes", "no"])
                if retry_choice == "yes":
                    retry_incorrect_questions(incorrect_questions)

        elif menu_choice == "2":
            display_user_scores(username)

        elif menu_choice == "3":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
