"""
Special thanks to all the people at CodeReview
who helped me optimize and improve my code!
"""

import os
import sys
sys.path.append(os.getcwd())
import time
import webbrowser
from utility_functions import say
from utility_functions import import_or_install
from platform import python_version


import_or_install('gtts', 'gTTS', 'Google Text to Speech API',
                  'sound natural')

import_or_install('bs4', 'beautifulsoup4', 'Beautiful Soup',
                  'be able to pull text from websites')

import_or_install('PyPDF2', 'PyPDF2', 'PyPDF2',
                  'be able to process PDF files')

import_or_install('ftfy', 'ftfy', 'the smart Python unicode fixer',
                  'sometimes say odd things or crash.')

import_or_install('unidecode', 'unidecode', 'the last resort unicode parser',
                  'will likely crash if it finds a special character.')

global speech_system
speech_system = 'google'
from OmniReader import OmniReader


if '2' == python_version()[0]:
    print("This program requires Python 3 in order to properly function.\n"
          "A backwards compatible version may be available in the future.")
    input("End of line.")
    sys.exit()

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
