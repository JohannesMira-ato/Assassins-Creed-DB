# pip install flask
from flask import Flask, render_template, request, redirect, session, flash
# pip install flask_wtf wtforms
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
# pip install werkzeug
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
import db

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'static/images'  # Uploaded file location
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB file size limit
ALLOWED_EXTENSIONS = set(['png', 'jpg',])


def check_filetype(filename):
    if filename.endswith(".png"):
        return ("png")
    elif filename.endswith(".jpg"):
        return (".jpg")


# Check if img format is in allowed extentions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")


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
        match = db.fetch("SELECT Username from UserInfo where USERNAME = ?", "one",(username,))
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
        # Add account to database
        db.character({username}, {password}, action="add")
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
        # Look for existing account with user inputted username
        user = db.fetch("SELECT Username, Password FROM UserInfo WHERE username = ?", "one", (username,))
        # If user input matches databasef
        if user and password == user[1]:
            session['username'] = user[0]
            return redirect("/dashboard", code=302)
        else:
            flash("Invalid Login")
            return redirect('/login')
    return render_template('login.html')


# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect("/login")


# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect("/login", code=302)


# Page to route user to which table in database to add to
@app.route('/database/add')
def database_add():
    return render_template('database_add.html')


# Page to add to characters table
@app.route('/database/add/character', methods=["GET", "POST"])
def database_character_add():
    profile_image = None  # Initialize profile_image
    # Initialize form outside the POST block
    try:
        form = UploadFileForm()
    except RequestEntityTooLarge:  # Large file size error
        flash("Image size exceeds the 16MB limit")
        return redirect("/database/add/character")
    # Form submission
    if request.method == "POST":
        name = request.form.get("character-name")
        alias = request.form.get("character-alias")
        birthdate = request.form.get("character-birthdate")
        deathdate = request.form.get("character-deathdate")
        gender = request.form.get("character-gender")
        affiliation = request.form.get("character-affiliation")
        description = request.form.get("character-description")
        if not name:
            flash("Character must have a name")
            return redirect("/database/add/character")
        # Add img to db
        if form.validate_on_submit():
            file = form.file.data  # Get img from form
            # If img uploaded
            if file:
                # Check if img format is allowed
                if not allowed_file(file.filename):
                    flash("Only jpg and png files are allowed")
                    return redirect("/database/add/character")

                # Rename file to character name + filetype
                filetype = check_filetype(file.filename)
                characterimg = name.replace(" ", "_")
                file.filename = (f"{characterimg}.{filetype}")

                # Save file in /static/images folder
                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                          app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                profile_image = file.filename
            # Function to add character
        db.character(name=name, alias=alias, birthdate=birthdate, deathdate=deathdate, gender=gender,
                     affiliation=affiliation, description=description, profile_image=profile_image,
                     action="add")
        flash("Character Successfully added to database")
    return render_template("database_character_add.html", form=form)


# Add game to db
@app.route('/database/add/game', methods=["GET", "POST"])
def database_game_add():
    # Form submission
    if request.method == "POST":
        try:
            # All user input
            title = request.form.get("game-title")
            releasedate = request.form.get('game-releasedate')
            description = request.form.get('game-description')
            db.game(action="add", title=title, releasedate=releasedate,
                    description=description)
        except TypeError:
            flash("Invalid Submission")
            return redirect('/database/add/game')
    return render_template('database_game_add.html',)


# Route to choose from which table to delete
@app.route('/database/delete')
def database_delete():
    return render_template('database_delete.html')


# Route to delete character from db
@app.route('/database/delete/character')
def database_character_delete():
    # Get all characters' name from database
    characters = db.fetch("SELECT CharacterID, Name FROM CHARACTER", "all")
    # If nothing found in db
    if not characters:
        return render_template("404.html")
    return render_template('database_character_delete.html', characters=characters)


# Route that deletes character from db
@app.route('/database/delete/character/<int:id>')
def database_delete_character_id(id):
    db.character(id=id, action="delete")
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
        return render_template("404.html")
    # Image upload
    try:
        form = UploadFileForm()
        # Check for valid post request
        if form.validate_on_submit():
            file = form.file.data  # Get img from form
            # If img uploaded
            if file:
                # Check if img format is allowed
                if not allowed_file(file.filename):
                    flash("Only jpg and png files are allowed")
                    return redirect(f"/database/edit/character/{id}")

                # Rename file to character name + filetype
                filetype = check_filetype(file.filename)
                characterimg = character[1].replace(" ", "_")
                file.filename = (f"{characterimg}{filetype}")

                # Save file in /static/images folder
                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                          app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
    # Large file size error
    except RequestEntityTooLarge:
        flash("Image size exceeds the 16MB limit")
        return redirect(f"/database/edit/character/{id}")
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
        profile_image = file.filename
        # Update function for character
        if name == "":
            flash("Character must have a name")
            return redirect(f'/database/edit/character/{id}')
        db.character(id=id, name=name, alias=alias, birthdate=birthdate,
                     deathdate=deathdate, gender=gender,
                     affiliation=affiliation, description=description,
                     profile_image=profile_image, action="edit")
        flash("Characer entry successfully edited")
        return redirect(f'/database/edit/character/{id}')
    return render_template("database_character_edit.html", character=character, form=form)


# Page for individual assassins
@app.route('/assassin/<int:id>')
def assassin(id):
    try:
        # Gets character information from database
        assassin = db.fetch('SELECT * FROM Character WHERE CharacterID = ?',
                            "one", (id,))
        # If asssassin not found
        if not assassin:
            return render_template("404.html")
        else:
            return render_template('assassin.html', assassin=assassin)
    except OverflowError:
        return render_template("500.html")


# Page for all assassins
@app.route('/all_assassins')
def all_assassins():
    # All characters who's affiliation is "Assassin"
    assassins = db.fetch(query='''SELECT CharacterID, Name, ProfileImage FROM
                         Character WHERE Affiliation LIKE "%Assassin%";''',
                         fetchtype="all")
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
    try:
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
    except OverflowError:
        return render_template("500.html")


# Page for all Games
@app.route('/all_games')
def all_games():
    # Gets all games in database
    games = db.fetch('SELECT GameID, Title, Image FROM game;', "all")
    return render_template('all_games.html', games=games)


# Page for individual games
@app.route('/game/<int:id>')
def game(id):
    try:
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
    except OverflowError:
        return render_template("500.html")


if __name__ == "__main__":
    app.run(debug=True)  # MUST BE FINAL LINE, DEBUGGER
