# My Mood Diary Full Stack Application

## **Description**

**\- Purpose**
The purpose of this application is to track the thoughts, problem areas and skills for clients who see a psychologist for various issues. The range of issues can include mental health, drug and alcohol addictions, food disorders etc. This application will allow the users (clients) to journal their thoughts and track their problem areas and skills in conjunction with a psychologist who will assist in the implementation of the app for their clients.

Behavioural activation is engaging in positive activities to boost mood. This is a therapeutic strategy for treating depression. Part of this strategy needs you to monitor your daily activities and systematically schedule in activities throughout your day. For more information: https://www.psychologytools.com/self-help/behavioral-activation/

Thoughts, emotions and behaviours are all intertwined whereby negative thoughts can trigger negative behaviours. A more holistic approach is usually implemented by tracking these three areas i.e. negative thoughts, general mood ratings and problem behaviours.

Tracking mood, thoughts and behaviours has been shown to increase insight, motivation and willingness to change. Skills are designed at the individual level to replace the negative moods, thoughts and behaviours. 

The journal entries are for clients to track mood, thoughts and behaviours. A psychologist with the client then analyses these entries, identifies problem areas and then creates skills to combat these problem areas. A more complete example can be found in the user stories and personas.

**\- Functionality / features**

1. User authentication including sign up, log in, changing password on profile page
2. Mood tracking through journal entries (CRUD resources for adding/updating/deleting/reading journal entries)
3. Problem area tracking  (CRUD resources for adding/updating/deleting/reading problem areas)
4. Skills tracking (CRUD resources for adding/updating/deleting/reading skills)
5. Adding psychologist details on profile page

Each of these features are tested and recorded on this spreadsheet.

 [Manual User Testing on Development site locally](docs/User_Testing_Dev.xlsx)

[Manual User Testing on Production site deployed on AWS](docs/User_Testing_Prod.xlsx)

**\- Target audience**

The target audience is clients who see a psychologist for any issue from addiction to mental health issues. It can also be used as a tool for psychologists to help treat their clients more effectively.

**\- Tech stack**

My tech stack includes:

PostgreSQL database in AWS RDS
Python Flask with Jinja2 templates
HTML/CSS in Jinja2 templates
AWS ECS and ECR for deployment (see cloud architecture diagram below)
Docker to create images of Flask App

## **Running the app locally**

Below are instructions to run the app locally, with docker and with docker-compose.

To run this app locally on Ubuntu 20.04 LTS without docker:

1. Update repositories on Ubuntu: `sudo apt-get update`

2. Clone GitHub repository: `git clone https://github.com/PandelisT/my_mood_diary_fullstack`

3. Install python virtual environment: `sudo apt-get install python3.8-venv`

4. Create virtual environment: `python3.8 -m venv venv`

5. Activate the virtual environment `source venv/bin/activate`

6. Install pip: `python -m pip install --upgrade pip`

7. Install modules from src/requirements.txt: `pip install -r requirements.txt`

8. In main.py file, set MIGRATION_DIR = os.path.join('src', 'migrations')

9. Create a .env file and insert variables in the file:

   POSTGRES_PASSWORD=
   POSTGRES_DB=
   DB_URI=
   FLASK_APP=
   FLASK_ENV=
   DB_USER=
   DB_PASSWORD=
   DB_HOST
   DB_NAME=
   DB_NAME_TEST=
   JWT_SECRET_KEY=
   AWS_ACCESS_KEY_ID=1
   AWS_SECRET_ACCESS_KEY=1
   AWS_S3_BUCKET=1

   for e.g. FLASK_APP=src/main.py, FLASK_ENV=development, AWS_ACCESS_KEY_ID=1, AWS_SECRET_ACCESS_KEY=1, AWS_S3_BUCKET=1. The app will NOT work if these variables are not set.

10. Create PostgreSQL database and add details to .env file:

    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_HOST=localhost:5432
    DB_NAME=mood_diary_flask

11. `flask db-custom drop` (If there are any tables in the database previously)

12. `flask db upgrade` (to add the tables in the migrations directory)

13. `flask run` and access the app at `localhost:5000`


~~~python
**Important: in the default_settings.py make sure that the settings are correct:**

