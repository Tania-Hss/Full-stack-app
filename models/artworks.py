import psycopg2
from psycopg2.extras import RealDictCursor
from cloudinary import CloudinaryImage
import cloudinary.uploader
from flask import session 

def get_all_artworks():
    conn = psycopg2.connect("dbname=art_gallary")
    cur = conn.cursor(cursor_factory=RealDictCursor)
    # select all the artworks and their user names from the database
    cur.execute("SELECT artworks.id, artworks.title, artworks.description, artworks.img_url, artworks.user_id, users.name FROM artworks JOIN users ON artworks.user_id = users.id;")
    rows = cur.fetchall()
    art_items = []
    for row in rows:
        art_items.append(
            {
               "id": row["id"],
                "title": row["title"],
                "description": row["description"],
                "img_url": row["img_url"],
                "user_id": row["user_id"],
                "name": row["name"]
            }
        )

    cur.close()
    conn.close()
    
    return art_items

def create_new_artwork(title, description, img, user_id):
    conn = psycopg2.connect("dbname=art_gallary")
    cur = conn.cursor()

    uploaded_image = cloudinary.uploader.upload(img)
    image_url = uploaded_image['url']
    # add artwork to the artworks table
    cur.execute('INSERT INTO artworks (title, description, img_url, user_id) VALUES (%s, %s, %s, %s)',
                       (title, description, image_url, user_id))

    conn.commit()
    cur.close()
    conn.close()

def delete_artwork(artwork_id):
    conn = psycopg2.connect("dbname=art_gallary")
    cur = conn.cursor()
    # deletes the artwork where id is the form id
    cur.execute("DELETE FROM artworks WHERE id = %s", [artwork_id])
    
    conn.commit()
    cur.close()
    conn.close()


def edit_artwork(artwork_id, artwork_title, artwork_description, artwork_img):
    conn = psycopg2.connect("dbname=art_gallary")
    cur = conn.cursor()
    # if image exits then upload to cloudinary 
    if artwork_img:
        uploaded_image = cloudinary.uploader.upload(artwork_img)
        image_url = uploaded_image['url']

        cur.execute("UPDATE artworks SET title = %s, description = %s, img_url = %s WHERE id = %s",
        (artwork_title, artwork_description, image_url, artwork_id))
    else:
        # get the existing image from the database
        cur.execute("UPDATE artworks SET title = %s, description = %s WHERE id = %s",
        (artwork_title, artwork_description, artwork_id))
    # updates artwork details from the form in the database

    conn.commit()
    cur.close()
    conn.close()


def get_user_artworks(user_id):
    conn = psycopg2.connect("dbname=art_gallary")
    cur = conn.cursor(cursor_factory=RealDictCursor)
    # select all the artworks from the database that belong to the user 
    cur.execute("SELECT artworks.id, artworks.title, artworks.description, artworks.img_url, artworks.user_id FROM artworks JOIN users ON artworks.user_id = users.id WHERE users.id = %s", [session['user_id']])
    rows = cur.fetchall()

    user_artwork = []
    for row in rows:
        user_artwork.append(
            {
                'id': row['id'],
                'title': row['title'],
                'description': row['description'],
                'img_url': row['img_url'],
                'user_id': row['user_id']
            }
        )

    cur.close()
    conn.close()

    return user_artwork
