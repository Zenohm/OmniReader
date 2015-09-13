import os
import sys
from gtts import gTTS
from importlib import import_module
from subprocess import call
home = os.path.expanduser("~")


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
