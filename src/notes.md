## From reddit
I think you are looking for connect_after rather than just connect. ;-)

i.e.

store.items_changed.connect_after(() => { do_something(); });
You can also use an Idle callback if the timing is still off.

store.items_changed.connect_after(() => { Idle.add(() => { do_something(); return false; }); });
Seems like I will end up adding my own signal.

If the above doesn't work adding your own signal shouldn't be all that bad, maybe

```
public class MyListStore : GLib.ListStore {

    public signal void item_added ();

    public override void append (Object item) {
        base.append(item);
        item_added();
    }

    public override void insert (uint position, Object item) {
        base.insert(position, item);
        item_added();
    }

    public override uint insert_sorted (Object item, CompareDataFunc<Object> compare_func) {
        uint retval = base.insert_sorted(item, compare_func);
        item_added();
        return retval;
    }
}
```
None of that is tested, just off the top of my head, so sorry if it doesn't quite work but it should get you closer.