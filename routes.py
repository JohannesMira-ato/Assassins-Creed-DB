from flask import Flask, render_template, request
import db

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("home.html")


@app.route('/database')
def database():
    return render_template('database.html')


# Page to route user to which table in database to add to
@app.route('/database/add')
def database_add():
    return render_template('database_add.html')


# Page to add to characters table
@app.route('/database/add/character')
def database_character_add():
    name = (request.args.get("character-name"))
    alias = (request.args.get("character-alias"))
    birthdate = (request.args.get("character-birthdate"))
    deathdate = (request.args.get("character-deathdate"))
    gender = (request.args.get("character-gender"))
    affiliation = (request.args.get("character-affiliation"))
    description = (request.args.get("character-description"))
    image = (request.args.get("character-image"))
    profile_image = (request.args.get("character-profileimage"))
    db.add_character(name, alias, birthdate, deathdate, gender,
                     affiliation, description, image, profile_image)
    return render_template("database_character_add.html")


# Page for individual assassins
@app.route('/assassin/<int:id>')
def assassin(id):
    assassin = db.fetch('SELECT * FROM Character WHERE CharacterID = ?', "one",
                        (id,))
    return render_template('character.html', assassin=assassin)


# Page for all assassins
@app.route('/all_assassins')
def all_assassins():
    assassins = db.fetch('SELECT * FROM Character ORDER BY CharacterID;',
                         "all")
    return render_template('all_characters.html', assassins=assassins)


# Page for all Weapons
@app.route('/all_weapons')
def all_weapons():
    weapons = db.fetch('SELECT * FROM Weapon ORDER BY WeaponID;', "all")
    return render_template('all_weapons.html', weapons=weapons)


# Page for individual weapons
@app.route('/weapon/<int:id>')
def weapon(id):
    # TODO make from conn =, to assassin =, a single function
    weapon = db.fetch('SELECT * FROM Weapon WHERE WeaponID = ?', "one", (id,))
    return render_template('weapon.html', weapon=weapon)


# Page for all Games
@app.route('/all_games')
def all_games():
    # TODO make from conn =, to assassin =, a single function
    games = db.fetch('SELECT * FROM Game ORDER BY GameID;', "all")
    return render_template('all_games.html', games=games)


# Page for individual weapons
@app.route('/game/<int:id>')
def game(id):
    game = db.fetch("SELECT * FROM Game WHERE GameID = ?", "one", (id,))
    return render_template('game.html', game=game)


if __name__ == "__main__":
    app.run(debug=True)  # MUST BE FINAL LINE
