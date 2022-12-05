from flask import Flask, render_template, request, url_for, redirect
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    last_5_questions = data_manager.get_last_5_questions()
    return render_template('index.html', last_5_questions=last_5_questions, title="Home")


@app.route('/display_all_questions')
def display_all_questions():
    all_questions = data_manager.get_all_questions()
    return render_template('display-all-questions.html', all_questions=all_questions, title="Display all questions")


@app.route('/question/<int:question_id>')
def display_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_all_answers_to_question(question_id)
    return render_template('display-question.html', question_id=question_id, question=question,
                           answers=answers, title='Display Question')


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == "POST":
        title = request.form['title']
        message = request.form['message']
        data_manager.add_question(title, message)
        return redirect('/index')
    return render_template('add-question.html', title='Add Question')


@app.route('/question/<int:question_id>/add-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'GET':
        return render_template('add-answer.html', question_id=question_id, title='Add Answer')
    message = request.form['message']
    data_manager.add_answer(question_id, message)
    return redirect(url_for("display_question", question_id=question_id, title="Display Question"))


@app.route('//question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect(url_for('display_all_questions', title="Delete Question"))


if __name__ == '__main__':
    app.debug = True
    app.run()
