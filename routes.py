from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import db

app = Flask(__name__)
app.secret_key = "SHOCEKR"


# 404 error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Homepage
@app.route('/')
def homepage():
    return render_template("home.html")


# Register Page
@app.route('/register', methods=["GET", "POST"])
def register():
    # Form submission
    if request.method == "POST":
        # All user input
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        # Database setup
        conn = sqlite3.connect("Accounts.db")
        cur = conn.cursor()
        # Search for username matching user input username in db
        cur.execute(f"""SELECT Username FROM UserInfo
                    WHERE Username = '{username}';""")
        match = cur.fetchone()
        # If any of the input fields are empty
        if not username or not password or not confirm_password:
            flash("Please fill out all fields correctly")
            return redirect('/register')
        # If there is matching username in database
        if match:
            flash("Username already exists")
            return redirect('/register')
        # Passwords not matching
        if password != confirm_password:
            flash("Passwords do not match")
            return redirect('/register')
        cur.execute(f"INSERT INTO UserInfo (Username, Password)\
                     values ('{username}', '{password}')")
        conn.commit()
        conn.close()
        flash("Account Successfully Created!")
        return redirect('/login', code=302)
    return render_template("register.html")


# Login page
@app.route('/login', methods=["GET", "POST"])
def login():
    # Form submission
    if request.method == "POST":
        # All user input
        username = request.form.get("username")
        password = request.form.get("password")
        conn = sqlite3.connect("Accounts.db")
        cur = conn.cursor()
        # Look for existing account with user inputted username
        cur.execute(f"""
            SELECT Username, Password
            FROM UserInfo
            WHERE Username = '{username}';""")
        user = cur.fetchone()
        # If user input matches database
        if user and password == user[1]:
            session['username'] = user[0]
            return redirect("/database", code=302)
        else:
            flash("Invalid Login")
            return redirect('/login')
    return render_template('login.html')


# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect("/login")


@app.route('/database')
def database():
    if 'username' in session:
        return render_template('database.html', username=session['username'])
    else:
        return redirect("/login", code=302)


# Page to route user to which table in database to add to
@app.route('/database/add')
def database_add():
    return render_template('database_add.html')


# Page to add to characters table
@app.route('/database/add/character', methods=["GET", "POST"])
def database_character_add():
    # Form submission
    if request.method == "POST":
        name = request.form.get("character-name")
        alias = request.form.get("character-alias")
        birthdate = request.form.get("character-birthdate")
        deathdate = request.form.get("character-deathdate")
        gender = request.form.get("character-gender")
        affiliation = request.form.get("character-affiliation")
        description = request.form.get("character-description")
        profile_image = request.form.get("character-profileimage")
        # Function to add character
        db.add_character(name, alias, birthdate, deathdate, gender,
                         affiliation, description, profile_image)
    return render_template("database_character_add.html")


# Add game to db
@app.route('/database/add/game', methods=["GET", "POST"])
def database_game_add():
    # Form submission
    if request.method == "POST":
        # All user input
        title = request.form.get("game-title")
        releasedate = request.form.get('game-releasedate')
        description = request.form.get('game-description')
        conn = sqlite3.connect("ACDB - Copy.db")
        cur = conn.cursor()
        # Add game to db
        cur.execute(''' INSERT INTO Game (Title, ReleaseDate, Description)
                    VALUES (?,?,?)''', (title, releasedate, description))
        conn.commit()
        conn.close()
    return render_template('database_game_add.html')


# Route to choose from which table to delete
@app.route('/database/delete')
def database_delete():
    return render_template('database_delete.html')


# Route to delete character from db
@app.route('/database/delete/character')
def database_character_delete():
    characters = db.fetch("SELECT CharacterID, Name FROM CHARACTER", "all")
    if not characters:
        return redirect('/404')
    return render_template('database_character_delete.html', characters=characters)


# Route that deletes character from db
@app.route('/database/delete/character/<int:id>')
def database_delete_character_id(id):
    db.delete_character(id)
    flash("Character successfully deleted!")
    return redirect('/database/delete/character')


