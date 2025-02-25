from flask import Blueprint, request, jsonify, render_template, session, current_app, redirect, url_for, make_response, Response
import sqlite3
import bcrypt

from app.routers.db import create_user_table, connect_db

data: Blueprint = Blueprint("data", __name__)

create_user_table()

@data.route("/signup", methods=["POST"])
def add_new_user():
    username = request.form.get("username")
    password = request.form.get("password")

    # To check if username or password was sent
    if not username or not password:
        return jsonify({"msg": "Username and/or password are not found"}), 400

    # Hashing password to store in db
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt).decode()

    # Storing new user's data
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

    return redirect(url_for("auth.login"))

def get_user(username: str):
    conn = connect_db()
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT username, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        return user
    except Exception as e:
        print(e)
    finally:
        conn.close()


def check_password(password, hashed_password):
    if bcrypt.checkpw(password.encode(), hashed_password.encode()):
        return True

    return False