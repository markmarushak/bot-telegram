import sqlite3

"""
{"ok":true,"result":{"short_name":"RezWay","author_name":"RezWayBlog","author_url":"","access_token":"cf60650e989daa99c5672392d64417c859c5e60e2fcb50a542f3802dea86","auth_url":"https://edit.telegra.ph/auth/UnXWOExDmsmcUyHyli4GhNHKH1xBrIaj35dRJKt6aN"}}
"""

token = 'cf60650e989daa99c5672392d64417c859c5e60e2fcb50a542f3802dea86'

class Spam():

    def __init__(self):
        pass


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('blog.db')
        self.c = self.conn.cursor()
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS articles( 
            id INTEGER PRIMARY KEY,
            title TEXT,
            author_name TEXT,
            content REAL )
        """)

    def add_blog(self, title, author_name, content):
        self.c.execute(''' INSERT INTO articles(title, author_name, content) VALUES (?, ?, ?)''',(title, author_name, content))
        self.conn.commit()


if __name__ == '__spam__':
    db = DB()
