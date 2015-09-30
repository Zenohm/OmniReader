import ftfy
import PyPDF2
import unidecode
from bs4 import BeautifulSoup
from urllib.request import urlopen

try:
    from __main__ import speech_system
except ImportError:
    speech_system = 'google'


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
        self.changes = {}
        if not hasattr(self.url, '__iter__') or type(self.url) is str:
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
    
    def __repr__(self):
        return "Story({})".format(self.url)

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
    
    @property
    def initialize(self):
        """
        Automatically detects and initializes the
        different types of stories that can be
        inputted.
        """
        if self.type == 'wattpad':
            self.wattpad
        elif self.type == 'fanfiction':
            self.fanfiction
        elif self.type == 'deviantart':
            self.deviantart
        elif self.type == 'pdf':
            self.pdf_initialize
        else:
            self.initialized = True
            pass
    
    @property
    def fanfiction(self):
        """
        Retrieves and parses text from a Fanfiction.net story.
        Will attempt to grab a chapter list.
        """
        # Opens and parses the URL with BeautifulSoup
        soup = BeautifulSoup(urlopen(str(self.url)))
        # Retrieve story text from the URL to be used elsewhere
        try:
            # The following code knows a bit too much about the input
            # Find better solution, this will likely break for edge cases
            self.text = soup.find(class_='storytext').text
            # Following code will grab the number of chapters for later use.
            options = str(soup.select('#chap_select')[0].option)
            penultimate_chapter = options.split('option value="')[::-1][1]
            last_chapter = int(penultimate_chapter.split('"')[0]) + 1
            self.chapters = list(map(str, range(-1, last_chapter + 1)))
            self.initialized = True
            """
             # This code tries to get chapter names, but doesn't always work
             # It remains to remind me what not to do.
             # Meanwhile, chapters will be named after their number.
             options = soup.select('#chap_select')[0].option.text
             options_modified = options
             for char in range(len(options)):
                if options[char].isdigit() and options[char + 1] == '.':
                    options_modified = options_modified.replace(
                        options[char], "~$~" + options[char]
                        )
             self.chapters = options_modified.split('~$~')[1:]
            """
        except Exception as E:
            print('Retrieval of Fanfiction story failed: ' + str(E))

    @property
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
        except Exception as E:
            print('Retrieval of Deviantart story failed: ' + str(E))

    @property
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

    @property
    def pdf_initialize(self):
        """
        Sets up the retrieval of text from a PDF,
        whether stored online or locally.
        """
        local_path = os.getcwd() + '\\PDF2BEREAD.pdf'
        if os.path.isfile(local_path):
            os.remove(local_path)
        if self.pathtype == 'url':
            # Download the PDF from the web
            web_path = urlopen(self.url)
            with open('PDF2BEREAD.pdf', 'wb') as file:
                file.write(web_path.read())
            self.url = local_path
        self.initialized = True

    def pdf(self, page):
        """
        Retrieves text from a PDF document, stored locally or online.
        """
        # While this works it's a bit odd. More research required.
        page = PyPDF2.PdfFileReader(self.url).getPage(page)
        self.text = page.extractText().replace('\u2122', "'")

    @property
    def parse(self):
        """
        Removes all unicode characters, nonprintable characters,
        and unneeded special characters.
        Also formats text for audio reading.
        """
        try: # Attempt to scrub the unicode with a library
            text = ftfy.fix_text(self.text)
            self.text = unidecode.unidecode(text).replace('[?]', '')
        except Exception: # If that fails, kill it with fire.
            text = bytes(self.text, 'utf-8')
            text = text.decode('unicode_escape')
            text = text.encode('ascii', 'ignore')
            text = text.decode('utf-8')
            self.text = str(text)
        # Formats text to remove odd artifacts from the conversion
        changes = {
            '\n': ' ',          '\r': ' ',
            '"': "'",           '.': '. ',
            '.   .   . ': '',   '. . .': '...',
            "\'": '',           '\"': '',
            ':': ': ',          ':  ': ': ',
            '!': '! ',          '!  ': '! ',
            '?': '? ',          '?  ': '? ',
            ';': '; ',          ';  ': '; ',
            '0': '0 ',          '1': '1 ',
            '2': '2 ',          '3': '3 ',
            '4': '4 ',          '5': '5 ',
            '6': '6 ',          '7': '7 ',
            '8': '8 ',          '9': '9 '
                  }
        if self.speech == 'local':
            # The Microsoft SAPI pronunciation is a bit off
            updates.update({
                       'Tali': 'Tahlie',     'tali': 'tahlie',
                       'Yalo': ' Yah-lo ',   'caf ': 'cafe ',
                       'Garrus': 'Gae-rrus', 'Klenon': 'Klenn une',
                       'Binary': 'Bi-nary',  'Noveria': ' No-veir-eaah ',
                       'Vakarian': 'Vah-kare-eean'
                      })
        else:
            # Google's TTS is better at its job :)
            updates.update({
                       'Tali': 'Tahhlee', 'tali': 'Tahhlee',
                       'caf ': 'cafe '
                      })
        changes.update(updates)
        for original_word, changed_word in changes.items():
            self.text = self.text.replace(original_word, changed_word)
