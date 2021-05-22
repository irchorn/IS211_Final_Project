import sqlite3 as lite
from datetime import datetime


def insert_data():
    connection = lite.connect('project.db')
    with connection:
        cur = connection.cursor()

        cur.execute(
            "CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY AUTOINCREMENT, post_date TEXT DEFAULT "
            "CURRENT_TIMESTAMP, author TEXT NOT NULL, title TEXT NOT NULL, content TEXT NOT NULL)")
        cur.execute(
            "INSERT INTO posts VALUES (1, CURRENT_TIMESTAMP, 'Iryna', 'Madrid', 'Madrid is an energetic "
            "city known for its late nights, historic sites, and delicious cuisine. As the capital of Spain, "
            "there’s also a lot of history and art here, which you could spend weeks discovering. It’s also bursting "
            "with beautiful architecture.')")
        cur.execute(
            "INSERT INTO posts VALUES (2, CURRENT_TIMESTAMP, 'Iryna', 'Rome', 'Rome is a city that sparks a "
            "thousand mental images. From ancient structures like the Colosseum or the Pantheon, to the Spanish Steps "
            "and Trevi Fountain, to the Vatican — not to mention tons of pasta and other delicious food.')")


def posts_data():
    connection = lite.connect('project.db')
    with connection:
        connection.row_factory = lite.Row

        cur = connection.cursor()
        cur.execute("SELECT * FROM posts")
        rows = cur.fetchall()
        for row in rows:
            print("{} {} {} {} {}".format(row["id"], row["post_date"], row["author"], row["title"], row['content']))


if __name__ == "__main__":
    insert_data()
