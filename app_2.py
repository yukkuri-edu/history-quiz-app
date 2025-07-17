from flask import Flask, request, render_template, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "kawai_manage_12345678"

quiz_data = {
    1 : {
        "question":"dummy_私の夢",
        "choices":{"A":"4日" , "B":"14日" , "C":"5日" , "D":"25日"},
        "correct_answer": "C"
        
    },
    2 : {
        "question":"dummy_胡蝶の夢",
        "choices":{"A":"4日" , "B":"荘子" , "C":"5日" , "D":"25日"},
        "correct_answer": "B"
        
    },

    3 : {
        "question":"dummy_キング牧師の夢",
        "choices":{"A":"4日" , "B":"In the sun" , "C":"5日" , "D":"25日"},
        "correct_answer": "B"
        
    },    
}

@app.route("/")
def show_quiz():
    if 'current_question_id' not in session or request.args.get('restart'):
        session.clear()
        session['current_question_id'] = 1
        session['score'] = 0
        session['quiz_started']

    question_id = session.get('current_question_id')
    question = quiz_data.get(question_id)

    if not question:
        session.clear()
        return "問題が見つかりません" , 404
    
    return render_template(
        "quiz.html",
        question_data=question,
        question_number=question_id,
        show_result_on_question = False,
        show_next_button = False,
        show_final_result_button = False
    )

@app.route("/answer", methods=["POST"])
def process_answer():
    user_answer = request.form.get("user_answer")
    question_id = session.get('current_question_id')

    if not question_id or not user_answer:
        return redirect(url_for('show_quiz'))
    
    question = quiz_data.get(question_id)
    if not question:
        return "問題が見つかりません", 404
    
    is_correct = (user_answer == question["correct_answer"])

    if is_correct:
        session['score'] = session.get('score', 0) + 1

    next_question_id = question_id + 1

    render_params = {
        "question_data": question,
        "question_number": question_id,
        "user_answered": user_answer,
        "is_correct": is_correct,
        "show_result_on_question": True,
        "show_next_button": False,
        "show_final_result_button": False
    }

    if next_question_id <= len(quiz_data):
        session['current_question_id'] = next_question_id
        render_params["show_next_button"] = True
    else:
        render_params["show_final_result_button"] = True
    return render_template("quiz.html", **render_params)

@app.route("/final_result")
def show_final_result():
    final_score = session.get('score', 0)
    total_questions = len(quiz_data)
    session.clear()

    return render_template(
        "final_result.html",
        final_score = final_score,
        total_questions = total_questions
    )

if __name__ == "__main__":
    app.run(debug=True)