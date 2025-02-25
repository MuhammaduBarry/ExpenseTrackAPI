from flask import Flask, Config

from app.routers.routes import routes
from app.routers.auth import auth
from app.routers.users import data
from app.routers.db import connect_db

app: Flask = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Register blueprints
app.register_blueprint(routes)
app.register_blueprint(auth)
app.register_blueprint(data)


# Secret key used for protecting session cookies and protect against tampering
# Ensures secure session management and CSRF(Cross Site Request Forgery) protection
app.config["SECRET_KEY"]: Config = "9cd2903d7107401abe897a8de517e218"

if __name__ == '__main__':
    app.run(debug=True)
