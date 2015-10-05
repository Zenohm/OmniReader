"""
Special thanks to all the people at CodeReview
who helped me optimize and improve my code!
"""

import sys
from OmniReader.utility_functions import checkup

checkup()

from OmniReader.OmniReader import OmniReader

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
