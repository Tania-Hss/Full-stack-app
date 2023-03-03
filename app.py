from flask import Flask, render_template
import psycopg2
app = Flask(__name__)

@app.route('/')
def index():
    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT id, title, description, file_img FROM artworks;")
    rows = db_cursor.fetchall()
    art_items = []
    for row in rows:
        art_items.append(
            {
               "id": row[0],
                "title": row[1],
                "description": row[2],
                "file_img": row[3]
            }
        )

    db_cursor.close()
    db_connection.close()
    
    return render_template("home.html", art_items=art_items)

if __name__ == "__main__":
    app.run(debug = True)


