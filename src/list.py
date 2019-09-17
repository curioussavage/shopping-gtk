from gi.repository import Gtk
from .gi_composites import GtkTemplate


@GtkTemplate(ui='/org/gnome/Shoppinglist/list.ui')
class List(Gtk.ListBoxRow):
    __gtype_name__ = 'List'

    list_name = GtkTemplate.Child()

    def __init__(self, list, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        self.list = list

        #import ipdb; ipdb.set_trace()
        markup = '<span size="large"><b>{text}</b></span>'
        self.list_name.set_markup(markup.format(text=self.list.name))
        
