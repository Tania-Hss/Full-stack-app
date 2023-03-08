# import psycopg2
# from psycopg2.extras import RealDictCursor

# def get_all_artworks():
#     db_connection = psycopg2.connect("dbname=art_gallary")
#     db_cursor = db_connection.cursor()
#     # select all the artworks and their user names from the database
#     db_cursor.execute("SELECT artworks.id, artworks.title, artworks.description, artworks.img_url, artworks.user_id, users.name FROM artworks JOIN users ON artworks.user_id = users.id;")
#     rows = db_cursor.fetchall()
#     art_items = []
#     for row in rows:
#         art_items.append(
#             {
#                "id": row[0],
#                 "title": row[1],
#                 "description": row[2],
#                 "img_url": row[3],
#                 "user_id": row[4],
#                 "name": row[5]
#             }
#         )

#     db_cursor.close()
#     db_connection.close()
    
#     return art_items
