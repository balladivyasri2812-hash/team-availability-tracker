from flask import Flask, render_template, redirect
import sqlite3

app = Flask(__name__)

def connect_db():

    conn = sqlite3.connect("team.db")
    conn.row_factory = sqlite3.Row

    return conn

def create_table():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            available INTEGER
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM team")

    count = cursor.fetchone()[0]

    if count == 0:

        members = [

            ("Alex Rivers", "Senior Developer", 1),
            ("Samantha Chen", "UX Designer", 0),
            ("Jordan Taylor", "Project Manager", 1),
            ("Maria Garcia", "Marketing Lead", 0)

        ]

        cursor.executemany("""
            INSERT INTO team(name, role, available)
            VALUES (?, ?, ?)
        """, members)

    conn.commit()
    conn.close()

@app.route("/")
def home():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM team")

    members = cursor.fetchall()

    conn.close()

    return render_template("index.html", members=members)

@app.route("/toggle/<int:id>")
def toggle(id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT available FROM team
        WHERE id=?
    """, (id,))

    member = cursor.fetchone()

    new_status = 0 if member["available"] == 1 else 1

    cursor.execute("""
        UPDATE team
        SET available=?
        WHERE id=?
    """, (new_status, id))

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":

    create_table()

    app.run(debug=True)