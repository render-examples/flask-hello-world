# README

This is the [Flask](http://flask.pocoo.org/) [quickstart example](http://flask.pocoo.org/docs/1.0/quickstart/#a-minimal-application) example for [Render](https://render.com).

The app in this repo is deployed at [https://flask.app.render.com](https://flask.app.render.com).

## Deployment
Create a new web service in Render with your version of this repo and the following values:
  * Build Command: `pip install -r requirements.txt`
  * Start Command: `gunicorn app:app`

That's it! Your web service will be live on your Render URL as soon as the build finishes.
