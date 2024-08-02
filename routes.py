from flask import Flask, render_template, request
import db

app = Flask(__name__)
empty_query = None


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


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
    assassin = db.fetch('SELECT * FROM Character WHERE CharacterID = ?',
                        "one", (id,))
    if assassin == empty_query:
        return render_template('404.html')
    else:
        return render_template('character.html', assassin=assassin)


# Page for all assassins
@app.route('/all_assassins')
def all_assassins():
    assassins = db.fetch('''SELECT CharacterID, Name, ProfileImage FROM
                        Character WHERE Affiliation LIKE "%Assassin%";''',
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
    weapons = db.fetch('''SELECT Weapon.WeaponID,
                       Weapon.Name,
                       Character.CharacterID,
                       Character.Name,
                       Weapon.Description
                       FROM Weapon 
                       JOIN CharacterWeapon ON Weapon.WeaponID = CharacterWeapon.WeaponID 
                       JOIN Character ON CharacterWeapon.CharacterID = Character.CharacterID
                       WHERE Weapon.WeaponID = ?;''', 'all', (id,))
    if weapons == empty_query:
        return render_template('404.html')
    else:
        return render_template('weapon.html', weapons=weapons)


# Page for all Games
@app.route('/all_games')
def all_games():
    games = db.fetch('SELECT GameID, Title, Image FROM game;', "all")
    return render_template('all_games.html', games=games)


# Page for individual weapons
@app.route('/game/<int:id>')
def game(id):
    game = db.fetch('''SELECT 
                        Game.GameID,
                        Game.Title,
                        Game.ReleaseDate,
                        Game.Setting,
                        Game.Image,
                        Character.CharacterID,
                        Character.Name
                    FROM Game
                        JOIN CharacterGame ON Game.GameID = CharacterGame.GameID
                        JOIN Character ON CharacterGame.CharacterID = Character.CharacterID
                    WHERE Game.GameID = ?;''', "all", (id,))
    if game == empty_query:
        return render_template('404.html')
    else:
        return render_template('game.html', game=game)


if __name__ == "__main__":
    app.run(debug=True)  # MUST BE FINAL LINE
