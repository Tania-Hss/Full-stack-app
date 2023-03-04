from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)


@app.post('/edit_artwork_action')
def edit_artwork():
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


@app.route('/edit')
def edit():
    artwork_id = request.args.get('id')
    artwork_title = request.args.get('title')
    artwork_description = request.args.get('description')
    artwork_img = request.args.get('img')
    
    return render_template("edit_artwork.html", artwork_id=artwork_id,artwork_title=artwork_title,artwork_description=artwork_description,artwork_img=artwork_img)

@app.post('/delete_artwork_action')
def delete_artwork():
    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()

    artwork_id = request.form['id']
    
    db_cursor.execute("DELETE FROM artworks WHERE id = %s", [artwork_id])
    
    db_connection.commit()
    db_cursor.close()
    db_connection.close()

    return redirect('/')

@app.route('/delete')
def delete():
    artwork_id = request.args.get('id')
    artwork_title = request.args.get('title')
    
    return render_template("delete_artwork.html", artwork_id = artwork_id, artwork_title=artwork_title)



@app.post('/add_artwork')
def create_artwork():
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


@app.route('/create')
def create():
    return render_template('add_artwork.html')


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
    
    return render_template("home.html", art_items=art_items)

if __name__ == "__main__":
    app.run(debug = True)


