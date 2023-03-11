# Full-stack-app
Art Gallary Project #2 for GA Flex Course

This is a web application developed with flask.
Users will be able to create an account
upload, edit, delete their artworks and view 
artworks posted by other users.
Using PostgreSQL as a database and Werkzeug to generate and check password hashes.

# # Features
View all artworks on the home page as a guest or user.
Create an account with a name, email, and password.
Login to the account.
View your own artworks on a separate my collection page.
Upload a new artwork with an image, title, and description.
Edit an existing artwork by the logged in user.
Delete your artwork.


# # included files

app.py - contains the main code for the web application / routes
and functions for creating, editing, and deleting artwork, as well as signing up and logging in.

db.py - connecting to the PostgreSQL database and executing SQL queries for the models.

models / artworks.py and users.py
Python modules for handling database queries for artworks and users.

static - css for designing the overall look
templates - contains of html files handling the views.

# # Technical Requirements

- Have at least 2 tables (more if they make sense) – one of them should represent the people using your application (users).

- Include sign up/log in functionality (if it makes sense), with encrypted passwords & an authorization flow.

- Modify data in the database There should be ways for users to add/change some data in the database (it's ok if only admins can make changes).

- Have semantically clean HTML and CSS

- Be deployed online and accessible to the public

# # Set up 
```
python -m venv venv
source venv/bin/activate
pip install flask psycopg2 requests python-dotenv cloudinary 
```

# # Setting up the DB
```
createdb art_gallary
psql -d art_gallary < schema.sql
psql -d art_gallary < seed.sql
```

# # the approach taken
- sign up 
User can enter their name, email, and password. The app checks for name, email and password values existing in the form if either doesnt exist app sends a error to fill in the empty field otherwise adds the user's information to the database and redirects the user to the login page.

- login
User can enter their email and password, The app checks if the email exists in the database and if the password matches the hashed password in the database.
If the email and password match, the app logs the user in and saves the user's ID, name, and email in the session. Otherwise, the app redirects the user back to the login page and gives an error message that either email or password is wrong.

- home page

When a user goes to the home page, the app checks to see if the user is logged in. If the user is not logged in they are welcomed as a guest and can still view artworks on home page but dont have any access to other pages than the signup or login page. If user is logged in they are identified by the session and have access to all pages. 


- collection page 

When a user goes to their collection page, the app checks if the user is logged in. If the user is not logged in, the app redirects the user to the login page. If the user is logged in, the app gets all the artworks from the database that belong to the user and renders them on the page.

- add artwork page

the app renders a form for the user to enter the title, description, and image file of the artwork. When the user submits the form, the app checks for an existing img uploaded then adds the artwork to the database and redirects the user to the my_artworks page, otherwise gived an error to ensure an image is submitted

- edit page

the app gets the ID, title, description, and image file of the artwork from the database and renders them on the page. The user can edit any of these fields and submit the form to update the artwork in the database. if user uploades a new image the app uploads the image to cloudinary and gets the image url in which it uses to update all the info in the database otherwise only the title or description gets updated in the database.

- delete page 

the app gets the ID and title of the artwork from the database and renders them on the page. The user can confirm the deletion of their artwork and the app deletes the artwork from the database.

- log out 

When a user clicks logout button, the app removes the user's ID, name, and email from the session and redirects the user to the login page.
