import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash


def get_user_by_email(email):
    conn = psycopg2.connect("dbname=art_gallary")
    cur = conn.cursor()

    # selects all user data belonging to the users email
    cur.execute('SELECT users.id, users.name, users.email, users.password_hash FROM users WHERE email = %s;', [email])
    result = cur.fetchone()

    cur.close()
    conn.close()
    return result

def insert_user(name, email, password_hash):
    conn = psycopg2.connect("dbname=art_gallary")
    cur = conn.cursor()
    cur.execute('INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)', 
    (name, email, password_hash))
    conn.commit()
    cur.close()
    conn.close()

     


