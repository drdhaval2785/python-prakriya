import ujson
from indic_transliteration import sanscript
from functools import wraps


# https://stackoverflow.com/questions/15585493/store-the-cache-to-a-file-functools-lru-cache-in-python-3-2
def cached(func):
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
def appDir(appname):
    import sys
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
def readJson(path):
    """Read the given JSON file into python object."""
    with open(path, 'r') as fin:
        return ujson.loads(fin.read())


@cached
def convert(text, inTran, outTran):
    """Convert a text from inTran to outTran transliteration."""
    if inTran == outTran:
        return text
    else:
        return sanscript.transliterate(text, inTran, outTran)
