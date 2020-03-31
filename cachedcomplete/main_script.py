'''
Gets values from special comments in the first 1024 bytes of the main script.
'''
import os
import re
import sys
import shlex

from argcomplete import USING_PYTHON2
from itertools import chain

if USING_PYTHON2:
    from pipes import quote
else:
    quote = shlex.quote


SEARCH_RANGE = 1024
INFO_PREFIX = 'CACHEDCOMPLETE_'
FILES_TO_HASH_INFO = INFO_PREFIX + r'HASH:\s*(?P<files>.*)$'

# Path to the main script
if sys.argv[0] != '-c':
    MAIN_FILE_PATH = os.path.abspath(sys.argv[0])
else:
    # Running as `python -c "commands"`
    MAIN_FILE_PATH = None


def _get_info_list(expr):
    '''
    :return: an iterable of all items from the main script (not an actual list).
    '''
    with open(MAIN_FILE_PATH) as main_file:
        content = main_file.read(SEARCH_RANGE)
    return chain(*(shlex.split(match.group('files')) for match in re.finditer(expr, content, re.M)))


def _expand(filename):
    return quote(os.path.expanduser(os.path.expandvars(filename)))


def get_files_to_hash():
    '''
    :return: an iterable of all the files and directories that should be hashed.
    '''
    os.environ.setdefault('pwd', os.path.abspath(os.curdir))
    return chain([MAIN_FILE_PATH, os.path.dirname(__file__)], (_expand(filename) for filename in _get_info_list(FILES_TO_HASH_INFO)))


def exists():
    '''
    :return: ``True`` if the main script exists, otherwise ``False`` (as when ran with `python -c`).
    '''
    return MAIN_FILE_PATH is not None and os.path.exists(MAIN_FILE_PATH)
