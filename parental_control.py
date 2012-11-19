import sublime, sublime_plugin

# Adds parentheses around the current word:
class AddParenthesesCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    
    for selection in view.sel():
      opening_position = False
      closing_position = False
      
      # Continue to put parentheses around the word:
      if selection.empty():
        opening_position = view.word(selection).begin()
        closing_position = view.word(selection).end() + 1
        
      # Put paretheses around the entire selection, mimicking the default behavior:
      else:
        opening_position = selection.begin()
        closing_position = selection.end() + 1
      
      if opening_position and closing_position:
        view.insert(edit, opening_position, "(")
        view.insert(edit, closing_position, ")")

# Removes parentheses around the cursor in a given line:
class RemoveParenthesesCommand(sublime_plugin.TextCommand):
  parentheses_types = ["(", "[", "{"]
  parentheses_match = {"(": ")",
                       "[": "]",
                       "{": "}"}
  
  def run(self, edit):
    view = self.view
    
    for selection in view.sel():
      # Skip processing selected text -- that'll overwrite default behavior:
      if not selection.empty(): continue
      
      seeking_position = selection.begin()
      opening_position = False
      closing_position = False
      closing_matching = False # the matching closing parentheses
      
      # Look backwards until you find a parentheses:
      while seeking_position > 0:
        seeking_position -= 1
        point             = view.substr(seeking_position)
        
        # If opening parentheses found
        if point in self.parentheses_types:
          closing_matching = self.parentheses_match[point]
          opening_position = seeking_position
          break
      
      # Stop processing this selection if no opening parentheses found:
      if not closing_matching or not opening_position: continue
      
      # Reinitialize the seeking position:
      seeking_position = selection.begin()
      
      # Stop processing this selection if we're outside the matching parentheses:
      while seeking_position > opening_position:
        seeking_position -= 1
        if view.substr(seeking_position) == closing_matching:
          opening_position = False
          break
        
      # Reinitialize the seeking position:
      seeking_position = selection.begin()
      
      # Look forward through EOF until you find a matching closing parentheses:
      while closing_matching and seeking_position < view.size():
        point = view.substr(seeking_position)
        
        if point == closing_matching:
          closing_position = seeking_position
          break
        
        seeking_position += 1
      
      # Actually replace the parentheses pair with a space and an empty character:
      if opening_position and closing_position:
        view.replace(edit, sublime.Region(opening_position, opening_position + 1), " ")
        view.replace(edit, sublime.Region(closing_position, closing_position + 1), "")
