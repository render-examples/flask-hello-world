# README

You'll need to make sure that you have Python >= 3.6 and virtualenv installed

pip3 install virtualenv
virtualenv -p python3 .env
source .env/bin/activate
pip3 install -r requirements.txt

gunicorn app:app

## Deployment

The app deploys on every push to master.  We do automatically make sure that the /ping route works before marking the deploy successful.
