import sys
import webbrowser

try:
    from OmniReader.utility_functions import say
    from OmniReader.__init__ import language
except ImportError:
    from utility_functions import say
    from __init__ import language



class HumorousError(Exception):
    pass

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

try:
    from OmniReader.OmniReader import OmniReader
except ImportError:
    from OmniReader import OmniReader

def main():
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
