# CareerPath AI

A student-friendly career guidance web application built with Python Flask, SQLite, HTML, CSS and JavaScript.

## Features
- Student profile
- 15-question career assessment
- Top 5 career recommendations
- Suitability scores
- Career Explorer
- Career roadmap
- Skill-gap analysis
- Personalized 4-week starter action plan
- CareerBot chatbot
- SQLite database

## Run locally

1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Create a virtual environment:

   Windows:
   `python -m venv venv`
   `venv\Scripts\activate`

   macOS/Linux:
   `python3 -m venv venv`
   `source venv/bin/activate`

4. Install dependencies:
   `pip install -r requirements.txt`

5. Start:
   `python app.py`

6. Open:
   `http://127.0.0.1:5000`

## Notes
The included recommendation engine is local and works without an API key. It is intentionally a guidance tool rather than a guaranteed predictor. For production use, add authentication, stronger validation, secure secret management, a curated career database, and an AI API behind a server-side endpoint.
