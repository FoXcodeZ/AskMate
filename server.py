from flask import Flask, session, render_template, request, escape, url_for, redirect
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    last_5_questions = data_manager.get_last_5_questions()
    if 'username' in session:
        return render_template('index.html', last_5_questions=last_5_questions, title="Home", user=session['username'])
    else:
        return render_template('index.html', last_5_questions=last_5_questions, title="Home")


@app.route('/display_all_questions')
def display_all_questions():
    all_questions = data_manager.get_all_questions()
    return render_template('display-all-questions.html', all_questions=all_questions, title="Display all questions")


@app.route('/question/<int:question_id>')
def display_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_all_answers_to_question(question_id)
    data_manager.count_nr_of_views(question_id)
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


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect(url_for('display_all_questions', title="Delete Question"))


@app.route('/question/<question_id>/<template_name>/vote-up')
def vote_up_question(question_id, template_name):
    data_manager.vote_up_question(question_id)
    return display_current_template(template_name)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        print("NONE")
        return render_template('registration.html', title="Registration")
    else:
        print("YES")
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        password_1 = request.form['password_1']
        password_2 = request.form['password_2']

        data_manager.register_user(user_name, user_email)
        return redirect(url_for('index', title="Home"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title="Login")
    session['username'] = request.form['user_name']
    return redirect(url_for('index', user=session['username']))


@app.route('/question/<question_id>/<template_name>/vote-down')
def vote_down_question(question_id, template_name):
    data_manager.vote_down_question(question_id)
    return display_current_template(template_name)


def display_current_template(template_name):
    if template_name == "index.html":
        return index()
    else:
        return display_all_questions()


@app.route('/list_users')
def list_users():
    all_users = data_manager.get_all_users()
    return render_template('users.html', all_users=all_users)


if __name__ == '__main__':
    app.debug = True
    app.run()
