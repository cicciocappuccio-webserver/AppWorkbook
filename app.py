from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret_key_for_session"  # Required for session handling

# Sample workbook questions
questions = [
    {"id": 1, "question": "What is the capital of the United States?", "options": ["New York", "Washington, D.C.", "Boston", "Chicago"], "answer": "Washington, D.C."},
    {"id": 2, "question": "Name one U.S. territory.", "options": ["Puerto Rico", "Hawaii", "Alaska", "Texas"], "answer": "Puerto Rico"},
    {"id": 3, "question": "What ocean is on the East Coast of the United States?", "options": ["Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"], "answer": "Atlantic Ocean"}
]

@app.route("/")
def index():
    # Reset session data for a new quiz
    session['current_question'] = 0
    session['score'] = 0
    return render_template("index.html", questions=questions)

@app.route("/question")
def question():
    current_question = session.get('current_question', 0)
    if current_question >= len(questions):
        # All questions answered, show the score
        return redirect(url_for("result"))
    question = questions[current_question]
    return render_template("question.html", question=question)

@app.route("/submit", methods=["POST"])
def submit():
    # Process the submitted answer
    current_question = session.get('current_question', 0)
    selected_option = request.form.get(str(questions[current_question]['id']))

    # Check if the answer is correct
    if selected_option == questions[current_question]['answer']:
        session['score'] += 1

    # Move to the next question
    session['current_question'] += 1
    return redirect(url_for("question"))

@app.route("/result")
def result():
    score = session.get('score', 0)
    total = len(questions)
    return render_template("result.html", score=score, total=total)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Usa la porta fornita da Render o fallback a 5000
    app.run(host="0.0.0.0", port=port)