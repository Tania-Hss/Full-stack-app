import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash

import db

def get_user_by_email(email):
    # selects all user data belonging to the users email
    result = db.select_one('SELECT users.id, users.name, users.email, users.password_hash FROM users WHERE email = %s;', [email])
    return result

def insert_user(name, email, password_hash):
    db.insert('INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)', 
    (name, email, password_hash))


     


