
from flask import Flask, render_template, session, abort, redirect, url_for, request
import pathlib,os
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import requests


app = Flask("Studsight")
app.secret_key = "davidneastudsightkey.com"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
GOOGLE_CLIENT_ID = "771970138692-gjilmd2o08eitr81o07oiuhfe7m5ardh.apps.googleusercontent.com"

# Example initialization (update with your actual client secrets file and scopes)
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
        "https://www.googleapis.com/auth/user.phonenumbers.read",
        "https://www.googleapis.com/auth/user.gender.read",
        "https://www.googleapis.com/auth/user.birthday.read"
    ],
    redirect_uri="https://nea-studsight.onrender.com/callback"
    
    )


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            abort(401) # Authorisation required
        else:
            return function()
        
    return wrapper




@app.route("/login") # Login route
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback") # Callback route
def callback():
    flow.fetch_token(authorization_response=request.url)
    if not  session["state"] == request.args["state"]:
        abort(500)  # State does  not match!+
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    # Optionally, store info in session for later use
    session["google_id"] = id_info.get("sub")
    session["email"] = id_info.get("email")
    # Return account info as JSON for direct feedback
    from flask import jsonify
    return jsonify({
        "id": id_info.get("sub"),
        "email": id_info.get("email"),
        "name": id_info.get("name"),
        "picture": id_info.get("picture"),
        "locale": id_info.get("locale"),
        "hd": id_info.get("hd"),
        "phone_number": id_info.get("phone_number"),
        "gender": id_info.get("gender"),
        "birthday": id_info.get("birthday")
    })



# @app.route("/callback")
# def callback():
#     flow.fetch_token(authorization_response=request.url)
#     if not session["state"] == request.args["state"]:
#         abort(500)
#     credentials = flow.credentials
#     request_session = requests.session()
#     cached_session = cachecontrol.CacheControl(request_session)
#     token_request = google.auth.transport.requests.Request(session=cached_session)
#     id_info = id_token.verify_oauth2_token(
#         id_token=credentials._id_token,
#         request=token_request,
#         audience=GOOGLE_CLIENT_ID
#     )
#     session["google_id"] = id_info.get("sub")
#     session["email"] = id_info.get("email")
#     return redirect("/protected_area")


@app.route("/logout") # Logout route
def logout():
    session.clear()
    return redirect("/")


@app.route("/") # Home route
def home():
    return render_template("home.html")


@app.route("/protected_area")
@login_is_required
def protected_area():
    return render_template("protected_area.html", email=session["google_id"])


if __name__ == "__main__": # Run the app
    app.run(debug=True)
