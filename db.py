import sqlite3

database = "ACDB - Copy.db"  # CURRENTLY A TEST DATABASE


def add_character(name, alias, birthdate, deathdate, gender,
                  affiliation, description, profileimage):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("""INSERT INTO Character (name, alias, birthdate, deathdate,
                gender, affiliation, description, profileimage)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
                (name, alias, birthdate, deathdate, gender, affiliation,
                 description, profileimage,))
    conn.commit()
    conn.close()


#  Function to choose between fetchone and fetchall query
def fetch(query, fetchtype, parameter=None):
    conn = sqlite3.connect("ACDB.db")  # TEST DB
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
