import psycopg2
from psycopg2.extras import RealDictCursor
from cloudinary import CloudinaryImage
import cloudinary.uploader


def get_all_artworks():
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
    
    return art_items

def create_new_artwork(title, description, img, user_id):
    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()

    uploaded_image = cloudinary.uploader.upload(img)
    image_url = uploaded_image['url']
    # add artwork to the artworks table
    db_cursor.execute('INSERT INTO artworks (title, description, img_url, user_id) VALUES (%s, %s, %s, %s)',
                       (title, description, image_url, user_id))

    db_connection.commit()
    db_cursor.close()
    db_connection.close()

    return

def delete_artwork(artwork_id):
    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()
    # deletes the artwork where id is the form id
    db_cursor.execute("DELETE FROM artworks WHERE id = %s", [artwork_id])
    
    db_connection.commit()
    db_cursor.close()
    db_connection.close()

def edit_artwork(artwork_id, artwork_title, artwork_description, artwork_img):
    db_connection = psycopg2.connect("dbname=art_gallary")
    db_cursor = db_connection.cursor()
    # if image exits then upload to cloudinary 
    if artwork_img:
        uploaded_image = cloudinary.uploader.upload(artwork_img)
        image_url = uploaded_image['url']
    else:
        # get the existing image from the database
        db_cursor.execute("SELECT img_url FROM artworks WHERE id = %s", (artwork_id,))
        image_url = db_cursor.fetchone()[0]
    # updates artwork details from the form in the database
    db_cursor.execute("UPDATE artworks SET title = %s, description = %s, img_url = %s WHERE id = %s",
                       (artwork_title, artwork_description, image_url, artwork_id))

    db_connection.commit()
    db_cursor.close()
    db_connection.close()
    