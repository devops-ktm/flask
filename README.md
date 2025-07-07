Flask Quiz App
==============

A simple quiz application built with Flask. Users can log in, answer quiz questions, and see their results.

Features
--------

- User login (single user for demo)
- Multiple choice quiz questions
- Score tracking
- Result display
- Logout functionality

Technologies Used
-----------------

- Python 3
- Flask (web framework)
- HTML & CSS (inline in templates)

How to Run
----------

Prerequisites:

- Python 3 installed on your machine
- pip package manager

Steps:

1. Create and activate a virtual environment:

   python -m venv venv

   On Windows, activate with:

   venv\Scripts\activate

2. Install Flask:

   pip install flask

3. Save your Flask app code into a file named `app.py`

4. Run the Flask development server:

   python -m flask --app app.py --debug run

5. Open your browser and go to:

   http://127.0.0.1:5000

Usage
-----

- Login using username: admin and password: password123
- Answer quiz questions and submit
- See your final score
- Logout when finished


