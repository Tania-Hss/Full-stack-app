TRUNCATE TABLE artworks CASCADE;
TRUNCATE TABLE users CASCADE;

ALTER SEQUENCE artworks_id_seq RESTART WITH 1;
ALTER SEQUENCE users_id_seq RESTART WITH 1;

INSERT INTO users (name, email) VALUES ('Tania', 'taniah@gmail.com');
INSERT INTO users (name, email) VALUES ('Bob the builder','bob@acme.com');


INSERT INTO artworks(title, description, file_img, user_id) VALUES ('The Girl', 'The painting depicts two young girls sitting down and laughing together, their faces full of joy and merriment. They are both dressed in colorful dresses that add a playful and lively atmosphere to the scene. One girl has her hand over her mouth, as if trying to stifle her laughter, while the other girl throws her head back in a carefree manner, her laughter ringing out loud and clear.', 'https://images.unsplash.com/photo-1505377059067-e285a7bac49b?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1752&q=80', 1 );
INSERT INTO artworks(title, description, file_img, user_id) VALUES ('Starry Night', 'The painting "The Starry Night" by Vincent van Gogh is an iconic masterpiece of post-impressionist art. In this particular interpretation, a student stands in front of the painting, with his back to the viewer, gazing up at the swirling night sky depicted in the painting.', 'https://images.unsplash.com/photo-1618481187866-5c7b6b9b5431?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1740&q=80', 2);
INSERT INTO artworks(title, description, file_img, user_id) VALUES ('River', 'The drawing depicts a peaceful river winding its way through a lush landscape, with several bridges spanning its width at different points. The artist has expertly captured the serene and tranquil atmosphere of the scene, with soft lines and delicate shading creating a sense of calmness and serenity.', 'https://images.unsplash.com/photo-1579541637431-4e3cd6f6c9e3?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1546&q=80', 1);



