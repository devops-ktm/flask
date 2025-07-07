from flask import Flask, render_template_string, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key in production

# In-memory storage (replace with a database in production)
users = {'admin': 'password123'}
questions = [
    {'question': 'What is 2 + 2?', 'options': ['3', '4', '5', '6'], 'answer': '4'},
    {'question': 'Which planet is known as the Red Planet?', 'options': ['Earth', 'Mars', 'Jupiter', 'Venus'], 'answer': 'Mars'},
    {'question': 'What is the capital of France?', 'options': ['London', 'Berlin', 'Paris', 'Madrid'], 'answer': 'Paris'}
]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            session['username'] = username
            session['score'] = 0
            return redirect(url_for('quiz'))
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f0f2f5; }
                .container { max-width: 400px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
                h2 { color: #333; text-align: center; }
                .form-group { margin-bottom: 15px; }
                input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 4px; }
                input[type="submit"] { background-color: #007bff; color: white; padding: 10px; border: none; border-radius: 4px; cursor: pointer; width: 100%; }
                input[type="submit"]:hover { background-color: #0056b3; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Login</h2>
                <form method="post">
                    <div class="form-group">
                        <input type="text" name="username" placeholder="Username" required>
                    </div>
                    <div class="form-group">
                        <input type="password" name="password" placeholder="Password" required>
                    </div>
                    <input type="submit" value="Login">
                </form>
            </div>
        </body>
        </html>
    ''')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if 'question_index' not in session:
        session['question_index'] = 0
        session['score'] = 0
        random.shuffle(questions)

    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer == questions[session['question_index']]['answer']:
            session['score'] += 1
        session['question_index'] += 1
        if session['question_index'] >= len(questions):
            return redirect(url_for('result'))

    if session['question_index'] < len(questions):
        current_question = questions[session['question_index']]
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f0f2f5; }
                    .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
                    h2 { color: #333; }
                    .question { margin-bottom: 20px; }
                    .options { margin: 10px 0; }
                    input[type="radio"] { margin-right: 10px; }
                    input[type="submit"] { background-color: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
                    input[type="submit"]:hover { background-color: #218838; }
                    a { color: #007bff; text-decoration: none; display: block; text-align: center; margin-top: 10px; }
                    a:hover { text-decoration: underline; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Quiz - Question {{ question_index + 1 }} of {{ total_questions }}</h2>
                    <form method="post">
                        <div class="question">{{ current_question.question }}</div>
                        <div class="options">
                            {% for option in current_question.options %}
                                <div><input type="radio" name="answer" value="{{ option }}" required> {{ option }}</div>
                            {% endfor %}
                        </div>
                        <input type="submit" value="Next">
                    </form>
                    <a href="{{ url_for('logout') }}">Logout</a>
                </div>
            </body>
            </html>
        ''', question_index=session['question_index'], total_questions=len(questions), current_question=current_question)
    return redirect(url_for('result'))

@app.route('/result')
def result():
    if 'username' not in session:
        return redirect(url_for('login'))
    score = session['score']
    total = len(questions)
    session.pop('question_index', None)
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f0f2f5; }
                .container { max-width: 400px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
                h2 { color: #333; text-align: center; }
                .result { font-size: 18px; color: #28a745; text-align: center; }
                a { color: #007bff; text-decoration: none; display: block; text-align: center; margin-top: 10px; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Quiz Result</h2>
                <div class="result">Your Score: {{ score }} / {{ total }}</div>
                <a href="{{ url_for('quiz') }}">Take Quiz Again</a>
                <a href="{{ url_for('logout') }}">Logout</a>
            </div>
        </body>
        </html>
    ''', score=score, total=total)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('score', None)
    session.pop('question_index', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)