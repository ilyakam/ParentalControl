"""Integration tests for the loaded plugin. See README.md for console usage."""

import copy
import unittest

import sublime


class RemoveParenthesesTests(unittest.TestCase):
  def setUp(self):
    self.window = sublime.active_window()
    self.original_view = self.window.active_view()
    self.view = self.window.new_file()
    self.view.set_scratch(True)
    self.view.settings().set('syntax', 'Packages/Text/Plain text.tmLanguage')
    self.settings = sublime.load_settings('Parental Control.sublime-settings')
    self.saved_settings = {}
    for key, value in {
      'parentheses_match': {'(': ')', '[': ']', '{': '}'},
      'default': {'opening': '', 'closing': ''},
      'plain text': {'opening': '', 'closing': ''}
    }.items():
      self.saved_settings[key] = (self.settings.has(key),
                                  copy.deepcopy(self.settings.get(key)))
      self.settings.set(key, value)

  def tearDown(self):
    for key, (existed, value) in self.saved_settings.items():
      if existed:
        self.settings.set(key, value)
      else:
        self.settings.erase(key)
    self.window.focus_view(self.view)
    self.window.run_command('close_file')
    if self.original_view is not None:
      self.window.focus_view(self.original_view)

  def text(self):
    return self.view.substr(sublime.Region(0, self.view.size()))

  def check(self, marked_text, expected, selections=None):
    # A pipe marks a cursor and is omitted from the actual buffer.
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
    self.view.run_command('remove_parentheses')
    self.assertEqual(self.text(), expected)

  def test_nonempty_selections(self):
    self.check('(one) plain_word (two) end', 'one plain_word two end',
               [sublime.Region(1, 4), sublime.Region(6, 16), sublime.Region(18, 21)])
    self.assertEqual([self.view.substr(s) for s in self.view.sel()],
                     ['one', 'plain_word', 'two'])

  def test_reversed_selections(self):
    self.check('(one) plain_word (two) end', 'one plain_word two end',
               [sublime.Region(4, 1), sublime.Region(16, 6), sublime.Region(21, 18)])
    self.assertEqual([self.view.substr(s) for s in self.view.sel()],
                     ['one', 'plain_word', 'two'])

  def test_cursor_positions(self):
    self.check('(o|ne) pla|in_word (|two) end', 'one plain_word two end')
    self.assertEqual([(s.a, s.b) for s in self.view.sel()], [(1, 1), (7, 7), (15, 15)])

  def test_language_replacement(self):
    # Exercise the same replacement as CoffeeScript without requiring its syntax.
    self.settings.set('plain text', {'opening': ' ', 'closing': ''})
    self.check('f(o|ne) pla|in_word g(t|wo)', 'f one plain_word g two')

  def test_long_replacements(self):
    self.settings.erase('plain text')
    self.settings.set('default', {'opening': 'OPEN', 'closing': 'CLOSE'})
    self.check('(o|ne) pla|in_word (t|wo)', 'OPENoneCLOSE plain_word OPENtwoCLOSE')

  def test_custom_brackets(self):
    self.settings.set('parentheses_match', {'<': '>'})
    self.check('<o|ne> pla|in_word <t|wo>', 'one plain_word two')

  def test_nested_long_replacements(self):
    self.settings.set('plain text', {'opening': 'OPEN', 'closing': 'CLOSE'})
    self.check('pla|in_word ((o|ne) t|wo) end',
               'plain_word OPENOPENoneCLOSE twoCLOSE end')

  def test_nested_language_replacement(self):
    self.settings.set('plain text', {'opening': ' ', 'closing': ''})
    self.check('f(o|ne g(t|wo)) end', 'f one g two end')

  def test_undo_redo(self):
    original = '(one) plain_word (two) end'
    expected = 'one plain_word two end'
    self.check('(o|ne) pla|in_word (t|wo) end', expected)
    self.view.run_command('undo')
    self.assertEqual(self.text(), original)
    self.view.run_command('redo')
    self.assertEqual(self.text(), expected)

  def test_add_parentheses_unchanged(self):
    self.view.run_command('append', {'characters': ' one two'})
    self.view.sel().clear()
    self.view.sel().add_all([sublime.Region(2), sublime.Region(6)])
    self.view.run_command('add_parentheses')
    self.assertEqual(self.text(), ' (one) (two)')


