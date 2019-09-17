from os import path

#from tinydb import TinyDB, Query
from gi.repository import GLib


class ListModel():
    pass
   # name = <string>
   # sections = [<name>]
   # items = []


def add_item_op(item):
     def transform(doc):
         # do something with the document
         import ipdb; ipdb.set_trace()
     return transform

def toggle_checked_op(item_name, checked):
     def transform(doc):
         # do something with the document
         import ipdb; ipdb.set_trace()
     return transform

def toggle_checked_op(section_name):
     def transform(doc):
         # do something with the document
         import ipdb; ipdb.set_trace()
     return transform

class DB():
    def __init__(self):
        pass
        # dir = GLib.get_user_data_dir()
        # db_path = path.join(dir, 'db.json')
        # self.db = TinyDB(db_path)

    def create(self, list):
        db.insert(list)

    def add_item(self, item, list_name):
        row = Query()
        self.db.update(add_item_op(item), row.name == list_name)
        return True

    def toggle_checked(self, item_name, list_name, checked):
        row = Query()
        self.db.update(toggle_checked_op(item_name, checked), row.name == list_name)

    def add_section(self, list_name, section_name):
        row = Query()
        self.db.update(add_section_op(section_name), row.name == list_name)

    def get_list(self, name):
        row = Query()
        return self.db.search(row.name == name)

