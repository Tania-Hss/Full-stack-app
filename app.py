from flask import Flask, render_template, request, redirect, session
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'in ye raze'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    password_hash = generate_password_hash(password)

    db_cursor.execute('INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)', 
    [name, email, password_hash])

    db_connection.commit()
    db_cursor.close()
    db_connection.close()

    return redirect('/login')


@app.post('/logout')
def logout_user():
    session.pop('user_id')
    session.pop('user_name')
    session.pop('user_email')

    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
       return render_template('login.html')

    user_email = request.form.get('email')
    user_password = request.form.get('password')
    
    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()

    
    db_cursor.execute('SELECT id, name, email, password_hash FROM users WHERE email = %s;', [user_email])
    result = db_cursor.fetchone()

    password_matches = check_password_hash(result[3], user_password)
    db_cursor.close()
    db_connection.close()
    
    if password_matches:
        session['user_id'] = result[0]
        session['user_name'] = result[1]
        session['user_email'] = result[2]
        return redirect('/')
    else:
        return redirect('/login')


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'GET':
        artwork_id = request.args.get('id')
        artwork_title = request.args.get('title')
        artwork_description = request.args.get('description')
        artwork_img = request.args.get('img')
    
        return render_template("edit_artwork.html", artwork_id=artwork_id,artwork_title=artwork_title,artwork_description=artwork_description,artwork_img=artwork_img)
    
    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()

    artwork_id = request.form['id']
    artwork_title = request.form['title']
    artwork_description = request.form['description']
    artwork_img = request.form['file_img']
    
    db_cursor.execute("UPDATE artworks SET title = %s, description = %s, file_img = %s WHERE id = %s", [
    artwork_title, artwork_description , artwork_img , artwork_id])
    

    db_connection.commit()
    db_cursor.close()
    db_connection.close()

    return redirect('/')


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'GET':
        artwork_id = request.args.get('id')
        artwork_title = request.args.get('title')

        return render_template("delete_artwork.html", artwork_id = artwork_id, artwork_title=artwork_title)

    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()

    artwork_id = request.form['id']
    
    db_cursor.execute("DELETE FROM artworks WHERE id = %s", [artwork_id])
    
    db_connection.commit()
    db_cursor.close()
    db_connection.close()

    return redirect('/') 



@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('add_artwork.html')
    
    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()

    art_item = {
        "title": request.form['title'],
        "description": request.form['description'],
        "file_img": request.form['file_img'],
        "user_id": request.form['user_id']
    }

    db_cursor.execute("INSERT INTO artworks(title, description, file_img, user_id) VALUES (%s, %s, %s, %s)", [
    art_item['title'], art_item['description'], art_item['file_img'], art_item['user_id']])
    

    db_connection.commit()
    db_cursor.close()
    db_connection.close()

    return redirect('/')


@app.route('/')
def index():
    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()

    db_cursor.execute("SELECT id, title, description, file_img, user_id FROM artworks;")
    rows = db_cursor.fetchall()
    art_items = []
    for row in rows:
        art_items.append(
            {
               "id": row[0],
                "title": row[1],
                "description": row[2],
                "file_img": row[3],
                "user_id": row[4]
            }
        )

    db_cursor.close()
    db_connection.close()
    
    return render_template("home.html", art_items=art_items, user_name = session.get('user_name'))

if __name__ == "__main__":
    app.run(debug = True)
