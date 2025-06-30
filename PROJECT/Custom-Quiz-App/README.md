#  Custom Quiz Application

A terminal-based Python quiz application that allows users to select quiz categories, choose difficulty levels, and receive instant feedback with performance tracking.

---

## Features

- **MCQ-based Questions** with 4 options
- **Multiple Categories** (e.g., Python Basics, Data Structures)
- **Difficulty Levels**: Easy, Medium, Hard
- **Score Tracking**: Percentage score with time taken
- **Retry Incorrect Questions** to reinforce learning
- **User Profiles** to store quiz history (JSON-based)
- **Data Validation** for clean question structure
- **Colored CLI Feedback** for correct/incorrect answers
- **Randomized Question Order**
- **Stores Results** in `data/quiz_results.json` and `data/user_profiles.json`

---

## 🗂️ Project Structure

```
Custom-Quiz-App/
│
├── quiz_data.py         # Question bank (organized by category and difficulty)
├── quiz_engine.py       # Core quiz logic and interaction
├── user_profiles.py     # Handles saving/viewing user scores
├── utils.py             # Helper functions (e.g., input validation, time formatting)
├── main.py              # Entry point and main menu
│
├── data/
│   ├── quiz_results.json    # Stores detailed quiz attempts (auto-created)
│   └── user_profiles.json   # Stores user score history (auto-created)
│
└── README.md            # Project documentation
```



---

## How to Run

1. **Clone the Repository**
   
   git clone https://github.com/your-username/your-repo-name.git

   cd your-repo-name/Custom-Quiz-App
   
3. **Run the Application**
    python main.py

4. **Follow Prompts to:**

  - Enter your username

  - Choose category and difficulty

  - Take the quiz and view your results!

## Dependencies

No external dependencies required. Built with:

   - Python 3.6+

   - Standard libraries: json, os, time, random, datetime, sys

## Future Improvements (Optional Ideas)

  - Add a GUI using tkinter or PyQt

  - Export results to PDF or CSV

  - Add timed quizzes or leaderboard support

##  What You’ll Learn

  - Working with dictionaries and nested structures
  - Functions and modularization
  - Input validation and user interaction
  - File I/O using JSON
  - Reusability and code separatio

## Author
Made by Ubaid Khan — as part of your Python learning journey!