CASES = [
  ('issue_7', '(o|ne) pla|in_word (t|wo) end', 'one plain_word two end'),
  ('invalid_first', 'pla|in_word (o|ne) (t|wo)', 'plain_word one two'),
  ('invalid_last', '(o|ne) (t|wo) pla|in_word', 'one two plain_word'),
  ('consecutive_invalid', '(o|ne) a|bc d|ef (t|wo)', 'one abc def two'),
  ('alternating', 'a|bc (o|ne) d|ef [t|wo] g|hi {th|ree}', 'abc one def two ghi three'),
  ('all_invalid', 'o|ne pla|in_word t|wo', 'one plain_word two'),
  ('empty_buffer', '|', ''),
  ('buffer_start', '|(o|ne)', 'one'),
  ('buffer_end', '(o|ne)|', 'one'),
  ('single_pair', '(o|ne)', 'one'),
  ('opening_at_zero', '(|one)', 'one'),
  ('cursor_at_closing', '(one|)', 'one'),
  ('empty_pair', '(|)', ''),
  ('adjacent_pairs', '(o|ne)(t|wo)', 'onetwo'),
  ('square_and_curly', '[o|ne] pla|in_word {t|wo}', 'one plain_word two'),
  ('nested_innermost', '((o|ne))', '(one)'),
  ('nested_mixed', '({[o|ne]})', '({one})'),
  ('nested_outer_before_inner', '(o|ne (t|wo)) end', 'one two end'),
  ('nested_outer_after_inner', '((o|ne) t|wo) end', 'one two end'),
  ('nested_distinct_after_invalid', 'pla|in_word ((o|ne) t|wo) end', 'plain_word one two end'),
  ('nested_mixed_multiple', '{o|ne [t|wo (th|ree)]} end', 'one two three end'),
  ('nested_after_invalid', 'pla|in_word ((o|ne))', 'plain_word (one)'),
  ('enclosing_completed_pair', '(one (two) th|ree)', 'one (two) three'),
  ('duplicate_pair', '(o|ne t|wo)', 'one two'),
  ('duplicate_nested_pair', '((o|ne t|wo))', '(one two)'),
  ('duplicates_with_distinct_nested', '(o|ne (t|wo) th|ree) end', 'one two three end'),
  ('several_nested_pairs', '(o|ne (t|wo)) [th|ree {fo|ur}]', 'one two three four'),
  ('duplicates_after_invalid', 'pla|in_word ((o|ne t|wo))', 'plain_word (one two)'),
  ('multiline', '(o|ne)\npla|in_word\n(t|wo)', 'one\nplain_word\ntwo'),
  ('pair_spans_lines', '(one\nt|wo)', 'one\ntwo'),
  ('unicode_content', '(caf|é) pla|in_word [世|界]', 'café plain_word 世界'),
  ('unmatched_closing', 'str|ay) (o|ne)', 'stray) one'),
  ('unmatched_opening', 'prefix (uncl|osed', 'prefix (unclosed'),
  ('unmatched_after_invalid', 'pla|in_word (uncl|osed', 'plain_word (unclosed'),
  ('unmatched_before_valid', 'prefix (uncl|osed [o|ne]', 'prefix (unclosed one'),
  ('missing_outer_closing', '((o|ne) ta|il', '(one tail'),
]


def make_test(marked_text, expected):
  def test(self):
    self.check(marked_text, expected)
  return test


for name, marked_text, expected in CASES:
  setattr(RemoveParenthesesTests, 'test_' + name, make_test(marked_text, expected))


if __name__ == '__main__':
  suite = unittest.defaultTestLoader.loadTestsFromTestCase(RemoveParenthesesTests)
  result = unittest.TextTestRunner(verbosity=2).run(suite)
  print('ParentalControl: {0} tests, {1} failures, {2} errors, ST {3}'.format(
    result.testsRun, len(result.failures), len(result.errors), sublime.version()))
