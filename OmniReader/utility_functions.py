import os
import sys
import webbrowser
from gtts import gTTS
from importlib import import_module
from platform import python_version
from subprocess import call
from textwrap import fill
home = os.path.expanduser("~")

speech_system = 'google'
language = 'en'


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

