import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
conn.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image BLOB,
        datePicture DATE DEFAULT (DATE('now'))
    )
''')
conn.commit()
conn.close()
