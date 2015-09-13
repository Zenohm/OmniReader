"""
Special thanks to all the people at CodeReview
who helped me optimize and improve my code!
"""

"""
Current bug list:
1. say() fails to work in command line.
2. Text causes problems with certain HTML tags on fanfiction.net
3. PDF doesn't always work correctly (No spaces sometimes) and
    when it does it cycles through pages as fast as it can.
"""


import os
import sys
import time
import webbrowser
from subprocess import call
from importlib import import_module
from textwrap import fill
from platform import python_version

home = os.path.expanduser("~")
speech_system = 'google'


if '2.' == python_version()[:1]:
    print("This program requires Python 3 in order to properly function.\n"
          "A backwards compatible version may be available in the future.")
    input("End of line.")
    sys.exit()
else:
    try:
        from urllib.request import urlopen
    except ImportError:
        from urllib import urlopen


def import_or_install(module, package, description, capability):
    """Import module. If it fails to import, prompt user to install
    package and try again. The description argument gives a brief
    human-readable description of the module, and capability gives a
    human-readable description of what it can do.
    """
    try:
        import_module(module)
    except ImportError:
        print(fill("Your system does not have {} installed. "
                   "Without this module, this process will not {}."
                   .format(description, capability)))
        answer = input("Do you want to install it?")
        if answer.startswith(('Y', 'y')):
            call([sys.executable, '-m', 'pip', 'install',
                 '--upgrade', package])
            import_module(module)
        else:
            raise


import_or_install('gtts', 'gTTS', 'Google Text to Speech API',
                  'sound natural')
from gtts import gTTS

import_or_install('bs4', 'beautifulsoup4', 'Beautiful Soup',
                  'be able to pull text from websites')
from bs4 import BeautifulSoup

import_or_install('PyPDF2', 'PyPDF2', 'PyPDF2',
                  'be able to process PDF files')
import PyPDF2

import_or_install('ftfy', 'ftfy', 'the smart Python unicode fixer',
                  'sometimes say odd things or crash.')
import ftfy

import_or_install('unidecode', 'unidecode', 'the last resort unicode parser',
                  'will likely crash if it finds a special character.')
import unidecode


def continue_question(intro_text='reached the end',
                      end_text='start another story'):
    answer = input("You have " + intro_text +
                   ", do you want to " + end_text + "? ")
    if answer == '1' or answer.startswith(('Y', 'y')):
        return True
    else:
        return False


def say(message, title='Speak', speech_system='google', say=True):
    if speech_system == 'google':
        try:
            # Create the MP3 file which will speak the text
            title += '.mp3'
            tts = gTTS(message)
            tts.save(home+'\\'+title)
            if say:
                call("start /MIN {}".format(home+'\\'+title), shell=True)
        except Exception:
            print("Vocalization failed.")
    else:
        try:
            # Create the Visual Basic code which will speak the text
            with open(title + '.vbs', 'w') as file:
                file.write(
                        """
                        speaks="{}"
                        Dim speaks, speech
                        Set speech=CreateObject("sapi.spvoice")
                        speech.Speak speaks
                        """
                        .format(
                            str(message).replace('"', '').replace('\n', '')))
            # Execute the file
            call(['cscript.exe', title + '.vbs'])
        except Exception:
            print("Vocalization failed.")


class HumorousError(Exception):
    pass


