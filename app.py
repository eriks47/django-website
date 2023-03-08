from flask import Flask, redirect, url_for, render_template, request
import os
import psycopg2

HOSTNAME = "localhost"

def get_db_connection():
    conn = psycopg2.connect(
        host = HOSTNAME,
        database = "library_db",
        user = os.environ["DB_USERNAME"],
        password = os.environ["DB_PASSWORD"]
    )
    return conn


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/collections')
def collections():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM collections;")
    collections = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("collections.html", items=collections)

@app.route('/contribute/', methods=("GET", "POST"))
def contribute():
    if request.method == "POST":
        title = request.form["title"]
        books = request.form["books"]
        description = request.form["description"]
        alias = request.form["alias"]
        links = request.form["links"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO collections (title, books, description, likes, made_by, links)"
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (title, books, description, "0", alias, links))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("collections"))

    return render_template("contribute.html")

@app.route('/collections/<id>')
def specific_collection(id):
    return "<p>index page</p>"

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/submit')
def submit():
    return redirect(url_for("collections"))
