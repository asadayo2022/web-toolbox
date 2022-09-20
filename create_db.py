import sqlite3

conn = sqlite3.connect('urls.db')
conn.execute('''CREATE TABLE urls (
short_id TEXT NOT NULL UNIQUE,
URL TEXT NOT NULL);''')
conn.close()