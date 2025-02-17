from flask import render_template, Blueprint

# Create a Blueprint for routes enabling modularity
routes: Blueprint = Blueprint("routes", __name__)

@routes.route("/")
def landing_page() -> str:
    """
    Landing page
    :return: str
    """
    return render_template("index.html")

@routes.route("/login")
def login() -> str:
    """
    Login page
    :return: str
    """
    return render_template("login.html")

@routes.route("/signup")
def singup() -> str:
    """
    Signup page
    :return: str
    """
    return render_template("signup.html")

@routes.route("/app")
def app() -> str:
    """
    App page
    :return: str
    """
    return render_template("app.html")
