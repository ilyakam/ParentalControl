import sublime, sublime_plugin

# Removes parentheses around the cursor in a given line:
class RemoveParenthesesCommand(sublime_plugin.TextCommand):
  parentheses_types = ["(", "[", "{"]
  parentheses_match = {"(":")",
                       "[":"]",
                       "{":"}"}
  
  def run(self, edit):
    # TODO:
    # - Clean up variable names:
    #   - Use position hash
    #   - Rename all brackets to parentheses
    # - Reorganize code blocks with defined functions
    # - Try to be more DRY
    
    view       = self.view
    selections = view.sel() # the cursor position in each multiline selection
    
    for selection in selections:
      # Skip processing selected text -- that'll overwrite default behavior:
      if not selection.empty(): continue
      
      seeking_position = selection.begin()
      end_of_file      = view.size()
      
      left_bracket        = False
      right_bracket       = False
      closing_parentheses = False
      
      # Look backwards until you find a parentheses:
      while seeking_position > 0:
        seeking_position -= 1
        point             = view.substr(seeking_position)
        
        if point in self.parentheses_types:
          closing_parentheses = self.parentheses_match[point]
          left_bracket = seeking_position
          break
      
      # Stop processing this selection if no opening parentheses found:
      if not closing_parentheses or not left_bracket: continue
      
      # Reinitialize the seeking position:
      seeking_position = selection.begin()
      
      # Stop processing this selection if we're outside the matching parenthesis:
      while seeking_position > left_bracket:
        seeking_position -= 1
        if view.substr(seeking_position) == closing_parentheses:
          left_bracket = False
          break
        
      # Reinitialize the seeking position:
      seeking_position = selection.begin()
      
      # Look forward until you find a parentheses:
      while closing_parentheses and seeking_position < end_of_file:
        point = view.substr(seeking_position)
        
        if point == closing_parentheses:
          right_bracket = seeking_position
          break
        
        seeking_position += 1
      
      # Actually replace the brackets with a space and an empty character:
      if left_bracket and right_bracket:
        view.replace(edit, sublime.Region(left_bracket, left_bracket + 1),  " ")
        view.replace(edit, sublime.Region(right_bracket, right_bracket + 1), "")
