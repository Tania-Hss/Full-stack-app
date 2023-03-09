import psycopg2
from psycopg2.extras import RealDictCursor

def select_all(query):
    conn = psycopg2.connect("dbname=art_gallary")
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def select_one(query, params):
    conn = psycopg2.connect("dbname=art_gallary")
    cur = conn.cursor()
    cur.execute(query, params)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result


def insert(query, params):
    conn = psycopg2.connect("dbname=art_gallary")
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    cur.close()
    conn.close()

def select_user_artwork(query, params):
    conn = psycopg2.connect("dbname=art_gallary")
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query, params)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def delete(query, params):
    conn = psycopg2.connect("dbname=art_gallary")
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    cur.close()
    conn.close()

