from flask import Flask, render_template, request, redirect, session
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from cloudinary import CloudinaryImage
import cloudinary.uploader
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.config['SECRET_KEY'] = 'in ye raze'


@app.route('/my_artworks')
def my_artworks():
    # Check if user is logged in 
    if 'user_id' not in session:
        return redirect('/login')
    
    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()
    # select all the artworks from the database that belong to the user 
    db_cursor.execute("SELECT artworks.id, artworks.title, artworks.description, artworks.img_url, artworks.user_id FROM artworks JOIN users ON artworks.user_id = users.id WHERE users.id = %s", [session['user_id']])
    rows = db_cursor.fetchall()
    
    user_artwork = []
    for row in rows:
        user_artwork.append(
            {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'img_url': row[3],
                'user_id': row[4]
            }
        )

    db_cursor.close()
    db_connection.close()

    return render_template('my_artworks.html', user_artwork = user_artwork , user_name = session.get('user_name'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # accesses the signup page
    if request.method == 'GET':
        return render_template('signup.html')
    # signup form is submitted and data from form is inserted into database
    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    # check to see if email already in database
    db_cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    exists = db_cursor.fetchone()
    if exists:
        # if email already exists we pass error message
        db_cursor.close()
        db_connection.close()
        error = 'Email already in use. Please use a different Email address.'
        return render_template('signup.html', error=error)
    # if email is new we define the password hash and insert (name, email, password_hash) in database
    password_hash = generate_password_hash(password)

    db_cursor.execute('INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)', 
    (name, email, password_hash))

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
    # accesses the login page
    if request.method == 'GET':
       return render_template('login.html')
    
    user_email = request.form.get('email')
    user_password = request.form.get('password')
    
    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()

    # selects all user data belonging to the users email
    db_cursor.execute('SELECT users.id, users.name, users.email, users.password_hash FROM users WHERE email = %s;', [user_email])
    result = db_cursor.fetchone()
    if result is None:
        # If the email does not exist, redirect with an error message
        return render_template('login.html', error='Invalid email or password')

    password_matches = check_password_hash(result[3], user_password)

    db_cursor.close()
    db_connection.close()
    # if password matches result is saved to session to identify user
    if password_matches:
        session['user_id'] = result[0]
        session['user_name'] = result[1]
        session['user_email'] = result[2]
        return redirect('/')
    else:
        return render_template('login.html', error='Invalid email or password')


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if 'user_id' not in session:
        return redirect('/login')
    # gets artwork information from query parameters
    if request.method == 'GET':
        artwork_id = request.args.get('id')
        artwork_title = request.args.get('title')
        artwork_description = request.args.get('description')
        artwork_img = request.args.get('img')
    
        return render_template("edit_artwork.html", artwork_id=artwork_id,artwork_title=artwork_title,artwork_description=artwork_description,artwork_img=artwork_img, user_name = session.get('user_name'))
    
    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()

    artwork_id = request.form['id']
    artwork_title = request.form['title']
    artwork_description = request.form['description']
    artwork_img = request.files.get('img')
    # if image exits then upload to cloudinary 
    if artwork_img:
        uploaded_image = cloudinary.uploader.upload(artwork_img)
        image_url = uploaded_image['url']
    else:
        # get the existing image from the database
        db_cursor.execute("SELECT img_url FROM artworks WHERE id = %s", (artwork_id,))
        image_url = db_cursor.fetchone()

    # updates artwork details from the form in the database
    db_cursor.execute("UPDATE artworks SET title = %s, description = %s, img_url = %s WHERE id = %s", (
    artwork_title, artwork_description , image_url , artwork_id))

    db_connection.commit()
    db_cursor.close()
    db_connection.close()

    return redirect('/my_artworks')


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if 'user_id' not in session:
        return redirect('/login')
    # gets id and title from query parameter
    if request.method == 'GET':
        artwork_id = request.args.get('id')
        artwork_title = request.args.get('title')

        return render_template("delete_artwork.html", artwork_id = artwork_id, artwork_title=artwork_title, user_name = session.get('user_name'))

    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()

    artwork_id = request.form['id']
    # deletes the artwork where id is the form id
    db_cursor.execute("DELETE FROM artworks WHERE id = %s", [artwork_id])
    
    db_connection.commit()
    db_cursor.close()
    db_connection.close()

    return redirect('/my_artworks') 



@app.route('/create', methods=['GET', 'POST'])
def create_artwork():
    if 'user_id' not in session:
        return redirect('/login')
        
    if request.method == 'GET':
        return render_template('add_artwork.html', user_name = session.get('user_name'))

    if not request.files.get('img'):
        return render_template('add_artwork.html', error='No image file was selected', user_name = session.get('user_name') )
    
    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()

    title = request.form['title']
    description = request.form['description']
    img = request.files.get('img')
    user_id = session['user_id']

    uploaded_image = cloudinary.uploader.upload(img)
    image_url = uploaded_image['url']

    # add artwork to the artworks table
    db_cursor.execute('INSERT INTO artworks (title, description, img_url, user_id) VALUES (%s, %s, %s, %s)',
    (title, description, image_url, user_id))
    
    db_connection.commit()
    db_cursor.close()
    db_connection.close()

        
    return redirect('/my_artworks')


@app.route('/')
def index():
    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()
    # select all the artworks and their user names from the database
    db_cursor.execute("SELECT artworks.id, artworks.title, artworks.description, artworks.img_url, artworks.user_id, users.name FROM artworks JOIN users ON artworks.user_id = users.id;")
    rows = db_cursor.fetchall()
    art_items = []
    for row in rows:
        art_items.append(
            {
               "id": row[0],
                "title": row[1],
                "description": row[2],
                "img_url": row[3],
                "user_id": row[4],
                "name": row[5]
            }
        )

    db_cursor.close()
    db_connection.close()
    
    return render_template("home.html", art_items=art_items, user_name = session.get('user_name'))

if __name__ == "__main__":
    app.run(debug = True)
