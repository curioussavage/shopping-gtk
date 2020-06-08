
import gi
from gi.repository import Gio
from gi.repository import GLib


#     def _set_actions(self):
#         action_entries = [
#             ('about', self._about, None),
#             ("help", self._help, ("app.help", ["F1"])),
#             ("lastfm-configure", self._lastfm_account, None),
#             ("quit", self._quit, ("app.quit", ["<Ctrl>Q"]))
#         ]

#         for action, callback, accel in action_entries:
#             simple_action = Gio.SimpleAction.new(action, None)
#             simple_action.connect('activate', callback)
#             self.add_action(simple_action)
#             if accel is not None:
#                 self.set_accels_for_action(*accel)


def new_action(name, param):
    return Gio.SimpleAction.new(name, param)

# def _help(self, action, param)

actions = [
     # Misc actions
     new_action('about', None),

     # app settings actions
     new_action('toggle_view_checked', None),

     # list actions
     new_action('add_list', GLib.VariantType('s')),
     new_action('delete_list', GLib.VariantType('s')),
     new_action('add_category', GLib.VariantType('s')),
     new_action('delete_category', GLib.VariantType('s')),

     # list item actions
     new_action('add_item', GLib.VariantType('s')),
     new_action('delete_item', GLib.VariantType('s')),
     new_action('toggle_item_checked', GLib.VariantType('s')),
]
