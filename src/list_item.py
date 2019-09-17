from gi.repository import Gtk
from .gi_composites import GtkTemplate


@GtkTemplate(ui='/org/gnome/Shoppinglist/list_item.ui')
class ListItem(Gtk.ListBoxRow):
    __gtype_name__ = 'ListItem'

    item_name = GtkTemplate.Child()
    item_checkbox = GtkTemplate.Child()

    def __init__(self, item, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        self.item = item

        markup = '<span size="large"><b>{text}</b></span>'
        self.item_name.set_markup(markup.format(text=self.item.title))
