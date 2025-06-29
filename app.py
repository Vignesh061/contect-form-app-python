from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database and table if not exist
def init_db():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 email TEXT NOT NULL,
                 message TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()  # call to create table

# Route: Contact form page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # Save data to database
        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()
        c.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
                  (name, email, message))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("index.html")

# Route: Admin page to view messages
@app.route("/admin")
def admin():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM contacts")
    messages = c.fetchall()
    conn.close()
    return render_template("admin.html", messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
