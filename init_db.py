import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Primer Post', 'Contenido del primer post')
            )
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Segundo Post', 'Contenido del segundo post')
            )

connection.commit()
connection.close()