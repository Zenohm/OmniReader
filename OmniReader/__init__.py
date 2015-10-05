__author__ = "Isaac Smith (Zenohm)"
__email__ = 'sentherus@gmail.com'
__copyright__ = '2015 sentherus@gmail.com'
__license__ = "MIT"
__date__ = '2015-10-04'
__version_info__ = (2, 1, 0)
__version__ = '.'.join(str(i) for i in __version_info__)
__home__ = 'https://github.com/Zenohm/OmniReader'
__download__ = 'https://github.com/Zenohm/OmniReader/archive/master.zip'



import sys
import webbrowser
from utility_functions import say, import_or_install
from platform import python_version


speech_system = 'google'
language = 'en'


def checkup():
    global speech_system
    google_tts = '?'
    beautiful_soup = '?'
    python_PDF2 = '?'
    ft_fy = '?'
    uni_decode = '?'
    correct_version = '?'
    
    if int(python_version()[0]) < 3:
        print("This program requires Python 3 in order to properly function.\n"
              "A backwards compatible version may be available in the future.")
        correct_version = False
    else:
        correct_version = True
    
    if not correct_version:
        input("End of line.")
        sys.exit()
    
    try:
        import_or_install('gtts', 'gTTS', 'Google Text to Speech API',
                      'sound natural')
        google_tts = True
    except Exception:
        google_tts = False
    
    try:
        import_or_install('bs4', 'beautifulsoup4', 'Beautiful Soup',
                      'be able to pull text from websites')
        beautiful_soup = True
    except Exception:
        beautiful_soup = False
    
    try:
        import_or_install('PyPDF2', 'PyPDF2', 'PyPDF2',
                      'be able to process PDF files')
        python_PDF2 = True
    except Exception:
        python_PDF2 = False
    
    try:
        import_or_install('ftfy', 'ftfy', 'the smart Python unicode fixer',
                      'sometimes say odd things or crash.')
        ft_fy = True
    except Exception:
        ft_fy = False
    
    try:
        import_or_install('unidecode', 'unidecode', 'the last resort unicode parser',
                      'will likely crash if it finds a special character.')
        uni_decode = True
    except Exception:
        uni_decode = False
    
    try:
        say("Initializing...")
    except Exception:
        global speech_system
        speech_system = 'local'
        try:
            say("Initializing...", speech_system=speech_system)
        except Exception:
            speech_system = None
            # I'm leaving this here. It's a fun easter egg, something
            # you don't expect to find when nothing works.
            webbrowser.open_new('https://www.youtube.com/watch?v=WlBiLNN1NhQ')
            raise HumorousError("Life's a piece of shit.")
