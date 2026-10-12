# 🎓 AI Career Guidance Chatbot

An interactive career guidance web application built with Python and Streamlit that helps students explore suitable career paths based on their interests, skills, education level, and goals.

The application recommends the top 3 matching careers, provides explanations for each recommendation, and suggests relevant courses and skills to develop.

🚀 Live Demo: https://ai-career-guidance-shathana.streamlit.app/

💻 GitHub Repository: https://github.com/shathanasri12/AI-Career-Guidance-Chatbot

## Features

Personalized top 3 career recommendations
Weighted career matching score
Career explanations and suggested courses
Skill-development guidance
Input validation and error handling
User feedback and automated tests

## Tech Stack

| Tool | Used for |
|---|---|
| Python 3.10+ | Programming language |
| Streamlit | Web interface |
| JSON | Career database (`data/careers.json`) |
| CSV | Feedback storage (`data/feedback.csv`) |
| pytest | Automated testing |

## Project Structure

```
AI-Career-Guidance/
├── app.py                  # Main Streamlit app (the web page)
├── requirements.txt        # Python packages to install
├── README.md               # This file
├── .gitignore              # Files Git should ignore
├── .streamlit/
│   └── config.toml         # Theme colours
├── assets/                 # Images and logos (optional)
├── data/
│   ├── careers.json        # Career database
│   └── feedback.csv        # Created automatically when feedback is saved
├── utils/
│   ├── __init__.py         # Makes "utils" a Python package
│   ├── validators.py       # Input validation
│   ├── recommender.py      # Scoring and explanation logic
│   └── feedback.py         # Saves and reads feedback
└── tests/
    ├── __init__.py
    └── test_core.py        # Automated tests
```

## How It Works

1. The student fills in the form in `app.py`.
2. `utils/validators.py` checks every answer.
3. `utils/recommender.py` gives each career in `data/careers.json` a score out of 100:
   - **45%** interest match
   - **40%** skill match
   - **15%** education fit
4. The 3 highest-scoring careers are shown with an explanation, courses and skills to build.
5. The student can rate the guidance, and `utils/feedback.py` saves it to `data/feedback.csv`.

## Input Validation

| Field | Rule |
|---|---|
| Name | 2-50 characters, starts with a letter, only letters, spaces, dots, apostrophes and hyphens |
| Age | Whole number from 13 to 60 |
| Interests | Choose 1 to 4 |
| Skills | Choose 1 to 6 |
| Feedback rating | Whole number from 1 to 5 |
| Feedback comment | Optional, maximum 500 characters |

If any rule fails, the app shows a red error message for each problem and does not continue.

## Error Handling

- **Missing or broken `careers.json`**: the app shows "Could not load career data" instead of crashing.
- **Problem while calculating results**: the error is caught and shown in a friendly message.
- **Feedback cannot be saved** (for example, the file is locked): the student sees "Could not save your feedback".
- **Spreadsheet safety**: feedback text that starts with `=`, `+`, `-` or `@` is neutralised so Excel cannot run it as a formula.

## Installation and Setup

### 1. Requirements

- Python 3.10 or newer (check with `python --version`)
- Git (optional, needed only for uploading to GitHub)
- VS Code (recommended)

### 2. Get the project

Download the project folder, or clone it from your GitHub repository page using
the "Code" button. Then open a terminal inside the `AI-Career-Guidance` folder.

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (Command Prompt)
.venv\Scripts\activate.bat

# Mac / Linux
source .venv/bin/activate
```

You should see `(.venv)` at the start of your terminal line.

### 5. Install the packages

```bash
pip install -r requirements.txt
```

## Run the App

```bash
streamlit run app.py
```

Your browser opens at http://localhost:8501. Press `Ctrl + C` in the terminal to stop the app.

If `streamlit` is not recognised, use:

```bash
python -m streamlit run app.py
```

## Run in VS Code

1. Open the `AI-Career-Guidance` folder with **File → Open Folder**.
2. Open a terminal with **Terminal → New Terminal**.
3. Activate the virtual environment (step 4 above).
4. Run `streamlit run app.py`.

## Run the Tests

```bash
python -m pytest -v
```

Every test should show `PASSED`. The tests cover the validators, the recommender
and saving and reading feedback.

### Manual test checklist

| Test | Expected result |
|---|---|
| Submit with an empty name | Error: "Please enter your name." |
| Name = `12345` | Name format error |
| Age = 5 | Error: "Age must be between 13 and 60." |
| No interests selected | Error: "Please select at least 1 interest." |
| 5 interests selected | Error: "Please select no more than 4 interests." |
| Technology + Engineering interests; Programming, Problem Solving, Analytical Thinking, Teamwork skills; Undergraduate | Software Developer is ranked first |
| Submit feedback | Green thank-you message, and `data/feedback.csv` is created |
| Comment longer than 500 characters | Error message |

## Add a New Career

Open `data/careers.json`, copy one of the existing blocks, and change its values:

```json
{
  "name": "Cyber Security Analyst",
  "description": "Protects computer systems and networks from attacks.",
  "interests": ["Technology", "Engineering"],
  "skills": ["Programming", "Problem Solving", "Analytical Thinking"],
  "education_levels": ["Undergraduate", "Graduate", "Postgraduate"],
  "courses": ["Google Cybersecurity Certificate (Coursera)"],
  "outlook": "High demand"
}
```

Remember to put a comma between career blocks. Interests and skills must use the
same names as the lists in `utils/recommender.py`. No Python changes are needed.

## Upload to GitHub

```bash
git init
git add .
git commit -m "Initial commit: AI Career Guidance Chatbot"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/career-guidance-chatbot.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username, after creating an empty repository
on github.com. The `.gitignore` file keeps `.venv/` and `data/feedback.csv` out of the upload.

## Deploy for Free (optional)

1. Push the project to GitHub.
2. Sign in at https://share.streamlit.io with your GitHub account.
3. Choose your repository and set the main file to `app.py`.
4. Click **Deploy** to get a public link.

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'streamlit'` | Activate `.venv`, then run `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'utils'` | Run the command from the project root, and check that `utils/__init__.py` exists |
| `streamlit: command not found` | Use `python -m streamlit run app.py` |
| "Could not load career data" | Check `data/careers.json` for a missing comma or bracket |
| PowerShell blocks the activate script | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then try again |

## Future Improvements

- Use the Claude API to write a personalised paragraph for each recommendation
- Add an admin page that shows feedback statistics
- Store data in SQLite instead of CSV
- Add more careers, courses and exam guidance

## License

This project is for learning purposes. You are free to use and modify it.
