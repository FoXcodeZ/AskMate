import connection
import util


@connection.connection_handler
def get_last_5_questions(cursor):
    cursor.execute("""
        SELECT * FROM question
        ORDER BY submission_time
        DESC LIMIT 5; """)
    return cursor.fetchall()


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
    SELECT * FROM question; """)
    return cursor.fetchall()


@connection.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""
        SELECT * FROM question
        WHERE id = %(question_id)s """,
                   {'question_id': question_id})
    return cursor.fetchall()


@connection.connection_handler
def get_all_answers_to_question(cursor, question_id):
    cursor.execute("""
        SELECT * FROM answer
        WHERE question_id = %(question_id)s""",
                   {'question_id': question_id})
    return cursor.fetchall()


@connection.connection_handler
def add_question(cursor, title, message):
    time = util.get_linux_timestamp()
    view_number = 0
    vote_number = 0
    cursor.execute("""
        INSERT INTO question (submission_time, title, message, view_number, vote_number)
        VALUES(%(submission_time)s, %(title)s, %(message)s, %(view_number)s, %(vote_number)s) """,
                   {'submission_time': time, 'title': title, 'message': message,
                    'view_number': view_number, 'vote_number': vote_number})


@connection.connection_handler
def add_answer(cursor, question_id, message):
    time = util.get_linux_timestamp()
    vote_number = 0
    cursor.execute("""
        INSERT INTO answer (submission_time, vote_number, question_id, message)
        VALUES(%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s) """,
                   {'submission_time': time, 'vote_number': vote_number,
                    'question_id': question_id, 'message': message})


@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
    DELETE FROM answer WHERE question_id = %(question_id)s;
    DELETE FROM question WHERE id = %(question_id)s """,
                   {'question_id': question_id})


@connection.connection_handler
def count_nr_of_views(cursor, question_id):
    cursor.execute("""
    UPDATE question
    SET view_number = view_number + 1
    WHERE id = %(question_id)s """,
                   {'question_id': question_id})


@connection.connection_handler
def vote_up_question(cursor, question_id,):
    cursor.execute("""
    UPDATE question
    SET vote_number = vote_number + 1
    WHERE id = %(question_id)s """,
                   {'question_id': question_id})


@connection.connection_handler
def vote_down_question(cursor, question_id):
    cursor.execute("""
    UPDATE question
    SET vote_number = vote_number - 1
    WHERE id = %(question_id)s """,
                   {'question_id': question_id})


@connection.connection_handler
def register_user(cursor, user_name, user_email, hashed_password):
    date = util.get_linux_timestamp()
    cursor.execute("""
    INSERT INTO users(reg_date, user_name, user_email, user_password)
    VALUES(%(reg_date)s, %(user_name)s, %(user_email)s, %(user_password)s)""",
                   {'user_name': user_name, 'reg_date': date, 'user_email': user_email,
                    'user_password': hashed_password})


@connection.connection_handler
def get_user_id(cursor, user_name):
    cursor.execute("""
    SELECT user_id FROM users
    WHERE user_name = %(user_name)s """,
                   {'user_name': user_name})
    return cursor.fetchall()


@connection.connection_handler
def get_user_password(cursor, user_name):
    cursor.execute("""
    SELECT user_password FROM users
    WHERE user_name = %(user_name)s """,
                   {'user_name': user_name})
    hashed_password = cursor.fetchone()
    return hashed_password['user_password']


@connection.connection_handler
def get_all_users(cursor):
    cursor.execute("""
    SELECT * FROM users""")
    return cursor.fetchall()
