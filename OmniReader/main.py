import sys
try:
    from OmniReader.utility_functions import checkup
except ImportError:
    from utility_functions import checkup

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
