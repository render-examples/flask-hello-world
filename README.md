# README

This is the [Flask](http://flask.pocoo.org/) [quick start](http://flask.pocoo.org/docs/1.0/quickstart/#a-minimal-application) example for [Render](https://render.com).

The app in this repo is deployed at [https://flask.onrender.com](https://flask.onrender.com).

## Deployment

Follow the guide at https://render.com/docs/deploy-flask.

## Running

`FLASK_DEBUG=1 flask run`

## Connecting to database 

To connect to the database it is necessary to set an .env file with the following variables: DB_USER_NAME, DB_PASSWORD, DB_ENDPOINT, DB_PORT, DB_NAME.

## Running update_db.py script 

It is necessary to set two different .env variables in order to run the update_db.py script:
- one with the chromedriver path;
- and another with the downloads directory path. 

