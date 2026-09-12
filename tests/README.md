# ParentalControl integration tests

These tests run the installed commands in real Sublime Text scratch views, using
its selection, edit, settings, and undo APIs. Run them with the development
checkout loaded as `Packages/ParentalControl`.

Open **View > Show Console** and run:

For removal:

```python
import os; path = os.path.join(sublime.packages_path(), 'ParentalControl', 'tests', 'test_remove_parentheses.py'); exec(compile(open(path, encoding='utf-8').read(), path, 'exec'), {'__name__': '__main__'})
```

For addition:

```python
import os; path = os.path.join(sublime.packages_path(), 'ParentalControl', 'tests', 'test_add_parentheses.py'); exec(compile(open(path, encoding='utf-8').read(), path, 'exec'), {'__name__': '__main__'})
```

The console prints each result and a summary. The suite closes its scratch views,
restores the previously active view, and restores all settings it overrides in
memory. It does not save settings to disk. No third-party test packages are needed.

Coverage includes issue #7 with empty and nonempty selections, cursor positions,
invalid cursors before and after valid ones, incomplete pairs, nested pairs,
duplicate pairs, all default bracket types, custom delimiters, language-specific
and longer replacement strings, Unicode text, multiline text, and undo/redo.
The addition suite covers words and selections at position zero, multiple cursors,
empty buffers, blank lines, and whitespace handling.
