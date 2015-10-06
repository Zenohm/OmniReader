import sys

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


checkup()

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
