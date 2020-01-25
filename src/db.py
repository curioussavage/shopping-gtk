from os import path

from gi.repository import GLib

import sqlite3
from uuid import uuid4


class ListModel():
    pass
   # name = <string>
   # sections = [<name>]
   # items = []

class DB():
    def create_tables(self):
        # We use uuid for primary key since I want to sync with remote server
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS list_items (
            id   TEXT,
            list_id INTEGER,
            title  VARCHAR(255) NOT NULL,
            done INTEGER,
            category_id TEXT,
            FOREIGN KEY (list_id) REFERENCES lists (id),
            FOREIGN KEY (category) REFERENCES categories (id)
           )"""
        )

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS lists (
            id   TEXT,
            name TEXT
           )"""
        )
        res = self.cursor.execute("""CREATE TABLE IF NOT EXISTS categories (
            id TEXT,
            name TEXT,
            list_id TEXT,
            FOREIGN KEY (list_id) REFERENCES lists (id)
            )""")
        print('res from categories is: ', res)

    def __init__(self):
        dir = GLib.get_user_data_dir()
        db_path = path.join(dir, 'app.db')
        print('db path is ', db_path)
        # might need to create db if not there
        conn = sqlite3.connect(db_path)
        self.cursor = conn.cursor()

        # Create table
        self.create_tables()

    def add_list(self, name):
        item_id = uuid4()
        res = self.cursor.execute("""INSERT INTO lists (id, name) values (?, ?)""", (item_id, name))
        self.add_category(item_id, 'default')

    def add_item(self, list_id, category_id, title):
        item_id = uuid4()
        res = self.cursor.execute(
        """INSERT INTO list_items (id, list_id, category_id, title, done)
           values (?, ?, ?, ?)
        """, (item_id, list_id, category_id, title, False))
        # check res

    def toggle_checked(self, item_id, done):
        res = self.cursor.execute(
        """UPDATE list_items  SET done=? WHERE item_id=?
        """, (done, item_id))

    def add_category(self, list_id, name):
        item_id = uuid4()
        res = self.cursor.execute(
        """INSERT INTO categories (id, list_id, name)
           values (?, ?, ?, ?)
        """, (item_id, list_id, name))

    def get_list(self, name):
        pass

