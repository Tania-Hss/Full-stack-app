import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash


def get_user_by_email(email):
    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()

    # selects all user data belonging to the users email
    db_cursor.execute('SELECT users.id, users.name, users.email, users.password_hash FROM users WHERE email = %s;', [email])
    result = db_cursor.fetchone()

    db_cursor.close()
    db_connection.close()
    return result

def insert_user(name, email, password_hash):
    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()
    db_cursor.execute('INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)', 
    (name, email, password_hash))
    db_connection.commit()
    db_cursor.close()
    db_connection.close()