class getStory:
    """
    This class handles the retrieval and classification
    of text from the various websites or formats.
    Now can handle mutable iterables.
    ---------------------------------------------------------
    Supported Websites/Filetypes:
        * Fanfiction.net
        * Wattpad
        * Deviantart
        * PDF Books - Tenuous
        * Plain Text
    ---------------------------------------------------------
    Attributes:
        url: Inputted string representing a story
        speech: Speech to text system to be used
            local: Local system solution
            google: Google text to speech engine
        text: Initially equal to url, set to story text after
                initialization is performed.
        chapters: On fanfiction, holds a list of chapters
        initialized: Whether the story has retrieved its text
        type: What is the input, where does it lead?
            wattpad: http://wattpad.com
            fanficton: http://fanfiction.net
            deviantart: http://deviantart.com
            pdf: Can be stored online or locally
            text: Plain text to be read, fallback type
            iterable: Objects like a list with multiple items
        pathtype: Is it stored online or locally?
            url: Online
            local: Locally
    """
    def __init__(self, url):
        self.url = url
        self.speech = speech_system
        self.text = url
        self.chapters = []
        self.initialized = False
        if not hasattr(self.url, '__iter__') or isinstance(self.url, str):
            if 'wattpad' in self.url:
                self.type = 'wattpad'
            elif 'fanfiction' in self.url and 'wattpad' not in self.url:
                self.type = 'fanfiction'
            elif 'deviantart' in self.url:
                self.type = 'deviantart'
            elif 'pdf' in self.url:
                self.type = 'pdf'
            else:
                self.type = 'text'
            if url.startswith(('http://', 'https://')):
                self.pathtype = 'url'
            else:
                self.pathtype = 'local'
                if '.com' in url or '.net' in url:
                    self.url = 'http://' + url
                    self.pathtype = 'url'
        else:
            self.type = 'iterable'
            self.backup = self.url
            map_class = [getStory(each_url) for each_url in self.url]
            self.url = map_class

    def __bool__(self):
        return self.initialized

    def __add__(self, other):
        return self.text + other

    def __radd__(self, other):
        return other + self.text

    def __lt__(self, other):
        return len(self.text) < other

    def __le__(self, other):
        return len(self.text) <= other

    def __eq__(self, other):
        return len(self.text) == other

    def __ne__(self, other):
        return len(self.text) != other

    def __gt__(self, other):
        return len(self.text) > other

    def __ge__(self, other):
        return len(self.text) >= other

    def __getitem__(self, index):
        if index > len(self.url) - 1:
            raise IndexError
        return self.url[index]

    def __iter__(self):
        return iter(self.url)

    def __len__(self):
        return len(self.text)

    def initialize(self):
        """
        Automatically detects and initializes the
        different types of stories that can be
        inputted.
        """
        if self.type == 'wattpad':
            self.wattpad()
        elif self.type == 'fanfiction':
            self.fanfiction()
        elif self.type == 'deviantart':
            self.deviantart()
        elif self.type == 'pdf':
            self.pdf_initialize()
        else:
            self.initialized = True
            pass

    def fanfiction(self):
        """
        Retrieves and parses text from a Fanfiction.net story.
        Will attempt to grab a chapter list.
        """
        # Opens and parses the URL with BeautifulSoup
        soup = BeautifulSoup(urlopen(str(self.url)))
        # Retrieve story text from the URL to be used elsewhere
        try:
            self.text = soup.find(class_='storytext').text
            # Following code will grab the number of chapters for later use.
            options = str(soup.select('#chap_select')[0].option)
            penultimate_chapter = options.split('option value="')[::-1][1]
            last_chapter = int(penultimate_chapter.split('"')[0]) + 1
            self.chapters = list(map(str, range(-1, last_chapter + 1)))
            self.initialized = True
            # This code tries to get chapter names, doesn't always work
            # options = soup.select('#chap_select')[0].option.text
            # options_modified = options
            # for char in range(len(options)):
            #    if options[char].isdigit() and options[char + 1] == '.':
            #        options_modified = options_modified.replace(
            #            options[char], "~$~" + options[char]
            #            )
            # self.chapters = options_modified.split('~$~')[1:]
        except Exception:
            print('Retrieval Failed.')

    def deviantart(self):
        """
        Retrieves text from Deviantart stories.
        """
        try:
            soup = BeautifulSoup(urlopen(str(self.url)))
            self.text = soup.select('#devskin >'
                                    ' div > div >'
                                    ' div.gr-body >'
                                    ' div > div >'
                                    ' div')[0].text
            self.initialized = True
        except Exception:
            print('Retrieval Failed.')

    def wattpad(self, page=0, mode='singular'):
        """
        Retrieve text from Wattpad stories given a page
        number and a mode type.
        Mode types are singular and plural.
        """
        # Sets up the page variable to be added onto the URL
        page = '/page/' + str(page) if page else ''
        soup = BeautifulSoup(urlopen(str(self.url + page)))
        # Finds the path and contents given by the search
        if mode == 'singular':
            self.text = soup.find(class_="panel panel-reading")
        elif mode == 'plural':
            self.text = soup.find_all(class_="panel panel-reading")
        self.initialized = True

    def pdf_initialize(self):
        """
        Sets up the retrieval of text from a PDF,
        whether stored online or locally.
        """
        try:
            os.remove(os.getcwd() + '\\PDF2BEREAD.pdf')
        except FileNotFoundError:
            pass
        if self.pathtype == 'url':
            # Download the PDF from the web
            path = urlopen(self.url)
            with open('PDF2BEREAD.pdf', 'wb') as file:
                file.write(path.read())
            self.url = os.getcwd() + '\\PDF2BEREAD.pdf'
        self.initialized = True

    def pdf(self, page):
        """
        Retrieves text from a PDF document, stored locally or online.
        """
        page = PyPDF2.PdfFileReader(self.url).getPage(page)
        self.text = page.extractText().replace('\u2122', "'")

    def parse(self):
        """
        Removes all unicode characters, nonprintable characters,
        and unneeded special characters.
        Also formats text for audio reading.
        """
        try:
            text = ftfy.fix_text(self.text)
            self.text = unidecode.unidecode(text).replace('[?]', '')
        except Exception:
            text = bytes(self.text, 'utf-8')
            text = text.decode('unicode_escape')
            text = text.encode('ascii', 'ignore')
            text = text.decode('utf-8')
            self.text = str(text)
        # Removes newline and return characters
        changes = {
            '\n': ' ',
            '\r': ' ',
            '"': "'",
            '.': '. ',
            '.   .   . ': '',
            "\'": '',
            '\"': '',
            ':': ': ',
            ':  ': ': ',
            '!': '! ',
            '!  ': '! ',
            '?': '? ',
            '?  ': '? ',
            ';': '; ',
            ';  ': '; ',
            '. . .': '...',
            '0': '0 ',
            '1': '1 ',
            '2': '2 ',
            '3': '3 ',
            '4': '4 ',
            '5': '5 ',
            '6': '6 ',
            '7': '7 ',
            '8': '8 ',
            '9': '9 '
                  }
        if self.speech == 'local':
            changes.update({
                       'Tali': 'Tahlie',
                       'tali': 'tahlie',
                       'Yalo': ' Yah-lo ',
                       'caf ': 'cafe ',
                       'Garrus': 'Gae-rrus',
                       'Klenon': 'Klenn une',
                       'Binary': 'Bi-nary',
                       'Noveria': ' No-veir-eaah ',
                       'Vakarian': 'Vah-kare-eean'
                      })
        else:
            changes.update({
                       'Tali': 'Tahhlee',
                       'tali': 'Tahhlee',
                       'caf ': 'cafe '
                      })
        for original_word, changed_word in changes.items():
            self.text = self.text.replace(original_word, changed_word)


