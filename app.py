from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', generate_password_hash('default-secret-key'))

# Configurazione
app.config.update(
    SESSION_PERMANENT=False,
    PERMANENT_SESSION_LIFETIME=1800,  # 30 minuti
    TEMPLATES_AUTO_RELOAD=True
)

# Database delle domande
questions = [
    {
        "id": 1,
        "question": "What is the capital of the United States?",
        "options": ["New York", "Washington, D.C.", "Boston", "Chicago"],
        "answer": "Washington, D.C.",
        "explanation": "Washington, D.C. has been the federal capital since 1800."
    },
    {
        "id": 2,
        "question": "Name one U.S. territory.",
        "options": ["Puerto Rico", "Hawaii", "Alaska", "Texas"],
        "answer": "Puerto Rico",
        "explanation": "Puerto Rico is an unincorporated U.S. territory."
    },
    {
        "id": 3,
        "question": "What ocean is on the East Coast of the United States?",
        "options": ["Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"],
        "answer": "Atlantic Ocean",
        "explanation": "The Atlantic Ocean borders the East Coast of the U.S."
    }
]

@app.route("/")
def index():
    """Pagina iniziale del quiz"""
    session.clear()
    session['current_question'] = 0
    session['score'] = 0
    session['answers'] = []
    return render_template("index.html", questions=questions)

@app.route("/question/<int:qid>")
def show_question(qid):
    """Mostra una specifica domanda del quiz"""
    if qid < 1 or qid > len(questions):
        return redirect(url_for('index'))
    
    session['current_question'] = qid - 1
    question_data = questions[qid - 1]
    
    return render_template(
        "question.html",
        question=question_data,
        progress=f"{qid}/{len(questions)}",
        total_questions=len(questions)
    )

@app.route("/submit", methods=["POST"])
def submit_answer():
    """Processa la risposta e passa alla prossima domanda o al risultato"""
    if 'current_question' not in session:
        return redirect(url_for('index'))
    
    current_q = session['current_question']
    if current_q >= len(questions):
        return redirect(url_for('show_result'))
    
    selected_option = request.form.get(str(questions[current_q]['id']))
    is_correct = selected_option == questions[current_q]['answer']
    
    if is_correct:
        session['score'] = session.get('score', 0) + 1
    
    session['answers'] = session.get('answers', [])
    session['answers'].append({
        'question_id': questions[current_q]['id'],
        'selected': selected_option,
        'correct': questions[current_q]['answer'],
        'is_correct': is_correct,
        'explanation': questions[current_q].get('explanation', '')
    })
    
    next_q = current_q + 1
    if next_q < len(questions):
        return redirect(url_for('show_question', qid=next_q + 1))
    else:
        return redirect(url_for('show_result'))

@app.route("/result")
def show_result():
    """Mostra i risultati del quiz"""
    if 'score' not in session:
        return redirect(url_for('index'))
    
    return render_template(
        "result.html",
        score=session.get('score', 0),
        total=len(questions),
        answers=session.get('answers', []),
        questions=questions
    )

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve i file statici"""
    return send_from_directory('static', filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get('DEBUG', 'False') == 'True'
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
