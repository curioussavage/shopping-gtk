from gi.repository import Gtk
from .gi_composites import GtkTemplate

from .db import DB

db = DB()

@GtkTemplate(ui='/org/gnome/Shoppinglist/category_editor_item.ui')
class CategoryEditorItem(Gtk.ListBoxRow):
    __gtype_name__ = 'CategoryEditorItem'

    category_name = GtkTemplate.Child()
    category_delete_btn = GtkTemplate.Child()

    def __init__(self, category, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        self.category = category


        markup = '<span size="large"><b>{text}</b></span>'
        self.category_name.set_markup(markup.format(text=category.name))

        self.category_delete_btn.connect('clicked', self.handle_delete)

    def handle_delete(self, widget):
        pass