def OmniReader(text, *, change_type=False):
    """

    "Drive me closer, I want to hit them with my superfunction."
    This function will gather text from the inputted source,
    parse it, and output an audio version of that text using
    either Google's text-to-speech engine or a local TTS
    solution.
    The audio versions will be stored in the
    ~/Users/USERNAME/
    path as either .MP3s or as .VBS files.

    change_type
        A variable which allows the user to set the story
        type manually from the command line.

    """
    story = getStory(text)
    if change_type:
        story.type = change_type
    if story.type == 'wattpad':
        if sys.argv[0] and len(sys.argv) == 2:
            raise SyntaxError(
                "Please input the number of pages in this story.")
        elif sys.argv[0] and len(sys.argv) == 3:
            if sys.argv[2]:
                number_of_pages = int(sys.argv[2])+1
        else:
            number_of_pages = int(
                input("How many pages are in the story: ")) + 1
        # Iterates through the pages of the story
        for each_page in range(number_of_pages):
            if each_page:
                # Designed to cope with Wattpad's weird multi-page system
                story.wattpad(each_page, 'plural')[1]
            else:
                # Meant for the first page because **** Wattpad
                story.wattpad()
            paragraphs = story.text.find_all('p')
            # Iterates through the paragraphs in each page of the story
            for each_paragraph in range(len(paragraphs)):
                # Get all the text segments
                paragraphs[each_paragraph] = paragraphs[each_paragraph].text
            story.text = ' '.join(paragraphs)
            story.parse()
            print(story.text)
            say(story.text, speech_system=speech_system)
            return continue_question()

    elif story.type == 'fanfiction':
        """
        Iterate through each chapter in a fanfiction
        and save the audio recording of each.
        """
        story.text = "No data available."
        story.fanfiction()
        url = story.url.split('/')
        for each_chapter in range(int(url[-2]), int(story.chapters[-1]) + 1):
            url = story.url.split('/')
            story.fanfiction()
            # Set up the name for each audio recording
            title = url[-1] + '_' + url[-2]
            if not os.path.exists(url[-1]):
                os.makedirs(url[-1])
            print("Processing story text...")
            story.parse()
            print("Downloading audio file, " + title)
            if speech_system == 'local':
                say(story.text,
                    url[-1] +
                    '\\' +
                    str(int(story.chapters[each_chapter]) + 1),
                    speech_system,
                    False)
            else:
                say(story.text,
                    url[-1] +
                    '\\' +
                    str(int(story.chapters[each_chapter]) + 1),
                    speech_system,
                    False)
            # Iterate to the next chapter and reset the URL
            url[-2] = str(int(url[-2]) + 1)
            print("Continuing to next chapter...")
            story.url = '/'.join(url)
        return continue_question('finished recording')

    elif story.type == 'pdf':
        story.pdf_initialize()
        if sys.argv[0] and len(sys.argv) == 2:
            raise SyntaxError("Please input the beginning page.")
        elif sys.argv[0] and len(sys.argv) == 3:
            if sys.argv[2]:
                first_page = int(sys.argv[2])-1
        else:
            first_page = int(input("Please enter the beginning page: ")) - 1
        for each_page in range(
            first_page,
            PyPDF2.PdfFileReader(story.url).getNumPages()
                              ):
            story.pdf(each_page)
            print('\n \t \t' + str(each_page + 1) + '\n')
            story.parse()
            print(story.text)
            say(story.text, speech_system=speech_system)
        return continue_question()

    elif story.type == 'deviantart':
        story.deviantart()
        url = story.url.split('/')
        title = url[-1]
        print("Processing story text...")
        story.parse()
        print("Creating audio file.")
        say(story.text, title, speech_system)
        return continue_question('finished recording')

    elif story.type == 'text':
        print('\n' + story.text)
        story.parse()
        say(story.text, speech_system=speech_system)
        return continue_question('finished speaking', 'say something else')


def main():
    try:
        say("Initializing...")
    except Exception:
        speech_system = 'local'
        try:
            say("Initializing...", speech_system=speech_system)
        except Exception:
            webbrowser.open_new('https://www.youtube.com/watch?v=WlBiLNN1NhQ')
            raise HumorousError("Life's a piece of shit.")
    reading = True
    while reading:
        if sys.argv[0] and len(sys.argv) > 1:
            text = sys.argv[1]
            reading = OmniReader(text)
        else:
            text = input("State your request: ")
            reading = OmniReader(text)


if __name__ == "__main__":
    main()
