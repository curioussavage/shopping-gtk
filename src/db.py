from os import path

from gi.repository import GObject
from gi.repository import GLib

import sqlite3
from uuid import uuid4

from .constants import DEFAULT_CATEGORY


class List(GObject.GObject):
    def __init__(self, id, name):
        GObject.GObject.__init__(self)
        self.id = id
        self.name = name


class Category(GObject.GObject):
    def __init__(self, id, name, list_id):
        GObject.GObject.__init__(self)
        self.id = id
        self.name = name
        self.list_id = list_id


class ListItem(GObject.GObject):
    def __init__(self, id, list_id, title, checked, category_id):
        GObject.GObject.__init__(self)
        self.id = id
        self.list_id = list_id
        self.title = title
        self.checked = checked
        self.category_id = category_id


class DB():
    def create_tables(self):
        # We use uuid for primary key since I want to sync with remote server
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS list_items (
            id   TEXT,
            list_id TEXT,
            title  VARCHAR(255) NOT NULL,
            done INTEGER,
            category_id TEXT,
            FOREIGN KEY (list_id) REFERENCES lists (id),
            FOREIGN KEY (category_id) REFERENCES categories (id)
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

    __instance = None

    def __new__(cls):
        if DB.__instance is None:
            DB.__instance = object.__new__(cls)
        return DB.__instance

    def __init__(self):
        dir = GLib.get_user_data_dir()
        db_path = path.join(dir, 'app.db')
        print('db path is ', db_path)
        # might need to create db if not there
        conn = sqlite3.connect(db_path)
        self.cursor = conn.cursor()
        self.conn = conn

        # Create table
        self.create_tables()

    @staticmethod
    def new_id():
        # creates a new uuid4 and returns as a hex string
        return uuid4().hex

    def add_list(self, name):
        list_id = DB.new_id()
        res = self.cursor.execute("""INSERT INTO lists (id, name) values (?, ?)""", (list_id, name))
        self.conn.commit()

        return list_id

    def add_item(self, list_id, title, category_id=None):
        if not category_id:
            category_id = DEFAULT_CATEGORY
        item_id = DB.new_id()
        res = self.cursor.execute(
        """INSERT INTO list_items (id, list_id, category_id, title, done)
           values (?, ?, ?, ?, ?)
        """, (item_id, list_id, category_id, title, False))
        self.conn.commit()
        return item_id

    # @GObject.Signal(arg_types=(str,bool))
    def toggle_checked(self, item_id, done):
        res = self.cursor.execute(
        """UPDATE list_items  SET done=? WHERE id=?
        """, (done, item_id))
        self.conn.commit()

    def add_category(self, list_id, name):
        item_id = DB.new_id()
        res = self.cursor.execute(
        """INSERT INTO categories (id, list_id, name)
           values (?, ?, ?)
        """, (item_id, list_id, name))
        self.conn.commit()

    def get_lists(self):
        res = self.cursor.execute(
        """SELECT * FROM lists;
        """)
        return res.fetchall()

    def get_list(self, list_id):
        res = self.cursor.execute(
        """SELECT * FROM lists WHERE id=?;
        """, [list_id])
        res = res.fetchall()[0]
        return List(res[0], res[1])

    def get_list_items(self, list_id):
        res = self.cursor.execute(
        """SELECT * FROM list_items
        Where list_id=?
        """, [list_id])

        return [ListItem(item[0], item[1], item[2], item[3], item[4]) for item in res.fetchall()]

    def get_categories(self, list_id):
        res = self.cursor.execute(
            """SELECT * FROM categories WHERE list_id=?""",
            [list_id],
        )
        items = res.fetchall()
        categories = [Category(DEFAULT_CATEGORY, 'default', list_id)]
        for item in items:
            categories.append(Category(item[0], item[1], item[2]))
        return categories


