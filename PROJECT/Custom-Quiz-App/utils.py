# utils.py
# Purpose: Utility functions for time tracking, formatting, or type casting.

import random
import time

def format_time(seconds):
    """Converts seconds to a mm:ss format."""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def shuffle_questions(questions):
    """Shuffles a list of questions."""
    random.shuffle(questions)
    return questions

def validate_input(prompt, valid_options):
    """Ensures user input is one of the valid options."""
    while True:
        user_input = input(prompt).strip()
        if user_input in valid_options:
            return user_input
        else:
            print(f"Invalid input. Please choose from: {', '.join(valid_options)}")