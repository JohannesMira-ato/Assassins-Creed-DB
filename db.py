import sqlite3

database = "ACDB - Copy.db"  # CURRENTLY A TEST DATABASE

def add_character(name, alias, birthdate, deathdate, gender, 
                  affiliation, description, image, profileimage):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("""INSERT INTO Character (name, alias, birthdate, deathdate,
                gender, affiliation, description, image, profileimage)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                (name, alias, birthdate, deathdate, gender, affiliation,
                 description, image, profileimage,))
    conn.commit()
    conn.close()
       
