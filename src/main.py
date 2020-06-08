# main.py
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

import sys
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio

from .window import ShoppinglistWindow
from shoppinglist.actions import actions
from shoppinglist.db import DB

db = DB()
class Application(Gtk.Application):
    instance = None
    def __init__(self):
        super().__init__(application_id='org.gnome.Shoppinglist',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self._settings = Gio.Settings.new('org.gnome.Shoppinglist')
        Application.instance = self

    def do_activate(self):
        self.win = self.props.active_window
        if not self.win:
            self.win = ShoppinglistWindow(application=self)
        self.win.present()

    def do_startup(self, **kwargs):
        Gtk.Application.do_startup(self)
        try:
            for action in actions:
                self.add_action(action)
                handler = action.get_name() + '_cb'
                action.connect('activate', getattr(self, handler))
        except:
            pass

    def about_cb(self, action, param):
        about_dialog = Gtk.AboutDialog(self)
        about_dialog.set_program_name('ShoppingList')
        about_dialog.set_transient_for(self.win)
        about_dialog.show()

    def toggle_item_checked_cb(self, action, param):
        pass

    def add_list_cb(self, action, param):

        pass

    def delete_list_cb(self, action, param):
        pass

    def add_category_cb(self, action, param):
        pass

    def delete_category_cb(self, action, param):
        pass

    def add_item_cb(self, action, param):
        pass

    def delete_item_cb(self, action, param):
        pass

    def toggle_item_checked_cb(self, action, param):
        pass

def main(version):
    app = Application()
    return app.run(sys.argv)
