from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Homepage
@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/about')
def about():
        return "about"

@app.route('/database')
def database():
    return render_template('database.html')

# Page to add to characters table
@app.route('/database/character/add')
def database_character_add():
    return render_template("database_character_add.html")

# Page for individual assassins
@app.route('/assassin/<int:id>')
def assassin(id):
    # TODO make from conn =, to assassin =, a single function
    conn = sqlite3.connect('ACDB.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Character WHERE CharacterID = ?',(id,))
    assassin = cur.fetchone()
    return render_template('character.html', assassin=assassin)


# Page for all assassins 
@app.route('/all_assassins')
def all_assassins():
    # TODO make from conn =, to assassin =, a single function
    conn = sqlite3.connect('ACDB.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Character ORDER BY CharacterID;')
    assassins = cur.fetchall()
    return render_template('all_characters.html', assassins=assassins)

# Page for all Weapons
@app.route('/all_weapons')
def all_weapons():
    # TODO make from conn =, to assassin =, a single function
    conn = sqlite3.connect('ACDB.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Weapon ORDER BY WeaponID;')
    weapons = cur.fetchall()
    return render_template('all_weapons.html', weapons=weapons)

# Page for individual weapons
@app.route('/weapon/<int:id>')
def weapon(id):
    # TODO make from conn =, to assassin =, a single function
    conn = sqlite3.connect('ACDB.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Weapon WHERE WeaponID = ?',(id,))
    weapon = cur.fetchone()
    return render_template('weapon.html', weapon=weapon)

# Page for all Games
@app.route('/all_games')
def all_games():
    # TODO make from conn =, to assassin =, a single function
    conn = sqlite3.connect('ACDB.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Game ORDER BY GameID;')
    games = cur.fetchall()
    return render_template('all_games.html', games=games)

# Page for individual games
@app.route('/game/<int:id>')
def game(id):
    # TODO make from conn =, to assassin =, a single function
    conn = sqlite3.connect('ACDB.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Game WHERE GameID = ?',(id,))
    game = cur.fetchone()
    return render_template('game.html', game=game)


if __name__ == "__main__":
    app.run(debug=True)  # MUST BE FINAL LINE
