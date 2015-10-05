import os
import sys
import webbrowser
from gtts import gTTS
from importlib import import_module
from platform import python_version
from subprocess import call
from textwrap import fill
home = os.path.expanduser("~")

try:
    from OmniReader.__init__ import language
except ImportError:
    from __init__ import language

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

def continue_question(intro_text='reached the end',
                      end_text='start another story'):
    answer = input("You have " + intro_text +
                   ", do you want to " + end_text + "? ")
    if answer == '1' or answer.startswith(('Y', 'y')):
        return True
    else:
        return False


def say(message, title='Speak', speech_system='google', say=True, lang='en'):
    if speech_system == 'google':
        # Create the MP3 file which will speak the text
        folder = ''
        if '\\' in title:
            folder = '\\'.join(title.split('\\')[:-1])
        title += '.mp3'
        tts = gTTS(message, lang=lang)
        path = home+'\\'+title
        folder_path = home + "\\" + folder
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        tts.save(path)
        if say:
            call("start /MIN {}".format(home+'\\'+title), shell=True)
    else:
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


class HumorousError(Exception):
    pass

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
        say("Initializing...", lang=language)
    except Exception:
        global speech_system
        speech_system = 'local'
        try:
            say("Initializing...", speech_system=speech_system, lang=language)
        except Exception:
            speech_system = None
            # I'm leaving this here. It's a fun easter egg, something
            # you don't expect to find when nothing works.
            webbrowser.open_new('https://www.youtube.com/watch?v=WlBiLNN1NhQ')
            raise HumorousError("Life's a piece of shit.")
