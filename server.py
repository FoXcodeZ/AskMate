import flask.sessions
from flask import Flask, session, render_template, request, escape, url_for, redirect, make_response
import data_manager
import util
from flask_session import Session
from flask_cors import CORS

app = Flask(__name__)
SECRET_KEY = "_435%k^&/a$@5z_#654fg"
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
CORS(app)


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    username = session['username'] if 'username' in session else None
    last_5_questions = data_manager.get_last_5_questions()
    return render_template('index.html', last_5_questions=last_5_questions, title="Home", user=username)


@app.route('/display_all_questions')
def display_all_questions():
    username = session['username'] if 'username' in session else None
    all_questions = data_manager.get_all_questions()
    return render_template('display-all-questions.html', all_questions=all_questions, title="Display all questions", user=username)


@app.route('/question/<int:question_id>')
def display_question(question_id):
    username = session['username'] if 'username' in session else None
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_all_answers_to_question(question_id)
    data_manager.count_nr_of_views(question_id)
    return render_template('display-question.html', question_id=question_id, question=question,
                           answers=answers, title='Display Question', user=username)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    username = session['username'] if 'username' in session else None
    if request.method == "POST":
        title = request.form['title']
        message = request.form['message']
        data_manager.add_question(title, message)
        return redirect('/index')
    return render_template('add-question.html', title='Add Question', user=username)


@app.route('/question/<int:question_id>/add-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    username = session['username'] if 'username' in session else None
    if request.method == 'GET':
        return render_template('add-answer.html', question_id=question_id, title='Add Answer')
    message = request.form['message']
    data_manager.add_answer(question_id, message)
    return redirect(url_for("display_question", question_id=question_id, title="Display Question", user=username))


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    username = session['username'] if 'username' in session else None
    data_manager.delete_question(question_id)
    return redirect(url_for('display_all_questions', title="Delete Question", user=username))


@app.route('/question/<question_id>/<template_name>/vote-up')
def vote_up_question(question_id, template_name):
    data_manager.vote_up_question(question_id)
    return display_current_template(template_name)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    username = session['username'] if 'username' in session else None
    if request.method == 'GET':
        return render_template('registration.html', title="Registration", user=username)
    else:
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        password_1 = request.form['password_1']
        password_2 = request.form['password_2']
        if password_1 == password_2 and '@' in user_email:
            hashed_password = util.hash_password(password_1)
            data_manager.register_user(user_name, user_email, hashed_password)
            return redirect(url_for('index', title="Home", user=username))
        else:
            render_template('registration.html', title="Registration", user=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = session['username'] if 'username' in session else None
    if request.method == "POST":
        user_name = request.form["user_name"]
        plain_password = request.form["password_1"]
        print(plain_password)
        hashed_password = data_manager.get_user_password(user_name)

        if util.verify_password(plain_password, hashed_password):
            session["username"] = user_name
            return redirect(url_for('index', user=session['username']))
    return render_template('login.html', title="Login", user=username)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.clear()
    return redirect('/')


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
    username = session['username'] if 'username' in session else None
    all_users = data_manager.get_all_users()
    return render_template('users.html', all_users=all_users, user=username)


if __name__ == '__main__':
    app.run(debug=True)
