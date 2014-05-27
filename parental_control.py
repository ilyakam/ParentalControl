from os.path import basename
import sublime, sublime_plugin
import re

# Adds parentheses around the cursor for a given word:
class AddParenthesesCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view

    for selection in view.sel():
      opening_position = None
      closing_position = None

      # Continue to put parentheses around the cursor:
      if selection.empty():
        # Extract word:
        word = view.word(selection)

        # Skip trying to put parentheses around empty words:
        if re.match("\s+", view.substr(word)): continue

        opening_position = word.begin()
        closing_position = word.end() + 1

      # Mimic default behavior:
      else:
        opening_position = selection.begin()
        closing_position = selection.end() + 1

      # Put the parentheses around the selection:
      if opening_position and closing_position:
        view.insert(edit, opening_position, "(")
        view.insert(edit, closing_position, ")")

# Removes parentheses around the cursor in a given line:
class RemoveParenthesesCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view

    # Initialize custom settings:
    pc_settings = sublime.load_settings("Parental Control.sublime-settings")
    syntax = view.settings().get("syntax")
    language = basename(syntax).replace(".tmLanguage", "").lower()
    replace_with = pc_settings.get(language, pc_settings.get("default"))
    parentheses_match = pc_settings.get("parentheses_match")

    # Iterate through each possible selection:
    for selection in view.sel():

      seeking_position = selection.begin()
      opening_position = False
      closing_position = False
      opening_character = None
      closing_character = None
      encounters = {}
      for key in parentheses_match.values():
        encounters[key] = 0

      # Move left until an opening bracket is found:
      while seeking_position >= 0:
        seeking_position -= 1
        character = view.substr(seeking_position)

        # Add the number of closing brackets encountered:
        if character in parentheses_match.values():
          encounters[character] += 1

        # Subtract the number of opening brackets encountered:
        if character in parentheses_match.keys():
          closing_character = parentheses_match.get(character)
          encounters[closing_character] -= 1

          # The true opening bracket is found after all pairs were skipped over:
          if encounters.get(closing_character) < 0:
            opening_position = seeking_position
            opening_character = character
            break

      # Exit if no opening character is found:
      if opening_character is None:
        return

      # Reinstantiate seeking position:
      seeking_position = selection.begin()
      bracket_counter = 0

      # Move right
      while seeking_position < view.size():
        character = view.substr(seeking_position)

        # For each opening bracket encountered, increment the bracket counter:
        if character is opening_character:
          bracket_counter += 1

        # For each closing bracket encountered, increment the bracket counter:
        elif character is closing_character:
          bracket_counter -= 1

          # When the matching closing bracket is found:
          if bracket_counter < 0:
            closing_position = seeking_position
            break

        seeking_position += 1

      # Replace the parentheses:
      if (opening_position >= 0) and (closing_position <= view.size()):
        # Delete the last position first; otherwise closing position
        # must be offset:
        view.replace(edit,
                     sublime.Region(closing_position, closing_position+1),
                     replace_with.get("closing"))
        view.replace(edit,
                     sublime.Region(opening_position, opening_position+1),
                     replace_with.get("opening"))
