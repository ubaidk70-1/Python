# quiz_engine.py
# Purpose: Handles how the quiz is conducted.

from utils import shuffle_questions

# ANSI color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def ask_question(question_data):
    """
    Displays a single question and captures user input.
    Allows user to type 'quit' or 'exit' to abort the quiz.
    Returns the user's answer string or None if they quit.
    """
    question = question_data["question"]
    options = question_data["options"]
    
    print(f"\n{YELLOW}{question}{RESET}")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    while True:
        # Get raw input to check for quit command first
        user_input = input("Your answer (or type 'quit' to exit): ").strip().lower()

        if user_input in ['quit', 'exit']:
            return None # Special value to signal quitting

        try:
            choice = int(user_input)
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"{RED}Invalid choice. Please enter a number from the options.{RESET}")
        except ValueError:
            print(f"{RED}Invalid input. Please enter a number or 'quit'.{RESET}")

def check_answer(user_answer, correct_answer):
    """Checks if the user's answer is correct and returns a boolean."""
    return user_answer.lower() == correct_answer.lower()

def run_quiz(questions):
    """
    Loops through selected questions, tracks score, and returns results.
    Returns: (score, incorrect_questions, quiz_aborted_flag)
    """
    score = 0
    incorrect_questions = []
    quiz_aborted = False
    
    shuffled_questions = shuffle_questions(list(questions))

    for question_data in shuffled_questions:
        user_answer = ask_question(question_data)

        # Check if the user decided to quit
        if user_answer is None:
            quiz_aborted = True
            break

        correct_answer = question_data["answer"]

        if check_answer(user_answer, correct_answer):
            print(f"{GREEN}Correct!{RESET}")
            score += 1
        else:
            print(f"{RED}Wrong! The correct answer was: {correct_answer}{RESET}")
            incorrect_questions.append(question_data)
    
    return score, incorrect_questions, quiz_aborted

def retry_incorrect_questions(incorrect_questions):
    """Allows the user to re-attempt incorrectly answered questions."""
    print("\n--- Let's retry the questions you got wrong ---")
    # The third return value (aborted flag) is ignored here, as quitting a retry session is less critical
    score, still_incorrect, _ = run_quiz(incorrect_questions)
    
    if not still_incorrect:
        print(f"{GREEN}Great job! You answered all of them correctly this time!{RESET}")
    else:
        print(f"{YELLOW}You still have {len(still_incorrect)} incorrect questions. Keep practicing!{RESET}")
