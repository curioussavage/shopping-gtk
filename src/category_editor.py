from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Gio
from .gi_composites import GtkTemplate

from .db import DB
from .constants import DEFAULT_CATEGORY

from .category_editor_item import CategoryEditorItem

db = DB()

@GtkTemplate(ui='/org/gnome/Shoppinglist/category_editor.ui')
class CategoryEditor(Gtk.Popover):
    __gtype_name__ = 'CategoryEditor'

    categories_list = GtkTemplate.Child()
    new_category_btn = GtkTemplate.Child()
    close_btn = GtkTemplate.Child()
    new_input = GtkTemplate.Child()

    def __init__(self, list_id, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        self.list_id = list_id

        self.list_store = Gio.ListStore()
        self.load_categories()

        self.categories_list.bind_model(self.list_store, self.make_list_widget)

        self.close_btn.connect('clicked', self.handle_close)

        self.new_category_btn.connect('clicked', self.handle_new_cat)
        self.new_input.connect('activate', self.handle_new_entry_activate)

    def load_categories(self):
        categories = db.get_categories(self.list_id)
        self.list_store.remove_all()
        for c in categories:
            self.list_store.append(c)



    def handle_new_entry_activate(self, widget):
        text = widget.get_text()
        db.add_category(self.list_id, text)
        widget.set_text('')
        self.load_categories()

    def handle_new_cat(self, widget):
        self.new_input.show()

    def handle_close(self, widget):
        self.hide()
        self.destroy()

    def make_list_widget(self, data):
        x = CategoryEditorItem(data)
        x.show()
        return x
