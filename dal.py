import sqlite3

DB = sqlite3.connect('settings.db')
CURSOR = DB.cursor()


def save_lastsync(lastsync):
    CURSOR.execute("SELECT * FROM settings")
    results = CURSOR.fetchone()
    if results is None:
        CURSOR.execute(
            "INSERT INTO settings VALUES(1, '%s')" % (lastsync))
    else:
        CURSOR.execute("UPDATE settings SET lastsync = '" +
                       lastsync + "' WHERE id = 1")

    DB.commit()


def get_lastsync():
    CURSOR.execute(
        "CREATE TABLE IF NOT EXISTS settings (id INTEGER, lastsync TEXT)")

    CURSOR.execute("SELECT * FROM settings;")
    return CURSOR.fetchone()
