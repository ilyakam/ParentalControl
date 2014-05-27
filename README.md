# ParentalControl - A Sublime Text Plugin #

A plugin for [Sublime Text](http://www.sublimetext.com/) that allows you to easily add and remove parentheses around words and expressions.

It is particularly useful in languages where parentheses are optional under certain circumstances, such as in [CoffeeScript](http://www.coffeescript.org/).

## Usage ##

#### OSX ####

* **Command + Shift + (** to create parentheses around the current word.
* **Command + Shift + )** to remove parentheses around the cursor.

#### Windows / Linux ####

* **Control + Shift + (** to create parentheses around the current word.
* **Control + Shift + )** to remove parentheses around the cursor.

## Changelog ##

#### v1.1.2 ####

* Fixed bug when cursor is on position 0 or in-between parenthesis sets.

#### v1.1.1 ####

* Fixed complex and nested parentheses.
* Fixed parentheses starting on position 0.
* More refactoring, cleanup, and comments.

#### v1.1.0 ####

* Ensured compatibility with [ST3](http://www.sublimetext.com/3).
* Added syntax and language aware settings file.
* Refactored code and fixed some miscellaneous bugs with `RemoveParentheses`.

#### v1.0.0 ####

* Initial release.

## License ##

Copyright (c) 2014 Ilya Kaminsky

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
