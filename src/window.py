# window.py
#
# Copyright 2018 curioussavage
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time

from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GLib
from gi.repository import GObject
from .gi_composites import GtkTemplate

from .list_item import ListItem as ListItemWidget
from .list import List as ListWidget

from .db import DB


class ListItem(GObject.GObject):
    def __init__(self, title, item_id, checked=False):
        GObject.GObject.__init__(self)
        self.id = item_id
        self.title = title
        self.checked = checked


class ShoppingList(GObject.GObject):
    def __init__(self, name, list_id, items=[]):
        GObject.GObject.__init__(self)
        self.id = list_id
        self.items = Gio.ListStore()
        self.name = name


def make_list_widget(data):
    return ListItemWidget(data)


def make_lists_widget(data):
    return ListWidget(data)


@GtkTemplate(ui='/org/gnome/Shoppinglist/window.ui')
class ShoppinglistWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ShoppinglistWindow'

    db = DB()

    back_btn = GtkTemplate.Child()
    stack = GtkTemplate.Child()
    lists_window = GtkTemplate.Child()
    list_view_window = GtkTemplate.Child()


    # TODO use flatpak cli tool to gnereate module for tinydb
    shoppinglist = GtkTemplate.Child()
    lists_listbox = GtkTemplate.Child()

    newlist_dialog = GtkTemplate.Child()

    new_item_button = GtkTemplate.Child()
    new_item_dialog = GtkTemplate.Child()

    list_store = Gio.ListStore()
    lists_store = Gio.ListStore()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        print('starting up app')

        self.init_lists()
        try:
            self.selected_list = self.lists_store.get_item(0).id
        except:
            self.selected_list = None

        if self.selected_list:
            self.change_list(self.selected_list)

        self.back_btn.connect('clicked', self.handle_back)
        self.back_btn.hide() # we are on the lists page here so it should be hidden

        self.shoppinglist.bind_model(self.list_store, make_list_widget)
        self.lists_listbox.bind_model(self.lists_store, make_lists_widget)
        self.lists_listbox.connect('row_selected', self.handle_list_selected)
        self.lists_listbox.set_selection_mode(Gtk.SelectionMode.BROWSE)

        self.lists_store.connect('items_changed', self.lists_listbox_handle_add)

        self.shoppinglist.set_placeholder(Gtk.Label('This list is empty'))

        self.new_item_button.connect('clicked', self.on_new_item)

        self.newlist_dialog.connect('response', self.handle_list_dialog_res)
        self.new_item_dialog.connect('response', self.handle_item_dialog_res)

    def handle_list_dialog_res(self, dialog, resp):
        if resp == Gtk.ResponseType.ACCEPT:
            input = self.newlist_dialog.get_child().get_children()[0].get_children()[2]
            name = input.get_text()

            list_id = self.db.add_list(name)
            self.lists_store.append(ShoppingList(name, list_id))
            self.newlist_dialog.hide()
            input.set_text('')
        else:
            self.newlist_dialog.hide()


    def handle_item_dialog_res(self, dialog, resp):
        if resp == Gtk.ResponseType.ACCEPT:
            input = self.new_item_dialog.get_child().get_children()[0].get_children()[2]
            name = input.get_text()

            # TODO add category
            item_id = self.db.add_item(self.selected_list, name)
            self.list_store.append(ListItem(name, item_id))
            self.new_item_dialog.hide()
            input.set_text('')
        else:
            self.new_item_dialog.hide()


    def change_list(self, list_id):
        items = self.db.get_list_items(list_id)

        self.list_store.remove_all()
        for item in items:
            self.list_store.append(ListItem(title=item[2], item_id=item[0], checked=bool(item[3])))

    def handle_list_selected(self, listbox, row):
        row_index = row.get_index()
        list = self.lists_store.get_item(row_index)
        self.selected_list = list.id
        self.change_list(list.id)
        self.stack.set_visible_child(self.list_view_window)
        self.back_btn.show()

    def handle_back(self, btn):
        self.stack.set_visible_child(self.lists_window)
        self.back_btn.hide()

    def on_new_item(self, btn):
        # check stack
        if self.stack.get_visible_child() == self.lists_window:
            self.newlist_dialog.run()
        else:
            self.new_item_dialog.run()

    def lists_listbox_handle_add(self, listModel, position, removed, added):
        row = self.lists_listbox.get_row_at_index(position)
        self.lists_listbox.select_row(row)


    def init_lists(self):
        print('getting lists')
        res = self.db.get_lists()
        for row in res:
            self.lists_store.append(ShoppingList(row[1], row[0]))
            print(row)


