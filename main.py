"""
Special thanks to all the people at CodeReview
who helped me optimize and improve my code!
"""

import os
import sys
import time
import webbrowser
from subprocess import call
from utility_functions import *
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
