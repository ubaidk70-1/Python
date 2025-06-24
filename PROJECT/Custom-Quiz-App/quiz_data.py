# quiz_data.py
# Purpose: Stores quiz questions, options, correct answers, categories, and difficulty levels.

quiz_data = {
    "Python": {
        "easy": [
            {
                "question": "What does the `print()` function do in Python?",
                "options": ("Displays output to the console", "Takes user input", "Defines a variable", "Performs a calculation"),
                "answer": "Displays output to the console"
            },
            {
                "question": "Which of the following is a valid variable name in Python?",
                "options": ("my-var", "1var", "_my_var", "var$"),
                "answer": "_my_var"
            },
            {
                "question": "What is the result of `2 + 2` in Python?",
                "options": ("22", "4", "Error", "None"),
                "answer": "4"
            }
        ],
        "medium": [
            {
                "question": "What is a list comprehension in Python?",
                "options": (
                    "A way to create lists using a concise syntax",
                    "A type of loop for lists",
                    "A function to sort a list",
                    "A method to add items to a list"
                ),
                "answer": "A way to create lists using a concise syntax"
            },
            {
                "question": "What is the difference between a list and a tuple?",
                "options": (
                    "Lists are mutable, tuples are immutable",
                    "Tuples are mutable, lists are immutable",
                    "They are the same",
                    "Lists can only store integers"
                ),
                "answer": "Lists are mutable, tuples are immutable"
            }
        ],
        "hard": [
            {
                "question": "What is a decorator in Python?",
                "options": (
                    "A function that modifies the behavior of another function",
                    "A way to style text",
                    "A special type of variable",
                    "A tool for debugging"
                ),
                "answer": "A function that modifies the behavior of another function"
            }
        ]
    },
    "General Knowledge": {
        "easy": [
            {
                "question": "What is the capital of France?",
                "options": ("Berlin", "Madrid", "Paris", "Rome"),
                "answer": "Paris"
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ("Earth", "Mars", "Jupiter", "Venus"),
                "answer": "Mars"
            }
        ],
        "medium": [
            {
                "question": "Who wrote 'Romeo and Juliet'?",
                "options": ("Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"),
                "answer": "William Shakespeare"
            }
        ]
    }
}

