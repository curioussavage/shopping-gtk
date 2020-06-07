from gi.repository import Gtk
from gi.repository import Gio
from .gi_composites import GtkTemplate

from shoppinglist.db import DB
from shoppinglist.constants import DEFAULT_CATEGORY

from shoppinglist.dialog_input import DialogInput
from shoppinglist.list_item import ListItem as ListItemWidget

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
        from shoppinglist.main import Application
        super().__init__(**kwargs)
        self.init_template()
        self.category = category
        self.list_store = Gio.ListStore()
        self.win = Application.instance.win
        self.settings = Application.instance._settings

        if category.id == DEFAULT_CATEGORY:
            self.header_box.hide()


        self.new_item_button.connect('clicked', self.handle_new_item)

        self.items_list.bind_model(self.list_store, self.make_list_widget)

        markup = '<span size="large"><b>{text}</b></span>'
        self.category_label.set_markup(markup.format(text=category.name))

        self.load_data()

        self.settings.connect(
            'changed::show-checked', self._on_show_checked_changed)

    def _on_show_checked_changed(self, settings, value):
        self.load_data()

    def filter_by_checked(self, item):
        if self.settings.get_value('show-checked'):
            return True

        return not item.checked

    def load_data(self):
        items = db.get_list_items(self.category.list_id)

        self.list_store.remove_all()
        for item in items:
            if item.category_id == self.category.id and self.filter_by_checked(item):
                self.list_store.append(item)

    def persist_and_reload(self, value):
        db.add_item(self.category.list_id, value, self.category.id)
        self.load_data()

    def handle_new_item(self, btn):
        dialog = DialogInput(self.win)
        dialog.connect('enter_text', lambda _, val: self.persist_and_reload(val))
        dialog.set_placeholder("list name")
        dialog.show_all()

    @staticmethod
    def make_list_widget(data):
        return ListItemWidget(data)
