OmniReader
===
This program will gather text from the inputted source, parse it, and output an audio version of that text using either Google's text-to-speech engine or a local text-to-speech solution.

Install
---

Run one of these two commands from the command line.

    pip install https://github.com/Zenohm/OmniReader/archive/master.zip
or

    cd <Install Directory>
    python setup.py install

Supported Websites
---

At the moment this program has only a few supported websites:
  - Fanfiction.net
  - Wattpad - In Progress after recent update
  - Deviantart
  - PDF Books
  - Plain Text

There are two primary components to this program, the OmniReader function and the getStory class.

OmniReader function
---
  Responsible for the performing the repetition of tasks required to parse, format, and present text from the implemented websites.
  Any additional websites that are implemented would require a simple `if` statement to be included in the type check performed by this function.
  The design is mostly modular.

getStory class
---
  Responsible for analyzing inputted text or urls and determining key qualities about said inputted text or urls.
  Responsible for fetching the text from the websites and providing the functionality to parse the text.
  Mutable, iterable objects can be inputted into this class and it will automatically distribute itself onto each item in the object.

Current methods
---

 The `OmniReader` object currently has the following methods:
 
  - `say(text, title, speech_system, say, lang)`
  - `getStory(text|url)`

In-depth Explanations
---

 The `say()` method has only one parameter which requires an argument to be passed to it, the `text` parameter. 
 Otherwise:
 
  - `title`, which determines the filename, defaults to `Speak`, the filetype is, by default, an `.mp3` or a `.vbs`
  - `speech_system`, which determines whether the Google text-to-speech system or a local solution should be used, defaults to `google`
  - `say`, which determines whether the result should be spoken after it is done downloading, defaults to `True`
  - `lang`, which determines the voice's native language, defaults to `en` or English

The `getStory` class can be passed a valid URL or text segment, or list of either. Either way, the text must be initialized.
 These are the different methods or properties currently built into the class:
 
  - `initialize` will use the determined story type to gather the text from a valid website and determine the language of the text.
  - `text` holds the story text after the story has been initialized
  - `translate(target_language)` a method of `getStory`, simply enter the language code [(codes listed here)](https://cloud.google.com/translate/v2/using_rest?hl=en#language-params) as a string for the language you want to translate to. The result will be stored in `text`.

Usage Example
---

    import OmniReader
    url = "https://www.fanfiction.net/s/11263086/1/Test"
    story = OmniReader.getStory(url)
    story.initialize
    OmniReader.say(story.text) # Opens the default media player and reads the story
    story.translate('es') # Translate to Spanish
    OmniReader.say(story.text) # Opens the default media player and reads the story in Spanish
