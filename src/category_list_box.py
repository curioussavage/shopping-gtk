from gi.repository import Gtk
from gi.repository import Gio
from .gi_composites import GtkTemplate

from .db import DB

from .list_item import ListItem as ListItemWidget

from .constants import DEFAULT_CATEGORY

from .input import Input

db = DB()


@GtkTemplate(ui='/org/gnome/Shoppinglist/category_list_box.ui')
class CategoryListBox(Gtk.Box):
    __gtype_name__ = 'CategoryListBox'

    category_label = GtkTemplate.Child()
    new_item_button = GtkTemplate.Child()
    header_box = GtkTemplate.Child()
    items_list = GtkTemplate.Child()

    list_store = Gio.ListStore()

    def __init__(self, category, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        self.category = category
        self.list_store = Gio.ListStore()

        if category.id == DEFAULT_CATEGORY:
            self.header_box.hide()


        self.new_item_button.connect('clicked', self.handle_new_item)

        self.items_list.bind_model(self.list_store, self.make_list_widget)

        markup = '<span size="large"><b>{text}</b></span>'
        self.category_label.set_markup(markup.format(text=category.name))

        items = db.get_list_items(category.list_id)

        for item in items:
            if item.category_id == category.id and not item.checked:
                self.list_store.append(item)

    def handle_new_item(self, btn):
        inp = Input()
        inp.set_placeholder('enter item name')
        self.add(inp)
        inp.popup()
        inp.connect('closed', lambda p: self.remove(inp))
        inp.connect('enter_text', lambda _,value: db.add_item(self.category.list_id, value, self.category.id))
        # add item to list or use the change_list or something
        # render popup

    @staticmethod
    def make_list_widget(data):
        return ListItemWidget(data)
