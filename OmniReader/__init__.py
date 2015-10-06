import os
__author__ = "Isaac Smith (Zenohm)"
__email__ = 'sentherus@gmail.com'
__copyright__ = '2015 sentherus@gmail.com'
__license__ = "MIT"
__date__ = '2015-10-04'
version_file = os.path.join(os.path.dirname(__file__), 'VERSION.py')
with open(version_file) as fh:
    __version_info__ = eval(fh.read().strip())
__version__ = '.'.join(str(i) for i in __version_info__)
__home__ = 'https://github.com/Zenohm/OmniReader'
__download__ = 'https://github.com/Zenohm/OmniReader/archive/master.zip'

try:
    from OmniReader.getStory import *
    from OmniReader.OmniReader import *
    from OmniReader.utility_functions import *
except ImportError:
    from getStory import *
    from OmniReader import *
    from utility_functions import *

speech_system = 'google'
language = 'en'
