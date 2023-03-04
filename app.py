from flask import Flask, render_template, request, redirect
import psycopg2
app = Flask(__name__)




@app.post('/add_artwork')
def add_new_artwork():
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
def create_new_artwork():
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


