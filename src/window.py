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
import functools

from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GLib
from gi.repository import GObject
from .gi_composites import GtkTemplate

from shoppinglist.list import List as ListWidget
from shoppinglist.category_list_box import CategoryListBox
from shoppinglist.category_editor import CategoryEditor
from shoppinglist.input import Input
from shoppinglist.dialog_input import DialogInput

from shoppinglist.db import DB

from shoppinglist.constants import DEFAULT_CATEGORY

class ShoppingList(GObject.GObject):
    def __init__(self, name, list_id, items=[]):
        GObject.GObject.__init__(self)
        self.id = list_id
        self.items = Gio.ListStore()
        self.name = name


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
    category_list_box_container = GtkTemplate.Child()
    lists_listbox = GtkTemplate.Child()

    new_item_button = GtkTemplate.Child()
    list_menu_popover = GtkTemplate.Child()

    categories_btn = GtkTemplate.Child()
    toggle_show_checked_btn = GtkTemplate.Child()

    shoppinglist_name_label = GtkTemplate.Child()
    shoppinglist_add_btn = GtkTemplate.Child()

    about_btn = GtkTemplate.Child()
    app_menu_popover = GtkTemplate.Child()

    list_store = Gio.ListStore()
    lists_store = Gio.ListStore()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        self.app = kwargs['application']

        self.init_lists()
        try:
            list = self.lists_store.get_item(0)
            self.selected_list = list.id
        except:
            self.selected_list = None

        if self.selected_list:
            self.change_list(self.selected_list)

        self.back_btn.connect('clicked', self.handle_back)
        self.back_btn.hide() # we are on the lists page here so it should be hidden

        self.lists_listbox.bind_model(self.lists_store, make_lists_widget)
        self.lists_listbox.connect('row_selected', self.handle_list_selected)
        self.lists_listbox.set_selection_mode(Gtk.SelectionMode.BROWSE)

        self.lists_store.connect('items_changed', self.lists_listbox_handle_add)


        self.new_item_button.connect('clicked', self.on_new_list)
        self.shoppinglist_add_btn.connect('clicked', self.on_new_item)


        self.categories_btn.connect('clicked', self.click_categories_btn)
        self.toggle_show_checked_btn.connect('clicked', self.handle_toggle_show_checked)
        self.toggle_show_checked_btn.active = self.app._settings.get_value('show-checked')
        self.about_btn.connect('clicked', self.handle_about_btn_click)

    def handle_about_btn_click(self, w):
        about_dialog = Gtk.AboutDialog(self)
        about_dialog.set_program_name('ShoppingList')
        about_dialog.set_transient_for(self)
        about_dialog.show()
        self.app_menu_popover.hide()


    def handle_toggle_show_checked(self, w):
        val = self.app._settings.get_value('show-checked')
        self.app._settings.set_boolean('show-checked', not val)
        self.list_menu_popover.hide()

    def click_categories_btn(self, btn):
        editor = CategoryEditor(self.selected_list)
        self.category_list_box_container.add(editor)
        self.list_menu_popover.hide()
        editor.show()


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

    def change_list(self, list_id):
        the_list = self.db.get_list(list_id)
        categories = self.db.get_categories(list_id)
        self.category_list_box_container.foreach(lambda child: self.category_list_box_container.remove(child))
        for category in categories:
            self.category_list_box_container.add(CategoryListBox(category))
        self.shoppinglist_name_label.set_text(the_list.name)

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

    def add_item(self, value):
        item_id = self.db.add_item(self.selected_list, value)
        self.change_list(self.selected_list) # a hack to make it refresh

    def on_new_item(self, btn):
        dialog = DialogInput(self)
        dialog.connect('enter_text', lambda _,value: self.add_item(value))
        dialog.set_placeholder("item name")
        dialog.show_all()

    def add_list(self, value):
        list_id = self.db.add_list(value)
        self.lists_store.append(ShoppingList(value, list_id))

    def on_new_list(self, btn):
        dialog = DialogInput(self)
        dialog.connect('enter_text', lambda _, val: self.add_list(val))
        dialog.set_placeholder("list name")
        dialog.show_all()

    def lists_listbox_handle_add(self, listModel, position, removed, added):
        row = self.lists_listbox.get_row_at_index(position)
        self.lists_listbox.select_row(row)


    def init_lists(self):
        res = self.db.get_lists()
        for row in res:
            self.lists_store.append(ShoppingList(row[1], row[0]))
