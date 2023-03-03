TRUNCATE TABLE artworks CASCADE;
TRUNCATE TABLE users CASCADE;

ALTER SEQUENCE artworks_id_seq RESTART WITH 1;
ALTER SEQUENCE users_id_seq RESTART WITH 1;

INSERT INTO users (name, email) VALUES ('Tania', 'taniah@gmail.com');
INSERT INTO users (name, email) VALUES ('Bob the builder','bob@acme.com');


INSERT INTO artworks(title, description, file_img, user_id) VALUES ('The Girl', 'The painting depicts two young girls sitting down and laughing together, their faces full of joy and merriment. They are both dressed in colorful dresses that add a playful and lively atmosphere to the scene. One girl has her hand over her mouth, as if trying to stifle her laughter, while the other girl throws her head back in a carefree manner, her laughter ringing out loud and clear.', '', 1 );
INSERT INTO artworks(title, description, file_img, user_id) VALUES ('Starry Night', 'The painting "The Starry Night" by Vincent van Gogh is an iconic masterpiece of post-impressionist art. In this particular interpretation, a student stands in front of the painting, with his back to the viewer, gazing up at the swirling night sky depicted in the painting.', '', 2);
INSERT INTO artworks(title, description, file_img, user_id) VALUES ('River', 'The drawing depicts a peaceful river winding its way through a lush landscape, with several bridges spanning its width at different points. The artist has expertly captured the serene and tranquil atmosphere of the scene, with soft lines and delicate shading creating a sense of calmness and serenity.', '', 1);



