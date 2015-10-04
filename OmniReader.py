from getStory import getStory
from utility_functions import say, continue_question
import os

try:
    from __main__ import speech_system
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
            raise SyntaxError(
                "Please input the number of pages in this story.")
        elif sys.argv[0] and len(sys.argv) == 3:
            if sys.argv[2]:
                number_of_pages = int(sys.argv[2])+1
        else:
            number_of_pages = int(
                input("How many pages are in the story: ")) + 1
        # Iterates through the pages of the story
        for each_page in range(number_of_pages):
            if each_page:
                # Designed to cope with Wattpad's weird multi-page system
                story.wattpad(each_page, 'plural')[1]
            else:
                # Meant for the first page because **** Wattpad
                story.wattpad()
            paragraphs = story.text.find_all('p')
            # Iterates through the paragraphs in each page of the story
            for each_paragraph in range(len(paragraphs)):
                # Get all the text segments
                paragraphs[each_paragraph] = paragraphs[each_paragraph].text
            story.text = ' '.join(paragraphs)
            story.parse()
            print(story.text)
            say(story.text, speech_system=speech_system)
            return continue_question()

    elif story.type == 'fanfiction':
        """
        Iterate through each chapter in a fanfiction
        and save the audio recording of each.
        """
        story.text = "No data available."
        story.fanfiction()
        url = story.url.split('/')
        for each_chapter in range(int(url[-2]), int(story.chapters[-1]) + 1):
            url = story.url.split('/')
            story.fanfiction()
            # Set up the name for each audio recording
            title = url[-1] + '_' + url[-2]
            if not os.path.exists(url[-1]):
                os.makedirs(url[-1])
            print("Processing story text...")
            story.parse()
            print("Downloading audio file, " + title)
            if speech_system == 'local':
                say(story.text,
                    url[-1] +
                    '\\' +
                    str(int(story.chapters[each_chapter]) + 1),
                    speech_system,
                    False)
            else:
                say(story.text,
                    url[-1] +
                    '\\' +
                    str(int(story.chapters[each_chapter]) + 1),
                    speech_system,
                    False)
            # Iterate to the next chapter and reset the URL
            url[-2] = str(int(url[-2]) + 1)
            print("Continuing to next chapter...")
            story.url = '/'.join(url)
        return continue_question('finished recording')

    elif story.type == 'pdf':
        story.pdf_initialize()
        if sys.argv[0] and len(sys.argv) == 2:
            raise SyntaxError("Please input the beginning page.")
        elif sys.argv[0] and len(sys.argv) == 3:
            if sys.argv[2]:
                first_page = int(sys.argv[2])-1
        else:
            first_page = int(input("Please enter the beginning page: ")) - 1
        for each_page in range(
            first_page,
            PyPDF2.PdfFileReader(story.url).getNumPages()
                              ):
            story.pdf(each_page)
            print('\n \t \t' + str(each_page + 1) + '\n')
            story.parse()
            print(story.text)
            say(story.text, speech_system=speech_system)
        return continue_question()

    elif story.type == 'deviantart':
        story.deviantart()
        url = story.url.split('/')
        title = url[-1]
        print("Processing story text...")
        story.parse()
        print("Creating audio file.")
        say(story.text, title, speech_system)
        return continue_question('finished recording')

    elif story.type == 'text':
        print('\n' + story.text)
        story.parse()
        say(story.text, speech_system=speech_system)
        return continue_question('finished speaking', 'say something else')
