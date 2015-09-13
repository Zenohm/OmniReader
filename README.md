# OmniReader
This program will gather text from the inputted source, parse it, and output an audio version of that text using either Google's text-to-speech engine or a local text-to-speech solution.

At the moment this program has only a few supported websites:
  - Fanfiction.net
  - Wattpad
  - Deviantart
  - PDF Books
  - Plain Text

There are two primary components to this program, the OmniReader function and the getStory class.

# OmniReader function
  Responsible for the performing the repetition of tasks required to parse, format, and present text from the implemented websites.
  Any additional websites that are implemented would require a simple `if` statement to be included in the type check performed by this function.
  The design is mostly modular.

# getStory class
  Responsible for analyzing inputted text or urls and determining key qualities about said inputted text or urls.
  Responsible for fetching the text from the websites and providing the functionality to parse the text.
  Mutable, iterable objects can be inputted into this class and it will automatically distribute itself onto each item in the object.

More information to come.
