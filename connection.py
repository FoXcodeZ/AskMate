import psycopg2
import psycopg2.extras
import psycopg2.extensions
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection_string():
    psql_db_name = os.environ.get('PSQL_DB_NAME')
    psql_user_name = os.environ.get('PSQL_USER_NAME')
    psql_password = os.environ.get('PSQL_PASSWORD')
    psql_host = os.environ.get('PSQL_HOST')

    if psql_db_name and psql_user_name and psql_password and psql_host:
        return f'postgresql://{psql_user_name}:{psql_password}@{psql_host}/{psql_db_name}'
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        dict_cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return_function = function(dict_cursor, *args, **kwargs)
        dict_cursor.close()
        connection.close()
        return return_function
    return wrapper


def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print("Could not connect to the database.")
        raise exception
    return connection
