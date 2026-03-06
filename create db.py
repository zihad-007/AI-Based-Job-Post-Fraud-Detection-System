 import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

# users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
contact TEXT,
password TEXT
)
""")

# job posts table
cursor.execute("""
CREATE TABLE IF NOT EXISTS job_posts(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
company TEXT,
description TEXT,
salary TEXT,
type TEXT,
result TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully")
