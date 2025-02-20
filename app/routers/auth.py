from flask import Blueprint, request, jsonify, render_template, session, current_app, redirect, url_for
import jwt
from datetime import datetime, timedelta
from functools import wraps

# Auth Blueprint to handle user authentication
auth: Blueprint = Blueprint("auth", __name__)

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get("token")
        if not token:
            return redirect(url_for("auth.login"))

        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"])
        except Exception as e:
            return jsonify({"Alert!": "Invalid token"})

    return decorated

@auth.route("/app")
@token_required  # Protecting the /app route with JWT authentication
def verify_user():
    """
    Checks if the user is logged in.

    If the user is not logged in (`session["logged_in"]` is False or missing),
    renders the login page. If the user is logged in, a confirmation message is returned.

    Authentication is handled via JWT, which verifies the user in a session when a
    POST request is sent from the login form.

    Once a user is authenticated, they are logged into the system via JWT instead of using cookies.
    The authentication token is typically sent in the request headers rather than stored in cookies.
    Verification is done by extracting the token from the request, validating it, and returning a
    confirmation message upon successful authentication.

    :return: str or rendered template
    """
    if not session.get("logged_in"):
        return render_template("login.html")

    return "Logged in currently"

@auth.route("/login", methods=["POST"])
def login():
    """
    Handles user login. Checks if the provided username and password are correct,
    and if so, logs the user in by setting a session and returning a JWT token.

    If the user credentials are correct, a JWT token is generated that contains the
    username and an expiration time. This token is then returned to the client,
    which can use it to authenticate future requests.

    :return: JSON response with the JWT token or error message.
    """

    # Get username and password from the form submission.
    username = request.form.get("username")
    password = request.form.get("password")

    # Verify if the username and password match the hardcoded values (for demonstration).
    if username and password == "123456":
        # If credentials are correct, log the user in by setting session["logged_in"] to True.
        session["logged_in"] = True  # User is now logged in.

        # Create a JWT token with the user's username and an expiration time.
        token = jwt.encode(
            {
                "user": username,  # Store the username inside the token payload.
                "expiration": str(datetime.utcnow() + timedelta(seconds=120))  # Token expires in 2 minutes.
            },
            current_app.config["SECRET_KEY"],  # Use the app's secret key to sign the JWT token.
            algorithm="HS256"  # The algorithm to use for signing the token (HMAC SHA256).
        )

        # Return the JWT token as a JSON response.
        return jsonify({"token": token})  # Return the token to the client.

    # If credentials are incorrect, return an error message with HTTP status 401 (Unauthorized).
    return jsonify({"message": "Invalid credentials"}), 401