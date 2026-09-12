"""Integration tests for adding parentheses. See README.md for console usage."""

import unittest

import sublime


class AddParenthesesTests(unittest.TestCase):
  def setUp(self):
    self.window = sublime.active_window()
    self.original_view = self.window.active_view()
    self.view = self.window.new_file()
    self.view.set_scratch(True)
    self.view.settings().set('syntax', 'Packages/Text/Plain text.tmLanguage')

  def tearDown(self):
    self.window.focus_view(self.view)
    self.window.run_command('close_file')
    if self.original_view is not None:
      self.window.focus_view(self.original_view)

  def text(self):
    return self.view.substr(sublime.Region(0, self.view.size()))

  def check(self, marked_text, expected, selections=None):
    text = ''
    cursors = []
    for character in marked_text:
      if character == '|':
        cursors.append(sublime.Region(len(text)))
      else:
        text += character
    self.view.run_command('append', {'characters': text})
    self.view.sel().clear()
    self.view.sel().add_all(cursors if selections is None else selections)
    self.view.run_command('add_parentheses')
    self.assertEqual(self.text(), expected)

  def test_nonempty_selections(self):
    self.check('one plain_word two', '(one) (plain_word) (two)',
               [sublime.Region(0, 3), sublime.Region(4, 14), sublime.Region(15, 18)])

  def test_reversed_selections(self):
    self.check('one plain_word two', '(one) (plain_word) (two)',
               [sublime.Region(3, 0), sublime.Region(14, 4), sublime.Region(18, 15)])

  def test_whole_buffer_selection(self):
    self.check('one two', '(one two)', [sublime.Region(0, 7)])

  def test_explicit_whitespace_selection(self):
    self.check('  one', '(  )one', [sublime.Region(0, 2)])

  def test_undo_redo(self):
    self.check('o|ne t|wo', '(one) (two)')
    self.view.run_command('undo')
    self.assertEqual(self.text(), 'one two')
    self.view.run_command('redo')
    self.assertEqual(self.text(), '(one) (two)')


CASES = [
  ('first_word', 'o|ne', '(one)'),
  ('cursor_at_zero', '|one', '(one)'),
  ('cursor_at_word_end', 'one|', '(one)'),
  ('screenshot', 'on|e p|lain_word t|wo end\n\nhe|llo, |world',
   '(one) (plain_word) (two) end\n\n(hello), (world)'),
  ('later_word', 'one t|wo', 'one (two)'),
  ('second_line', 'one\nt|wo', 'one\n(two)'),
  ('leading_whitespace', '  o|ne', '  (one)'),
  ('underscore', 'plain_|word', '(plain_word)'),
  ('unicode', 'ca|fé', '(café)'),
  ('empty_buffer', '|', ''),
  ('whitespace_at_zero', '|   ', '   '),
  ('whitespace_only', ' |  ', '   '),
  ('blank_line', 'one\n|\ntwo', 'one\n\ntwo'),
  ('whitespace_before_word', ' |  o|ne', '   (one)'),
]


def make_test(marked_text, expected):
  def test(self):
    self.check(marked_text, expected)
  return test


for name, marked_text, expected in CASES:
  setattr(AddParenthesesTests, 'test_' + name, make_test(marked_text, expected))


if __name__ == '__main__':
  suite = unittest.defaultTestLoader.loadTestsFromTestCase(AddParenthesesTests)
  result = unittest.TextTestRunner(verbosity=2).run(suite)
  print('Add parentheses: {0} tests, {1} failures, {2} errors, ST {3}'.format(
    result.testsRun, len(result.failures), len(result.errors), sublime.version()))
