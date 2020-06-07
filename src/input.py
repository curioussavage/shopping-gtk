from gi.repository import Gtk
from gi.repository import GObject
from .gi_composites import GtkTemplate


@GtkTemplate(ui='/org/gnome/Shoppinglist/input.ui')
class Input(Gtk.Popover):
    __gtype_name__ = 'Input'

    text_field = GtkTemplate.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()


        self.set_default_widget(self.text_field)
        self.text_field.connect('activate', self.handle_text_enter)

    def handle_text_enter(self, text_field):
        text = text_field.get_text()
        self.emit('enter_text', text)
        self.popdown()

    def set_placeholder(self, text):
        self.text_field.set_placeholder_text(text)

    @GObject.Signal(flags=GObject.SignalFlags.RUN_LAST, return_type=str,
                    arg_types=(str,),
                    accumulator=GObject.signal_accumulator_true_handled)
    def enter_text(self, *args):
        value = args[0]
        return value
