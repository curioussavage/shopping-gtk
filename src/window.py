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
    def __init__(self, title, checked=None):
        GObject.GObject.__init__(self)
        self.title = title
        self.checked = checked


class ShoppingList(GObject.GObject):
    def __init__(self, name, items=[]):
        GObject.GObject.__init__(self)
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

    # TODO use flatpak cli tool to gnereate module for tinydb
    shoppinglist = GtkTemplate.Child()
    lists_listbox = GtkTemplate.Child()

    newlistbtn = GtkTemplate.Child()
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

        self.newlistbtn.connect('clicked', self.on_new_list)

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

            self.lists_store.append(ShoppingList(name))
            self.newlist_dialog.hide()
            input.set_text('')
        else:
            self.newlist_dialog.hide()


    def handle_item_dialog_res(self, dialog, resp):
        if resp == Gtk.ResponseType.ACCEPT:
            input = self.new_item_dialog.get_child().get_children()[0].get_children()[2]
            name = input.get_text()

            self.get_slist_store().append(ListItem(name))
            self.new_item_dialog.hide()
            input.set_text('')
        else:
            self.new_item_dialog.hide()

    def get_slist_store(self):
        sel_row = self.lists_listbox.get_selected_row()
        if sel_row:
            row_index = sel_row.get_index()
            list = self.lists_store.get_item(row_index)
            return list.items
        return None

    def handle_list_selected(self, listbox, row):
        row_index = row.get_index()
        list = self.lists_store.get_item(row_index)
        self.shoppinglist.bind_model(list.items, make_list_widget)

    def on_new_item(self, btn):
        self.new_item_dialog.run()

    def lists_listbox_handle_add(self, listModel, position, removed, added):
        row = self.lists_listbox.get_row_at_index(position)
        self.lists_listbox.select_row(row)


    def init_lists(self):
        self.lists_store.append(ShoppingList('test'))

    def on_new_list(self, btn):
        self.newlist_dialog.run()

