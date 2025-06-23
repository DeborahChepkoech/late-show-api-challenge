# Setup Instructions
Prerequisites
Python 3.8+
PostgreSQL database server installed and running.
Git (for cloning the repository)
1. Clone the Repository
git clone <git@github.com:DeborahChepkoech/late-show-api-challenge.git>
cd late-show-api-challenge 
2. Set up Virtual Environment and Dependencies
pipenv install flask flask_sqlalchemy flask_migrate flask-jwt-extended psycopg2-binary 
pipenv shell

3. PostgreSQL Database Setup
You need to create a dedicated user and database for your application in PostgreSQL.

Connect to PostgreSQL as a superuser (e.g., postgres):
sudo -u postgres psql
Inside the psql prompt, create the user and database:
(Replace your_secure_password_here with a strong password you choose)

CREATE USER late_show_db_yasm_user WITH PASSWORD 'your_secure_password_here';
CREATE DATABASE late_show_db_yasm OWNER late_show_db_yasm_user;
GRANT ALL PRIVILEGES ON DATABASE late_show_db_yasm TO late_show_db_yasm_user;
\q
4. Environment Variables


Navigate to your project root:
cd /path/to/your/late-show-api-challenge 
export PYTHONPATH=$(pwd)
export FLASK_APP=server/app.py
export JWT_SECRET_KEY="a-very-secret-key-that-you-should-change-in-prod" 
export JWT_ACCESS_TOKEN_EXPIRES=3600 # Token valid for 1 hour
export DATABASE_URI="postgresql://late_show_db_yasm_user:your_secure_password_here@localhost:5432/late_show_db_yasm"
Important: Replace your_secure_password_here with the exact password you set for the PostgreSQL user.

# How to Run the Application
1. Database Migrations
Initialize and apply database migrations to create your tables.
flask db init      
flask db migrate -m "Initial migration" 
flask db upgrade   
2. Seeding the Database
Populate your database with initial data (users, guests, episodes, appearances) for testing.
python server/seed.py
3. Running the Flask Application
flask run
The API will typically be accessible at http://localhost:5000.

# Authentication Flow
This API uses JWTs for authentication on protected routes.
Register: Send a POST request to /api/auth/register with a username and password.
Example Request Body: {"username": "myuser", "password": "mypassword"}
Login: Send a POST request to /api/auth/login with the registered username and password.
Example Request Body: {"username": "myuser", "password": "mypassword"}
The response will contain an access_token. Copy this token.
Use Token: For protected routes, include the access_token in the Authorization header in the format Authorization: Bearer <your_access_token>.
API Endpoints
All routes are prefixed with /api. Base URL: http://localhost:5000/api

Route	Method	Auth Required?	Description	Sample Request Body (if applicable)	Sample Response (Success)
/auth/register	POST	❌	Register a new user.	{ "username": "newuser", "password": "securepass" }	{ "msg": "User registered successfully" }
/auth/login	POST	❌	Log in a user and return a JWT token.	{ "username": "newuser", "password": "securepass" }	{ "access_token": "eyJ..." }
/episodes	GET	❌	Get a list of all episodes.	(None)	[ { "id": 1, "date": "...", "number": 1001, "appearances": [...] } ]
/episodes/<int:id>	GET	❌	Get a single episode by ID with its appearances.	(None)	{ "id": 1, "date": "...", "number": 1001, "appearances": [...] }
/episodes/<int:id>	DELETE	✅	Delete an episode and its associated appearances.	(None)	{ "msg": "Episode X and its appearances deleted successfully" }
/guests	GET	❌	Get a list of all guests.	(None)	[ { "id": 1, "name": "...", "occupation": "..." } ]
/appearances	POST	✅	Create a new appearance.	{ "rating": 4, "guest_id": 1, "episode_id": 1 }	{ "id": 1, "rating": 4, "guest_id": 1, "episode_id": 1 }

# Postman Usage Guide
A Postman collection with pre-configured requests can be found in challenge-4-lateshow.postman_collection.json (if provided). If not, you can easily create one manually:

Download and Install Postman.
Create a New Collection: Click the + button in the sidebar and select "New Collection." Give it a descriptive name like "Late Show API."
Add Requests: For each API endpoint listed above, click "Add Request" within your collection.
Set the HTTP Method (GET, POST, DELETE).
Enter the URL (e.g., http://localhost:5000/api/auth/register).
For POST requests, go to the "Body" tab, select raw and JSON, and paste your sample JSON request body.
For protected routes, go to the "Headers" tab and add a key Authorization with the value Bearer <your_jwt_token_here>. Remember to get a fresh token from the /api/auth/login endpoint after each login.
Save each request after configuring it.

# GitHub Repository
You can find the source code for this project on GitHub: 
https://github.com/DeborahChepkoech/late-show-api-challenge#