from typing import Callable, Optional, Any
from flask import Blueprint, request, jsonify, render_template, session, current_app, redirect, url_for, make_response, \
    Response
import jwt
from datetime import datetime, timedelta
from functools import wraps

from werkzeug import Response

from app.routers.users import get_user, check_password

# Auth Blueprint to handle user authentication
auth: Blueprint = Blueprint("auth", __name__)


def token_required(func: Callable[..., Any]) -> Callable[..., Response]:
    """
    Decorator to ensure that the route is protected by JWT authentication.
    If no token is provided or the token is invalid, it redirects the user to the login page.
    """

    @wraps(func)
    def decorated(*args: Any, **kwargs: Any) -> Response | tuple[Response, int] | Response:
        # Get the token from the Authorization header
        token: Optional[str] = request.headers.get("Authorization") or request.cookies.get("auth_token")

        # If no token is provided, redirect to the login page
        if not token:
            return redirect(url_for("auth.login"))

        try:
            # If the token is in 'Bearer <token>' format, extract the token
            token: str = token.split(" ")[1] if "Bearer " in token else token

            # Decode the token using the app's secret key and check for expiration
            payload: Any = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            expiration_time: datetime = datetime.strptime(payload["expiration"], "%Y-%m-%d %H:%M:%S.%f")

            # If the token has expired, return it to the log in page
            if expiration_time < datetime.now():
                return redirect(url_for("auth.login"))

        except Exception as e:
            # If decoding fails (e.g., invalid token), return an error
            return jsonify({"Alert!": "Invalid token", "error": str(e)}), 401

        # If the token is valid, refresh it by issuing a new token with updated expiration time
        new_token: str = jwt.encode(
            {
                "user": payload["user"],  # Retain the username in the new token
                "expiration": str(datetime.now() + timedelta(seconds=120))  # Extend expiration by 2 minutes
            },
            current_app.config["SECRET_KEY"],  # Use the app's secret key to sign the token
            algorithm="HS256"  # Specify the algorithm used for signing the token
        )

        # Execute the protected route function and add the new token to the response headers
        response: Response = make_response(func(*args, **kwargs))
        response.set_cookie("auth_token", new_token)  # Update token in cookie
        return response

    return decorated


@auth.route("/app", methods=["GET", "POST"])
@token_required  # Protecting the /app route with JWT authentication
def verify_user() -> Response | str:
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
    if request.method == "POST":
        response = make_response(redirect(url_for("auth.login")))
        response.delete_cookie("jwt") # deletes log in session
        session["logged_in"] = False # flags the current session
        return response

    if not session.get("logged_in"):
        # If the user is not logged in (session["logged_in"] is False or missing), redirect to login page
        return redirect(url_for("auth.login"))


    return render_template("app.html")


@auth.route("/login", methods=["POST"])
def login() -> tuple[Response, int] | Response:
    """
    Handles user login. Checks if the provided username and password are correct,
    and if so, logs the user in by setting a session and returning a JWT token.

    If the user credentials are correct, a JWT token is generated that contains the
    username and an expiration time. This token is then returned to the client,
    which can use it to authenticate future requests.

    :return: JSON response with the JWT token or error message.
    """
    # Get username and password from our request
    username: str = request.form.get("username")
    password: str = request.form.get("password")

    # Retrieve user data from database
    # get_user(username) handles fail-safe
    if get_user(username) is None:
        # If user is None, return a JSON response with a message
        return jsonify({"msg": "User does not exist, please create an account.", "url": "http://127.0.0.1:5000/signup"}), 401

    user, hashed_password = get_user(username)

    # Verify if the username and password match the hardcoded values (for demonstration).
    if check_password(password, hashed_password):
        # If credentials are correct, log the user in by setting session["logged_in"] to True.
        session["logged_in"] = True  # User is now logged in.

        # Create a JWT token with the user's username and an expiration time.
        token: str = jwt.encode(
            {
                "user": username,  # Store the username inside the token payload.
                "expiration": str(datetime.now() + timedelta(seconds=120))  # Token expires in 2 minutes.
            },
            current_app.config["SECRET_KEY"],  # Use the app's secret key to sign the JWT token.
            algorithm="HS256"  # The algorithm to use for signing the token (HMAC SHA256).
        )

        # If the user is authenticated then it works
        response: Response = redirect(url_for("auth.verify_user"))
        response.set_cookie("auth_token", token)  # Store JWT in a cookie
        return response

    # If credentials are incorrect, return an error message with HTTP status 401 (Unauthorized).
    return jsonify({"message": "Invalid credentials"}), 401
