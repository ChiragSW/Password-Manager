from flask import Flask, render_template, request, redirect, jsonify, session
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')  # Required for session handling

# Database initialization
def init_db():
    with sqlite3.connect("password_manager.db") as conn:
        cursor = conn.cursor()
        # Create users table for master passwords
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password TEXT NOT NULL UNIQUE
        )
        """)
        # Create passwords table linked to user_id
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            website TEXT NOT NULL,
            password TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)
        conn.commit()

init_db()

@app.route("/")
def home():
    return redirect("/master")

# Master Password Setup and Validation
@app.route("/master", methods=["GET", "POST"])
def master():
    with sqlite3.connect("password_manager.db") as conn:
        cursor = conn.cursor()

        if request.method == "POST":
            master_password = request.form.get("master_password")
            if not master_password:
                return "Master password cannot be empty!", 400

            # Check if the master password already exists
            cursor.execute("SELECT id, password FROM users")
            users = cursor.fetchall()

            for user_id, stored_password in users:
                if master_password == stored_password:  # Compare directly
                    # Login with the existing master password
                    session["authenticated"] = True
                    session["user_id"] = user_id
                    return redirect("/index")

            # If not found, create a new master password
            try:
                cursor.execute("INSERT INTO users (password) VALUES (?)", (master_password,))
                conn.commit()
                session["authenticated"] = True
                session["user_id"] = cursor.lastrowid
                return redirect("/index")
            except sqlite3.Error as e:
                return f"Database error: {e}", 500

        return render_template("master.html")

# Index route for managing passwords
@app.route("/index", methods=["GET", "POST"])
def index():
    if not session.get("authenticated"):
        return redirect("/master")

    user_id = session.get("user_id")

    with sqlite3.connect("password_manager.db") as conn:
        cursor = conn.cursor()

        if request.method == "POST":
            website = request.form.get("website")
            password = request.form.get("password")
            try:
                cursor.execute("INSERT INTO passwords (user_id, website, password) VALUES (?, ?, ?)",
                               (user_id, website, password))
                conn.commit()
            except sqlite3.Error as e:
                return f"Database error: {e}", 500

        # Retrieve passwords for the logged-in user
        cursor.execute("SELECT id, website, password FROM passwords WHERE user_id = ?", (user_id,))
        passwords = cursor.fetchall()

    return render_template("index.html", passwords=passwords)

@app.route("/delete/<int:password_id>", methods=["POST"])
def delete_password(password_id):
    if not session.get("authenticated"):
        return redirect("/master")

    user_id = session.get("user_id")

    with sqlite3.connect("password_manager.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM passwords WHERE id = ? AND user_id = ?", (password_id, user_id))
            conn.commit()
        except sqlite3.Error as e:
            return f"Database error: {e}", 500

    return redirect("/index")

@app.route("/view/<int:password_id>", methods=["POST"])
def view_password(password_id):
    if not session.get("authenticated"):
        return redirect("/master")

    user_id = session.get("user_id")

    with sqlite3.connect("password_manager.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM passwords WHERE id = ? AND user_id = ?", (password_id, user_id))
        password = cursor.fetchone()

    if password:
        return jsonify({"password": password[0]})
    return "Password not found!", 404

@app.route("/logout")
def logout():
    session.clear()  # Clear the session data
    return redirect("/master")  # Redirect to the master password page

if __name__ == "__main__":
    app.run(debug=True)
