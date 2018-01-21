#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create a python library which returns details about a verb form.

Example
-------

To use prakriya in a project::

    >>> from prakriya import Prakriya
    >>> p = Prakriya()

If you are using the library the first time, be patient.
This will take a long time, because the data file (30 MB) is being downloaded.

If you can spare around 600 MB space, It is highly recommended to decompress the tar.gz first time.
Subsequent actions will be very fast. This is one time requirement.
If the data is not decompressed, the code will read from tar.gz file every time.
It introduces slowness to a great extent. So highly recommended to decompress.

    >>> p.decompress()

Now you are ready to roll!

The generic format for usage is as follows:

    >>> p[verbform, field]

``verbform`` is mandatory. It is the verb form to be investigated.
The input should be in SLP1 encoding.

``field`` is optional.

Actual usage examples will be like the following.

    >>> p['Bavati']
    >>> p['Bavati', 'prakriya']
    >>> p['Bavati', 'verb']


Valid values of ``field`` and expected output are as follows.

    ``prakriya`` - Return step by step derivation.

    ``verb`` - Return verb in Devanagari without accent marks.

    ``verbaccent`` - Return the verb in Devanagari with accent marks.

    ``lakara`` - Return the lakAra (tense / mood) in which this form is generated.

    ``gana`` - Return the gaNa (class) of the verb.

    ``meaning`` - Return meaning of the verb in SLP1 transliteration.

    ``number`` - Return number of the verb in dhAtupATha.

    ``madhaviya`` - Return link to mAdhaviyadhAtuvRtti. http://sanskrit.uohyd.ac.in/scl/dhaatupaatha is the home page.

    ``kshiratarangini`` - Return link to kSIrataraGgiNI. http://sanskrit.uohyd.ac.in/scl/dhaatupaatha is the home page.

    ``dhatupradipa`` - Return link to dhAtupradIpa. http://sanskrit.uohyd.ac.in/scl/dhaatupaatha is the home page.

    ``jnu`` - Return link to JNU site for this verb form. http://sanskrit.jnu.ac.in/tinanta/tinanta.jsp is the home page.

    ``uohyd`` - Return link to UoHyd site for this verb form. http://sanskrit.uohyd.ac.in/cgi-bin/scl/skt_gen/verb/verb_gen.cgi is the home page.

    ``upasarga`` - Return upasarga, if any. Currently we do not support verb forms with upasargas.

    ``padadecider_id`` - Return the rule number which decides whether the verb is parasmaipadI, AtmanepadI or ubhayapadI.

    ``padadecider_sutra`` - Return the rule text which decides whether the verb is parasmaipadI, AtmanepadI or ubhayapadI.

    ``it_id`` - Returns whether the verb is seT, aniT or veT, provided the form has iDAgama.

    ``it_status`` - Returns whether the verb form has iDAgama or not. seT, veT, aniT are the output.

    ``it_sutra`` - Returns rule number if iDAgama is caused by some special rule.

    ``purusha`` - Returns the purusha of the given verb form.

    ``vachana`` - Returns the vacana of the given verb form.

transliteration
---------------
If you want to set the input or output transliteration, follow these steps.

  >>> from prakriya import Prakriya
  >>> p = Prakriya()
  >>> p.inputTranslit('hk') # Customize 'hk'
  >>> p.outputTranslit('devanagari') # Customize 'devanagari'
  >>> p['bhavati'] # Input in HK and output in Devanagari.
  >>> p.inputTranslit('devanagari')
  >>> p.outputTranslit('iast')
  >>> p['गच्छति'] # Input in Devanagari and output in IAST.

