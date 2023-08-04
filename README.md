Overview

Forti-flask is a RESTful API service that provides several endpoints  for interacting with data. It is designed to be secure and utilizes JWT token-based authentication. The app is built with Python and Flask, using Pydantic for data validation, PostgreSQL for the database,  Nginx as a reverse proxy server and WSGI as web servers to forward requests to web application. The entire app is containerized using Docker for easy deployment and scalability.

Features

Secure JWT token-based authentication
RESTful APIs for data manipulation
Data validation using Pydantic,
Scalable and easily deployable with Docker and Docker Compose
Nginx as a reverse proxy for improved performance
WSGI as web server to forward requests to web application

Technologies Used
Python
Flask
Pydantic
PostgreSQL
Nginx
WSGI
Docker
Docker Compose

Getting Started
Prerequisites
Before running the app, ensure you have the following installed on your machine:

Docker
Docker Compose 

Running the App

Clone this repository to your local machine

The app is configured to work with .env. files,
you should provide them by yourself.
In FortiFlask folder create .env.prod and env.prod.db:

.env.prod content:

FLASK_APP=project/__init__.py
FLASK_DEBUG=0
DATABASE_URL=postgresql://your_postgres_username:your_postgres_password@db:5432/your_db_name
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
APP_FOLDER=/home/app/web
FLASK_SECRET_KEY=your_secret_key_here

.env.prod.db content:

POSTGRES_USER=your_postgres_username
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_postgres_db_name


Start the application using Docker Compose:
In FortiFlask folder run docker-compose -f docker-compose.prod.yml up -d --build
This command will build and start application containers in detached mode.


To create the tables in database in FortiFlask directory run:
docker-compose -f docker-compose.prod.yml exec web python manage.py create_db

You can check if the tables are created successfully by running:
docker-compose exec -f docker-compose.prod.yml db psql --username=your_postgres_username --dbname=your_postgres_db_name
In psql type \l to List the databases
type \dt to List the tables there should be two tables user and contacts

If you have permission problems with entrypoint.prod.sh in FortiFlask directory run: chmod +x services/web/entrypoint.prod.sh

API Documentation

Swagger documentation is available in http://localhost:1337


Continuous Integration and Continuous Deployment (CI/CD)

FortiFlask uses GitHub Actions for its CI/CD pipelines. The pipelines are configured to automatically build, push to repository, and deploy the application image  whenever changes are pushed to the main branch. The CI/CD process includes the following steps:
Generate build id for the image using env variable, GITHUB_SHA
Login to Docker Hub using docker/login-action@v2 action with two secrets.
Build, Tag and Push an image to the repository
Login and Deploy to Vm by using appleboy/ssh-action@master action




