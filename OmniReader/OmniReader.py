try:
    from OmniReader.getStory import getStory
    from OmniReader.utility_functions import say, continue_question
except ImportError:
    from getStory import getStory
    from utility_functions import say, continue_question

import os
import sys

try:
    from __init__ import speech_system
except ImportError:
    speech_system = 'google'


def OmniReader(text, *, change_type=False):
    """
    "Drive me closer, I want to hit them with my superfunction."
    This function will gather text from the inputted source,
    parse it, and output an audio version of that text using
    either Google's text-to-speech engine or a local TTS
    solution.
    The audio versions will be stored in the
    ~/Users/USERNAME/
    path as either .MP3s or as .VBS files.
    ------------------------------------------------------------
    change_type
        A variable which allows the user to set the story
        type manually from the command line.
    """
    story = getStory(text)
    if change_type:
        story.type = change_type
    
    if story.type == 'wattpad':
        if sys.argv[0] and len(sys.argv) == 2:
            error_text = "Page count required for this story."
            raise SyntaxError(error_text)
        elif sys.argv[0] and len(sys.argv) == 3:
            if sys.argv[2]:
                page_count = int(sys.argv[2])+1
        else:
            page_count = input("How many pages are in the story: ")
            page_count = int(page_count) + 1
        # Iterates through the pages of the story
        for page in range(page_count):
            if page:
                # Designed to cope with Wattpad's weird multi-page system
                story.wattpad(page, 'plural')[1]
            else:
                # Meant for the first page because **** Wattpad
                story.wattpad()
            paragraphs = story.text.find_all('p')
            # Iterates through the paragraphs in each page of the story
            text = [paragraph.text for paragraph in paragraphs]
            story.text = ' '.join(text)
            story.parse
            print(story.text)
            say(story.text, speech_system=speech_system, lang=story.language)
            return continue_question()

    elif story.type == 'fanfiction':
        """
        Iterate through each chapter in a fanfiction
        and save the audio recording of each.
        """
        story.fanfiction
        url = story.url.split('/')
        # Starts at the first chapter
        for each_chapter in range(int(url[-2]), int(story.chapters[-1]) + 1):
            url = story.url.split('/')
            story.fanfiction
            # Set up the name for each audio recording
            title = url[-1] + " Chapter " + url[-2]
            # if not os.path.exists(url[-1]):
            #     os.makedirs(url[-1])
            # print("Processing story text...")
            story.parse
            print("Downloading: " + title)
            current_chapter = int(story.chapters[each_chapter]) + 1
            say(story.text, 
                url[-1] + '\\' + str(current_chapter),
                speech_system, False)
            # Iterate to the next chapter and reset the URL
            url[-2] = str(int(url[-2]) + 1)
            # print("Continuing to next chapter...")
            story.url = '/'.join(url)
        return continue_question('finished recording')

    elif story.type == 'pdf':
        story.pdf_initialize
        request = "Enter the beginning page"
        if sys.argv[0] and len(sys.argv) == 2:
            raise SyntaxError(request + '.')
        elif sys.argv[0] and len(sys.argv) == 3:
            if sys.argv[2]:
                first_page = int(sys.argv[2])-1
        else:
            first_page = int(input(request + ": ")) - 1
        last_page = PyPDF2.PdfFileReader(story.url).getNumPages()
        for page in range(first_page, last_page):
            # There's some weird shit going on here.
            story.pdf(page)
            print('\n \t \t' + str(page + 1) + '\n')
            story.parse
            print(story.text)
            say(story.text, speech_system=speech_system, lang=story.language)
        return continue_question()

    elif story.type == 'deviantart':
        story.deviantart
        url = story.url.split('/')
        title = url[-1]
        # print("Processing story text...")
        story.parse
        print("Downloading: " + title)
        say(story.text, title, speech_system, lang=story.language)
        return continue_question('finished recording')

    elif story.type == 'text':
        story.initialize
        print('\n' + story.text)
        story.parse
        try:
            say(story.text, speech_system=speech_system, lang=story.language)
        except Exception: # The language could not be determined.
            say(story.text, speech_system=speech_system)
        return continue_question('finished speaking', 'say something else')
