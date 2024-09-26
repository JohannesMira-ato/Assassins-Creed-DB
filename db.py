import sqlite3
database = "ACDB.db"


#  Function to get information from db and for fetchone and fetchall query
def fetch(query, fetchtype, parameter=None):
    # Database connection
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    if fetchtype == "all":
        if parameter is None:
            cur.execute(query)
            results = cur.fetchall()
        else:
            cur.execute(query, parameter)
            results = cur.fetchall()
    elif fetchtype == "one":
        cur.execute(query, parameter)
        results = cur.fetchone()
    conn.close()
    return results


# Handles adding and deleting accounts
def account(username, password=None, action=None):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    if action == "add":
        cur.execute(f"INSERT INTO UserInfo (Username, Password)\
                     values ('{username}', '{password}')")
        conn.commit()
        conn.close()
    if action == "delete":
        pass
        # For future if have time available


# Handles adding, editing and deleting from character table
def character(id=None, name=None, alias=None, birthdate=None, deathdate=None,
              gender=None, affiliation=None, description=None, profile_image=None,
              action=None):
    # database connection
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    # Adding to characters
    if action == "add":
        cur.execute("""INSERT INTO Character (name, alias, birthdate, deathdate,
                        gender, affiliation, description, profileimage)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
                    (name, alias, birthdate, deathdate, gender, affiliation,
                     description, profile_image,))
    # Editing existing extry
    if action == "edit":
        cur.execute(f'''UPDATE Character
                SET Name="{name}", Alias="{alias}", Birthdate="{birthdate}",
                Deathdate="{deathdate}", Gender="{gender}",
                Affiliation="{affiliation}", Description="{description}",
                ProfileImage="{profile_image}"
                Where CharacterID ="{id}";''')
    # Delete existing character
    if action == "delete":
        cur.execute("DELETE FROM Character WHERE CharacterID =?", (id,))
    conn.commit()
    conn.close()


# Handles adding new games to game table, would handle editng
# and deleting if have time
def game(id=None, title=None, releasedate=None, description=None, action=None):
    # Database connection
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    if action == "add":
        cur.execute(''' INSERT INTO Game (Title, ReleaseDate, Description)
            VALUES (?,?,?)''', (title, releasedate, description))
        conn.commit()
        conn.close()
