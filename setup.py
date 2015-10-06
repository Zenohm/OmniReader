import os

version_file = os.path.join(os.path.dirname(__file__), 'OmniReader', 'VERSION.py')
with open(version_file) as fh:
    __version_info__ = eval(fh.read().strip())
omnireader_version = '.'.join(str(i) for i in __version_info__)



from distutils.core import setup

setup(
    name = "OmniReader",
    description = "OmniReader Story Teller",
    version = omnireader_version,
    url = "https://github.com/Zenohm/OmniReader",
    long_description = """\
The OmniReader Story Teller is a python package that reads stories
using a TTS engine.  OmniReader requires Python 3.3+.""",
    license = "MIT",
    keywords = ['OmniReader', 'Fanfiction', 'stories',
                'scraping', 'translating', 'Wattpad',
                'text-to-speech', 'deviantart'],
    maintainer = "Isaac Smith (Zenohm)",
    maintainer_email = "sentherus@gmail.com",
    author = "Isaac Smith (Zenohm)",
    author_email = "sentherus@gmail.com",
    classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Other Audience',
    'Intended Audience :: Education',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Topic :: Multimedia :: Sound/Audio',
    'Topic :: Multimedia :: Sound/Audio :: Speech',
    ],
    packages = ['OmniReader'],
    )
