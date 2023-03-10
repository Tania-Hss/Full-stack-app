import psycopg2
from psycopg2.extras import RealDictCursor
from cloudinary import CloudinaryImage
import cloudinary.uploader
from flask import session 

import db


def get_all_artworks():
    rows = db.select_all("SELECT artworks.*, users.name FROM artworks JOIN users ON artworks.user_id = users.id")
    return rows


def insert_artwork(title, description, img, user_id):
    uploaded_image = cloudinary.uploader.upload(img)
    image_url = uploaded_image['url']

    db.insert(
        'INSERT INTO artworks (title, description, img_url, user_id) VALUES (%s, %s, %s, %s)',
        (title, description, image_url, user_id)
    )


def delete_artwork(artwork_id):
    # deletes the artwork where id is the form id
    db.delete("DELETE FROM artworks WHERE id = %s", [artwork_id])


def edit_artwork(artwork_id, artwork_title, artwork_description, artwork_img):
    # if image exits then upload to cloudinary 
    if artwork_img:
        uploaded_image = cloudinary.uploader.upload(artwork_img)
        image_url = uploaded_image['url']

        db.insert("UPDATE artworks SET title = %s, description = %s, img_url = %s WHERE id = %s",
        (artwork_title, artwork_description, image_url, artwork_id))
    else:
        db.insert("UPDATE artworks SET title = %s, description = %s WHERE id = %s",
        (artwork_title, artwork_description, artwork_id))
   


def get_user_artwork(user_id):
    rows = db.select_user_artwork("SELECT artworks.id, artworks.title, artworks.description, artworks.img_url, artworks.user_id FROM artworks JOIN users ON artworks.user_id = users.id WHERE users.id = %s", [user_id])
    return rows