# Route to choose from whcih table to edit from
@app.route('/database/edit')
def database_edit():
    return render_template('database_edit.html')


# Route to choose which character to edit
@app.route('/database/edit/character')
def database_edit_character_choice():
    # Gets all characters from db.
    characters = db.fetch("SELECT CharacterID, Name FROM CHARACTER", "all")
    return render_template('database_character_choice_edit.html', characters=characters)


# Route to go to form to edit character entry
@app.route('/database/edit/character/<int:id>', methods=["GET", "POST"])
def database_edit_character(id):
    # Get character from database
    character = db.fetch("Select * FROM Character WHERE CharacterID = ?", "one", (id,))
    # If character doesn't exist
    if not character:
        return redirect('/404')
    # Form submission
    if request.method == "POST":
        # User input
        name = request.form.get("character-name")
        alias = request.form.get("character-alias")
        birthdate = request.form.get("character-birthdate")
        deathdate = request.form.get("character-deathdate")
        gender = request.form.get("character-gender")
        affiliation = request.form.get("character-affiliation")
        description = request.form.get("character-description")
        profile_image = request.form.get("character-profileimage")
        print(name, alias, birthdate, deathdate, gender,
              affiliation, description, profile_image, id)
        # Update function for character
        db.update_character(id, name, alias, birthdate, deathdate, gender,
                            affiliation, description, profile_image)
        return redirect(f'/database/edit/character/{id}')
    return render_template("database_character_edit.html", character=character)


# Page for individual assassins
@app.route('/assassin/<int:id>')
def assassin(id):
    # Gets character information from database
    assassin = db.fetch('SELECT * FROM Character WHERE CharacterID = ?',
                        "one", (id,))
    if not assassin:
        return redirect('/404')
    else:
        return render_template('assassin.html', assassin=assassin)


# Page for all assassins
@app.route('/all_assassins')
def all_assassins():
    # All characters who's affiliation is "Assassin"
    assassins = db.fetch('''SELECT CharacterID, Name, ProfileImage FROM
                        Character WHERE Affiliation LIKE "%Assassin%";''',
                         "all")
    return render_template('all_assassins.html', assassins=assassins)


# Page for all Weapons
@app.route('/all_weapons')
def all_weapons():
    # Gets all weapons in db
    weapons = db.fetch('SELECT * FROM Weapon ORDER BY WeaponID;', "all")
    return render_template('all_weapons.html', weapons=weapons)


# Page for individual weapons
@app.route('/weapon/<int:id>')
def weapon(id):
    # Get weapon information and name of users
    weapon = db.fetch('''SELECT Weapon.WeaponID,
        Weapon.Name,
        Character.CharacterID,
        Character.Name,
        Weapon.Description
        FROM Weapon
        JOIN CharacterWeapon ON Weapon.WeaponID = CharacterWeapon.WeaponID
        JOIN Character ON CharacterWeapon.CharacterID = Character.CharacterID
        WHERE Weapon.WeaponID = ?;''', 'all', (id,))
    # If weapon id doesn't exist
    if not weapon:
        return render_template('404.html')
    else:
        return render_template('weapon.html', weapon=weapon)


# Page for all Games
@app.route('/all_games')
def all_games():
    # Gets all games in database
    games = db.fetch('SELECT GameID, Title, Image FROM game;', "all")
    return render_template('all_games.html', games=games)


# Page for individual games
@app.route('/game/<int:id>')
def game(id):
    # Gets all games and characters in the game
    game = db.fetch('''SELECT
            Game.GameID,
            Game.Title,
            Game.ReleaseDate,
            Game.Description,
            Game.Image,
            Character.CharacterID,
            Character.Name
        FROM Game
            JOIN CharacterGame ON Game.GameID = CharacterGame.GameID
            JOIN Character ON CharacterGame.CharacterID = Character.CharacterID
        WHERE Game.GameID = ?;''', "all", (id,))
    # If game doesn't exist
    if not game:
        return render_template('404.html')
    else:
        return render_template('game.html', game=game)


if __name__ == "__main__":
    app.run(debug=True)  # MUST BE FINAL LINE
