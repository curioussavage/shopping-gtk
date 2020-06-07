from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Gdk
from .gi_composites import GtkTemplate


@GtkTemplate(ui='/org/gnome/Shoppinglist/dialog_input.ui')
class DialogInput(Gtk.Window):
    __gtype_name__ = 'DialogInput'

    dialog_input_entry = GtkTemplate.Child()

    def __init__(self, parent_win, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

        self.set_transient_for(parent_win)
        self.dialog_input_entry.connect('activate', self.handle_text_enter)
        self.connect('key_press_event', self.handle_keys)

        self.connect_after('enter_text', self.handle_after)


    def handle_after(self, w, bar):
        # lets just cleanup for our users
        self.destroy()

    def handle_keys(self, w, event_key):
        if event_key.keyval == Gdk.KEY_Escape:
            self.hide()

    def handle_text_enter(self, dialog_input_entry):
        text = dialog_input_entry.get_text()
        self.emit('enter_text', text)
        self.destroy()

    def set_placeholder(self, text):
        self.dialog_input_entry.set_placeholder_text(text)

    @GObject.Signal(flags=GObject.SignalFlags.RUN_LAST, return_type=str,
                    arg_types=(str,),
                    accumulator=GObject.signal_accumulator_true_handled)
    def enter_text(self, *args):
        value = args[0]