Valid transliterations are slp1, itrans, hk, iast, devanagari, wx, bengali,
gujarati, gurmukhi, kannada, malayalam, oriya and telugu.
They can be used both as input transliteration and output transliteration.
"""
import os.path
import sys
import tarfile
import requests
from .utils import appDir, readJson, convert
# import datetime


class Prakriya():
    r"""Generate a prakriya class.

    Parameters
    ----------
    It takes a list as parameters e.g. ['verbform', 'field']
    verbform is a string in SLP1.
    field is optional.
    When it is not provided, the whole data gets loaded back.
    The results are always in list format.

    Valid values of field and expected output are as follows.
    "prakriya" - Return step by step derivation.
    "verb" - Return verb in Devanagari without accent marks.
    "verbaccent" - Return the verb in Devanagari with accent marks.
    "lakara" - Return the lakAra (tense / mood) in which this form is generated.
    "gana" - Return the gaNa (class) of the verb.
    "meaning" - Return meaning of the verb in SLP1 transliteration.
    "number" - Return number of the verb in dhAtupATha.
    "madhaviya" - Return link to mAdhaviyadhAtuvRtti. http://sanskrit.uohyd.ac.in/scl/dhaatupaatha is the home page.
    "kshiratarangini" - Return link to kSIrataraGgiNI. http://sanskrit.uohyd.ac.in/scl/dhaatupaatha is the home page.
    "dhatupradipa" - Return link to dhAtupradIpa. http://sanskrit.uohyd.ac.in/scl/dhaatupaatha is the home page.
    "jnu" - Return link to JNU site for this verb form. http://sanskrit.jnu.ac.in/tinanta/tinanta.jsp is the home page.
    "uohyd" - Return link to UoHyd site for this verb form. http://sanskrit.uohyd.ac.in/cgi-bin/scl/skt_gen/verb/verb_gen.cgi is the home page.
    "upasarga" - Return upasarga, if any. Currently we do not support verb forms with upasargas.
    "padadecider_id" - Return the rule number which decides whether the verb is parasmaipadI, AtmanepadI or ubhayapadI.
    "padadecider_sutra" - Return the rule text which decides whether the verb is parasmaipadI, AtmanepadI or ubhayapadI.
    "it_id" - Returns whether the verb is seT, aniT or veT, provided the form has iDAgama.
    "it_status" - Returns whether the verb form has iDAgama or not. seT, veT, aniT are the output.
    "it_sutra" - Returns rule number if iDAgama is caused by some special rule.
    "purusha" - Returns the purusha of the given verb form.
    "vachana" - Returns the vacana of the given verb form.

    Example
    -------
    >>> from verbforms import Prakriya
    >>> p = Prakriya()
    # If you are using the library the first time, be patient.
    # This will take a long time.
    # Data file (30 MB) is being downloaded.
    # If you can spare around 600 MB space, decompress the tar.gz first time.
    # Subsequent actions will be very fast. This is one time requirement.
    >>> p.decompress()
    >>> p['Bavati']
    # Will return [{u'gana': u'BvAdi', u'verb': u'BU', ...}]
    >>> p['Bavati', 'verb']
    [u'BU']
    >>> p['Bavati', 'prakriya']
    [[{'sutra': u'BUvAdayo DAtavaH', 'sutra_num': u'1.3.1', 'form': u'BU'}..}]]

    """

    def __init__(self):
        """Start the class. Decompress tar file if asked for."""
        # Find the directory of the module.
        self.appdir = appDir('prakriya')
        # Path where to store the file
        self.filename = 'composite_v003.tar.gz'
        self.tr = os.path.join(self.appdir, self.filename)
        self.inTran = 'slp1'
        self.outTran = 'slp1'
        # If the file does not exist, download from Github.
        if not os.path.exists(self.appdir):
            os.makedirs(self.appdir)
            os.makedirs(os.path.join(self.appdir, 'json'))
        # Download tar.gz data file
        downloadFromGithub(self.appdir, 'composite_v003.tar.gz')
        self.tar = tarfile.open(self.tr, 'r:gz')
        # keep only first thee letters from verbform
        downloadFromGithub(self.appdir, 'jsonindex.json')
        self.jsonindex = readJson(os.path.join(self.appdir, 'jsonindex.json'))
        # Read sutrainfo file. This is needed to convert sutra_num to sutra_text.
        downloadFromGithub(self.appdir, 'sutrainfo.json')
        self.sutrainfo = readJson(os.path.join(self.appdir, 'sutrainfo.json'))
        self.jsonCache = {}

    def decompress(self):
        """Decompress the tar file if user asks for it.

        It makes the future operations very fast.
        """
        self.tar.extractall(self.appdir)
        print("data files extracted.")
        print("You shall not need to use decompress() function again.")
        print("Just do regular `p = Prakriya()`.")

    def inputTranslit(self, tran):
        """Set input transliteration."""
        # If valid transliteration, set transliteration.
        if tran in ['slp1', 'itrans', 'hk', 'iast', 'devanagari', 'velthuis',
                    'wx', 'kolkata', 'bengali', 'gujarati', 'gurmukhi',
                    'kannada', 'malayalam', 'oriya', 'telugu', 'tamil']:
            self.inTran = tran
        # If not valid, throw error.
        else:
            print('Error. Not a valid transliteration scheme.')
            exit(0)

    def outputTranslit(self, tran):
        """Set output transliteration."""
        # If valid transliteration, set transliteration.
        if tran in ['slp1', 'itrans', 'hk', 'iast', 'devanagari', 'velthuis',
                    'wx', 'kolkata', 'bengali', 'gujarati', 'gurmukhi',
                    'kannada', 'malayalam', 'oriya', 'telugu', 'tamil']:
            self.outTran = tran
        # If not valid, throw error.
        else:
            print('Error. Not a valid transliteration scheme.')
            exit(0)

    def get_data(self, verbform, tar, inTran='slp1', outTran='slp1'):
        """Get whole data from the json file for given verb form."""
        # Find the parent directory
        slugname = self.jsonindex[verbform[:3]]
        # path of json file.
        json_in = os.path.join(self.appdir, 'json', slugname + '.json')
        extract_from_tar(tar, json_in, slugname, self.appdir)
        compositedata = readJson(json_in)
        # Keep only the data related to inquired verbform.
        data = compositedata[verbform]
        # Return results
        return storeresult(data, inTran, outTran, self.sutrainfo)

    def __getitem__(self, items):
        """Return the requested data by user."""
        # Initiate without arguments
        argument = ''
        # print(datetime.datetime.now())
        # If there is only one entry in items, it is treated as verbform.
        if isinstance(items, ("".__class__, u"".__class__)):
            verbform = items
        # Otherwise, first is verbform and the next is argument1.
        else:
            verbform = items[0]
            if len(items) > 1:
                argument = items[1]
        # Convert verbform from desired input transliteration to SLP1.
        if sys.version_info[0] < 3:
            verbform = verbform.decode('utf-8')
        verbform = convert(verbform, self.inTran, 'slp1')
        # Read from tar.gz file.
        data = self.get_data(verbform, self.tar, 'slp1', self.outTran)
        # If there is no argument, return whole data.
        if argument == '':
            result = data
        # Else, keep only the data related to the provided argument.
        else:
            result = keepSpecific(data, argument)
        # print(datetime.datetime.now())
        # Return the result.
        return result


def convertible(argument):
    if argument in set(['verb', 'lakara', 'gana', 'meaning', 'upasarga',
                        'padadecider_id', 'padadecider_sutra', 'suffix',
                        'it_status', 'it_sutra', 'it_id', 'vachana',
                        'purusha']):
        return True
    else:
        return False


def extract_from_tar(tar, filename, slugname, appdir):
    """Extracts a file from given tar object and places in the outdir."""
    if not os.path.isfile(filename):
        member = tar.getmember('json/' + slugname + '.json')
        tar.extract(member, appdir)


def storeresult(data, inTran, outTran, sutrainfo):
    """Store the result with necessary transliteration conversions."""
    # Initialize empty result stack.
    result = []
    # For each possible derivation leading to the given verb form
    # e.g. baBUva can be from BU, asa~
    for datum in data:
        # Initialize a subresult stack as dict.
        # key will be argument and value will be data.
        subresult = {}
        # Start a list for derivation. It needs special treatment.
        derivationlist = []
        # For each key,
        for item in datum:
            # if not in these two
            if item not in ['derivation']:
                tmp = datum[item]
                # correct the wrong anusvAra in SLP1 to correct one.
                tmp = tmp.replace('!', '~')
                # Store in subresult dict.
                if convertible(item):
                    subresult[item] = convert(tmp, inTran, outTran)
                else:
                    subresult[item] = tmp
            # derivation is a list (as compared to others which are strings.)
            elif item == 'derivation':
                # For member of the list
                for member in datum['derivation']:
                    # Fetch sutratext
                    sutratext = sutrainfo[member['sutra_num']]
                    sutratext = convert(sutratext, inTran, outTran)
                    # Replace tilde with hyphen.
                    # Otherwise wrong transliteration will happen.
                    sutranum = member['sutra_num'].replace('~', '-')
                    # sutranum = convert(sutranum, inTran, outTran)
                    # A decent representation for rutva.
                    form = member['form'].replace('@', 'u~')
                    form = convert(form, inTran, outTran)
                    # Add to derivationlist.
                    derivationlist.append({'sutra': sutratext,
                                          'sutra_num': sutranum, 'form': form})
        # Add the derivationlist to the prakriya key.
        subresult['prakriya'] = derivationlist
        # Append subresult to result and start again.
        result.append(subresult)
    # Give result.
    return result


def keepSpecific(data, argument):
    """Create a list of only the relavent argument."""
    return [member[argument] for member in data]


def downloadFromGithub(appdir, filename):
    if not os.path.isfile(os.path.join(appdir, filename)):
        print('downloading ' + filename)
        url = 'https://github.com/drdhaval2785/python-prakriya/releases/download/v0.0.2/' + filename
        with open(os.path.join(appdir, filename), "wb") as f:
            r = requests.get(url)
            f.write(r.content)
        print('downloaded ' + filename)