```python
class DevelopmentConfig(Config):
    DEBUG = True
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # DB_URI for local development
        value = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
        
        # DB_URI for Docker Containers
        value =  f"{os.getenv('DB_URI')}"

        if not value:
            raise ValueError("DB_URI is not set")

        return value
```
~~~

**Docker, Dockerfile and docker-compose for creating containers**

Docker is an open source containerisation technology for building and containerising applications. This application can be run locally with docker and docker-compose and can also create docker images to be uploaded to Docker Hub or in this project to AWS ECR. To create an image for this application, the Dockerfile is:

```dockerfile
FROM ubuntu:latest

RUN apt-get clean 

RUN apt-get update --fix-missing

RUN apt-get install python3.8 libpq-dev wait-for-it -y

WORKDIR /code

COPY src .

RUN apt-get install python3-pip -y

RUN pip3 install -r requirements.txt

ENV FLASK_APP=main:create_app

CMD ["gunicorn", "-b", "0.0.0.0", "-w", "3", "main:create_app()"]
```

Compose is a tool for defining and running multi-container Docker applications. With Compose, use a YAML file to configure the application’s services. Then, with a single command `docker-compose up`,  create and start all the services from your configuration.

https://docs.docker.com/engine/

https://docs.docker.com/compose/

**Create and Run Docker Containers locally**

1. In the .env file, update these environment variables for e.g.:

   FLASK_APP=main.py
   DB_URI=postgresql+psycopg2://postgres:banana@flask_postgres/flask_app
   where `postgres` is the user, `banana` is the password, `flask_postgres` is the container and `flask_app` is the database name

2. In main.py file, set MIGRATION_DIR = os.path.join('.', 'migrations')

3. Build the Docker Image:

   `docker build --tag mood_app_main .`

4. Create a bridge network for the flask app and the postgres database:
   `docker network create --driver bridge flask_network`

5. Run the flask app:
   `docker run -d  -p 5000:5000 --name test_mood_container --mount type=bind,src=/home/pandelis/projects/flask_auth_scotch/src,dst=/code  --network flask_network  --env FLASK_ENV=development  --env DB_URI=postgresql+psycopg2://postgres:banana@flask_postgres/flask_app  --env AWS_ACCESS_KEY_ID=1  --env AWS_SECRET_ACCESS_KEY=1  --env AWS_S3_BUCKET=1  mood_app_main flask run -h 0.0.0.0`

6. Run the postgres container:
   `docker run -d --name flask_postgres --env POSTGRES_PASSWORD=banana --env POSTGRES_DB=flask_app --mount type=volume,src=flask_postgres_data,dst=/var/lib/postgresql/data --network flask_network postgres`

7. Run the migrations in the container:
   `docker exec test_mood_container flask db upgrade`

8. If the migrations do not work, connect to the container:
   `docker exec -it test_mood_container /bin/bash`

   and run:
   `flask db-custom drop`
   `flask db upgrade`

To remove all the containers and resources:

1. Get docker container IDs by running `docker ps -a`
2. Run `docker stop <container-ID>`
3. Run `docker rm <container-ID>`
4. Run `docker network rm flask_network`

**To run the application using docker-compose.yml**

1. Build the Docker Image:

   `docker build --tag mood_app_main .`

2. To run the app using docker-compose, run:
   `docker-compose up`

3. To tear down, run:
   `docker-compose down -v `
   (-v removes the volumes as well)

## **Automatic Testing**

To run automatic tests using unittest,

1. Run `export FLASK_ENV=testing` in terminal to change the environment
2. Make sure Postgresql service is running by running command `sudo systemctl start postgresql`
3. The testing database has a different URI: `DB_NAME_TEST` different to the development database as described in the `default_settings.py` file, so you need to run:

`flask db-custom drop` (If there are any tables in the test database previously)
`flask db upgrade` (to add the tables in the migrations directory)
`flask db-custom seed` (to seed the test database to run the tests)

3. To run the tests, run`cd src` and run `python -m unittest discover tests/`

## **Code coverage**

To run the coverage module for the unittests in this application, change the environment to `testing` and then run `coverage run -m unittest discover tests/`

To get the report for the test coverage, run `coverage report -m`

Test coverage at the time of writing is 44%.

## **Code quality using flake8**

 Run `flake8 models controllers forms tests commands.py default_settings.py main.py` to view styling and other Python errors such as redundant imports.