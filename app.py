from flask import Flask

from app.routers.routes import routes
from app.routers.auth import auth

app: Flask = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Register blueprints
app.register_blueprint(routes)
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(debug=True)
