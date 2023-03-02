CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);


CREATE TABLE artworks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    description TEXT,
    image_url TEXT, 
    user_id INT,
    CONSTRAINT fk_artworks_users
        FOREIGN KEY(user_id)
        REFERENCES users(id)
);