#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Helper functions for prakriya package."""

import json
import sys
from functools import wraps
from indic_transliteration import sanscript


# https://stackoverflow.com/questions/15585493/store-the-cache-to-a-file-functools-lru-cache-in-python-3-2
def cached(func):
    """Create a decorator for cacheing."""
    func.cache = {}

    @wraps(func)
    def wrapper(*args):
        try:
            return func.cache[args]
        except KeyError:
            func.cache[args] = result = func(*args)
            return result
    return wrapper


# https://stackoverflow.com/questions/1084697/how-do-i-store-desktop-application-data-in-a-cross-platform-way-for-python
def app_dir(appname):
    """Return the repository where the system stores APPDATA."""
    from os import path, environ
    if sys.platform == 'darwin':
        from AppKit import NSSearchPathForDirectoriesInDomains as searchin
        from AppKit import NSApplicationSupportDirectory as dirin
        from AppKit import NSUserDomainMask as maskin
        appdata = path.join(searchin(dirin, maskin, True)[0], appname)
    elif sys.platform == 'win32':
        appdata = path.join(environ['APPDATA'], appname)
    else:
        appdata = path.expanduser(path.join("~", "." + appname))
    return appdata


@cached
def read_json(path):
    """Read the given JSON file into python object."""
    with open(path, 'r') as fin:
        return json.loads(fin.read())


@cached
def convert(text, intran, outtran):
    """Convert a text from intran to outtran transliteration."""
    result = ''
    if intran == outtran:
        result = text
    elif sys.version_info[0] < 3:
        result = sanscript.transliterate(text, intran, outtran).replace(u'|', u'.')
    else:
        result = sanscript.transliterate(text, intran, outtran).replace('|', '.')
    return result
