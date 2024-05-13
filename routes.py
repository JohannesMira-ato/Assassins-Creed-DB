from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/about')
def about():
        return "about"

@app.route('/assassin/<int:id>')
def assassin(id):
    conn = sqlite3.connect('ACDB.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Character WHERE CharacterID = ?',(id,))
    assassin = cur.fetchone()
    return render_template('character.html', assassin = assassin)

@app.route('/all_assassins')
def all_assassins():
    conn = sqlite3.connect('ACDB.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Character ORDER BY Characterid;')
    assassin = cur.fetchall()
    return render_template('character.html', assassin = assassin)

if __name__ == "__main__":
    app.run(debug=True)  # MUST BE FINAL LINE