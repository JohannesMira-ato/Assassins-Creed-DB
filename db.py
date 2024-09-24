import sqlite3
database = "ACDB - Copy.db"  # CURRENTLY A TEST DATABASE


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


def account(username, password=None, action=None):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    if action == "add":
        cur.execute(f"INSERT INTO UserInfo (Username, Password)\
                     values ('{username}', '{password}')")
        conn.commit()
        conn.close()
    if action =="delete":
        pass
        # Make delete acc stuff


def character(id=None, name=None, alias=None, birthdate=None, deathdate=None,
              gender=None, affiliation=None, description=None, profile_image=None,
              action=None):
    # database connection
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    if action == "add":
        cur.execute("""INSERT INTO Character (name, alias, birthdate, deathdate,
                        gender, affiliation, description, profileimage)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
                    (name, alias, birthdate, deathdate, gender, affiliation,
                     description, profile_image,))
    if action == "edit":
        cur.execute(f'''UPDATE Character
                SET Name="{name}", Alias="{alias}", Birthdate="{birthdate}",
                Deathdate="{deathdate}", Gender="{gender}",
                Affiliation="{affiliation}", Description="{description}",
                ProfileImage="{profile_image}"
                Where CharacterID ="{id}";''')
    if action == "delete":
        cur.execute("DELETE FROM Character WHERE CharacterID =?", (id,))
    conn.commit()
    conn.close()


def game(id, title, releasedate, description, action):
    # Database connection
    conn = sqlite3.connect("ACDB - Copy.db")
    cur = conn.cursor()
    if action == "add":
        cur.execute(''' INSERT INTO Game (Title, ReleaseDate, Description)
            VALUES (?,?,?)''', (title, releasedate, description))
