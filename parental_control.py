import sublime, sublime_plugin

# Removes parentheses around the cursor in a given line:
class RemoveParenthesesCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view       = self.view
    selections = view.sel() # the cursor position in each multiline selection
    
    for selection in selections:
      # Skip processing selected text -- that'll overwrite default behavior:
      if not selection.empty(): continue
      
      seeking_position = selection.begin()
      end_of_file      = view.size()
      
      # TODO: Convert to hash with start, end, and bracket:
      # e.g.: {start: 11, end: 15, bracket: "["}
      left_bracket = right_bracket = False
      
      # Look backwards until you find a parentheses:
      while seeking_position > 0:
        seeking_position -= 1
        if view.substr(seeking_position) == "(":
          left_bracket = seeking_position
          break
      
      seeking_position = selection.begin()
      
      # Look forward until you find a parentheses:
      while seeking_position < end_of_file:
        seeking_position += 1
        if view.substr(seeking_position) == ")":
          right_bracket = seeking_position
          break
      
      if left_bracket and right_bracket:
        view.replace(edit, sublime.Region(left_bracket, left_bracket + 1),  " ")
        view.replace(edit, sublime.Region(right_bracket, right_bracket + 1), "")
