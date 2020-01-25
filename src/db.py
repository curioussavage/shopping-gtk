from os import path

from gi.repository import GLib

import sqlite3


class ListModel():
    pass
   # name = <string>
   # sections = [<name>]
   # items = []

class DB():
    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS list_items (
            id   INTEGER PRIMARY KEY,
            list_id INTEGER,
            title  VARCHAR(255) NOT NULL,
            done INTEGER,
            FOREIGN KEY (list_id) REFERENCES lists (id)
           )"""
        )

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS lists (
            id   INTEGER PRIMARY KEY,
            name TEXT
           )"""
        )

    def __init__(self):
        dir = GLib.get_user_data_dir()
        db_path = path.join(dir, 'app.db')
        print('db path is ', db_path)
        # might need to create db if not there
        conn = sqlite3.connect(db_path)
        self.cursor = conn.cursor()

        # Create table
        self.create_tables()

    def create(self, list):
        db.insert(list)

    def add_item(self, item, list_name):
        pass

    def toggle_checked(self, item_name, list_name, checked):
        pass

    def add_section(self, list_name, section_name):
        pass

    def get_list(self, name):
        pass

