from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/about')
def about():
        return "about"

@app.route('/Assassin/<int:id>')
def assassin():
    return "Assassin"


if __name__ == "__main__":
    app.run(debug=True)  # MUST BE FINAL LINE