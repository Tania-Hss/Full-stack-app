DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS artworks CASCADE;

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL
);


CREATE TABLE artworks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    description TEXT,
    img_url TEXT, 
    user_id INT,
    CONSTRAINT fk_artworks_users
        FOREIGN KEY(user_id)
        REFERENCES users(id)
);
