import sqlite3

database = "ACDB - Copy.db"  # CURRENTLY A TEST DATABASE


def add_character(name, alias, birthdate, deathdate, gender,
                  affiliation, description, profileimage):
    # Database connection
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    # Add all information to character table
    cur.execute("""INSERT INTO Character (name, alias, birthdate, deathdate,
                gender, affiliation, description, profileimage)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
                (name, alias, birthdate, deathdate, gender, affiliation,
                 description, profileimage,))
    conn.commit()
    conn.close()


def add_game(title, releasedate, description):
    # Database connection
    conn = sqlite3.connect("ACDB - Copy.db")
    cur = conn.cursor()
    # Add all information to game table
    cur.execute(''' INSERT INTO Game (Title, ReleaseDate, Description)
                VALUES (?,?,?)''', (title, releasedate, description))
    conn.commit()
    conn.close()


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


def delete_character(CharacterID):
    # Database connection
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    # Delete character from database
    cur.execute("DELETE FROM Character WHERE CharacterID =?", (CharacterID,))
    conn.commit()
    conn.close()


# Edit character information in database
def update_character(id, name, alias, birthdate, deathdate, gender,
                     affiliation, description, profileimage):
    # Database connection
    conn = sqlite3.connect("ACDB - Copy.db")
    cur = conn.cursor()
    # Update character information
    cur.execute(f'''UPDATE Character
                SET Name="{name}", Alias="{alias}", Birthdate="{birthdate}",
                Deathdate="{deathdate}", Gender="{gender}",
                Affiliation="{affiliation}", Description="{description}",
                ProfileImage="{profileimage}"
                Where CharacterID ="{id}";''')
    conn.commit()
    conn.close()
