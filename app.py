from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session
)
from werkzeug.security import generate_password_hash, check_password_hash
from cloudinary import CloudinaryImage
import cloudinary.uploader
# import psycopg2
# from psycopg2.extras import RealDictCursor

from models.artworks import get_all_artworks, insert_artwork, delete_artwork, edit_artwork, get_user_artwork
from models.users import get_user_by_email, insert_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'in ye raze'



@app.route('/my_artworks')
def my_artworks():
    # Check if user is logged in 
    if 'user_id' not in session:
        return redirect('/login')

    user_artwork = get_user_artwork(session['user_id'])

    return render_template('my_artworks.html', user_artwork = user_artwork , user_name = session.get('user_name'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # accesses the signup page
    if request.method == 'GET':
        return render_template('signup.html')
    # signup form is submitted and data from form is inserted into database
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    # check to see if email already in database
    exists = get_user_by_email(email)
    if exists:
        # if email already exists we pass error message
        error = 'Email already in use. Please use a different Email address.'
        return render_template('signup.html', error=error)
    # if email is new we define the password hash and insert (name, email, password_hash) in database
    password_hash = generate_password_hash(password)
    insert_user(name, email, password_hash)

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
    result = get_user_by_email(user_email)

    if result is None:
        # If the email does not exist, redirect with an error message
        return render_template('login.html', error='Invalid email or password')

    password_matches = check_password_hash(result[3], user_password)
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

        return render_template("edit_artwork.html", artwork_id=artwork_id, artwork_title=artwork_title,
        artwork_description=artwork_description, artwork_img=artwork_img,
        user_name=session.get('user_name'))

    edit_artwork(
        request.form['id'],
        request.form['title'],
        request.form['description'],
        request.files.get('img')
    )
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

    delete_artwork(
        request.form['id']
    )
    return redirect('/my_artworks') 


@app.route('/create', methods=['GET', 'POST'])
def create_artwork():
    if 'user_id' not in session:
        return redirect('/login')
        
    if request.method == 'GET':
        return render_template('add_artwork.html', user_name = session.get('user_name'))

    if not request.files.get('img'):
        return render_template('add_artwork.html', error='No image file was selected', user_name = session.get('user_name') )

    insert_artwork(
        request.form['title'],
        request.form['description'],
        request.files.get('img'),
        session['user_id']
    )
    return redirect('/my_artworks')


@app.route('/')
def index():
    art_items = get_all_artworks()
    return render_template("home.html", art_items=art_items, user_name = session.get('user_name'))

if __name__ == "__main__":
    app.run(debug = True)
