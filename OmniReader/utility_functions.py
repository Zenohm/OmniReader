import os
from gtts import gTTS
from subprocess import call
home = os.path.expanduser("~")

speech_system = 'google'
language = 'en'


def continue_question(intro_text='reached the end',
                      end_text='start another story'):
    answer = input("You have " + intro_text +
                   ", do you want to " + end_text + "? ")
    return answer == '1' or answer.startswith(('Y', 'y'))


def say(message, title='Speak', speech_system='google', say=True, lang='en'):
    if speech_system == 'google':
        # Create the MP3 file which will speak the text
        folder = ''
        folder, file_name = os.path.split(title)
        title += '.mp3'
        tts = gTTS(message, lang=lang)
        path = os.path.join(home, title)
        folder_path = os.path.join(home, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        tts.save(path)
        if say:
            call("start /MIN {}".format(os.path.join(home, title)), shell=True)
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
                    .format(str(message).replace('"', '').replace('\n', '')))
        # Execute the file
        call(['cscript.exe', title + '.vbs'])


class HumorousError(Exception):
    pass

