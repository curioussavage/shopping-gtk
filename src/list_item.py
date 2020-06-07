from gi.repository import Gtk
from .gi_composites import GtkTemplate

from .db import DB

db = DB()

@GtkTemplate(ui='/org/gnome/Shoppinglist/list_item.ui')
class ListItem(Gtk.ListBoxRow):
    __gtype_name__ = 'ListItem'

    item_name = GtkTemplate.Child()
    item_checkbox = GtkTemplate.Child()

    def __init__(self, item, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        self.item = item


        markup = '<span size="medium">{text}</span>'
        self.item_name.set_markup(markup.format(text=self.item.title))

        self.item_checkbox.set_active(item.checked)
        self.item_checkbox.connect('toggled', self.handle_toggled)

    def handle_toggled(self, btn):
        done = btn.get_active()
        db.toggle_checked(self.item.id, done)
