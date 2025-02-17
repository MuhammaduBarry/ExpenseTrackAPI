from flask import Flask

from app.routers.routes import routes

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Register routes
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)