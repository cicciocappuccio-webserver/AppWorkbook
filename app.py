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
    session['current_question'] = 0  # Zero-based index
    session['score'] = 0
    session['answers'] = []
    return render_template("index.html", questions=questions)

@app.route("/question/<int:question_id>")
def show_question(question_id):
    """Mostra una specifica domanda del quiz"""
    question_index = question_id - 1  # Convert to zero-based
    
    if question_index < 0 or question_index >= len(questions):
        return redirect(url_for('index'))
    
    session['current_question'] = question_index
    question_data = questions[question_index]
    
    return render_template(
        "question.html",
        question=question_data,
        question_number=question_id,  # 1-based for display
        total_questions=len(questions)
    )

@app.route("/submit", methods=["POST"])
def submit_answer():
    """Processa la risposta e passa alla prossima domanda o al risultato"""
    if 'current_question' not in session:
        return redirect(url_for('index'))
    
    current_index = session['current_question']
    selected_option = request.form.get('selected_option')
    
    # Verifica risposta
    is_correct = selected_option == questions[current_index]['answer']
    
    # Aggiorna punteggio
    if is_correct:
        session['score'] = session.get('score', 0) + 1
    
    # Salva risposta
    session['answers'] = session.get('answers', [])
    session['answers'].append({
        'question_id': questions[current_index]['id'],
        'selected': selected_option,
        'correct': questions[current_index]['answer'],
        'is_correct': is_correct,
        'explanation': questions[current_index].get('explanation', '')
    })
    
    # Determina prossima azione
    if current_index >= len(questions) - 1:  # Ultima domanda
        return redirect(url_for('show_result'))
    else:
        next_question_id = current_index + 2  # 1-based ID
        return redirect(url_for('show_question', question_id=next_question_id))

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
