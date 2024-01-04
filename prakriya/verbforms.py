#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create a python library which returns details about a verb form."""
import os.path
import sys
import tarfile
import requests
from .utils import app_dir, read_json, convert
# import datetime


class Prakriya():
    """Generate a prakriya class.


    Example
    -------

    To use prakriya in a project::

        >>> from prakriya import Prakriya
        >>> p = Prakriya()

    If you are using the library the first time, be patient.
    This will take a long time, because the data file (30 MB) is being downloaded.

    If you can spare around 600 MB space,
    it is highly recommended to decompress the tar.gz first time.
    Subsequent actions will be very fast. This is one time requirement.
    If the data is not decompressed, the code will read from tar.gz file every time.
    It introduces slowness to a great extent. So highly recommended to decompress.

        >>> p.decompress()

    Now you are ready to roll!

    The generic format for usage is as follows:

        >>> p.get_info(verbform, field)

    ``verbform`` is mandatory. It is the verb form to be investigated.
    The input should be in SLP1 encoding.

    ``field`` is optional.

    Actual usage examples will be like the following.

        >>> p.get_info('Bavati')
        >>> p.get_info('Bavati', 'prakriya')
        >>> p.get_info('Bavati', 'verb')


    Valid values of ``field`` and expected output are as follows.

        ``prakriya`` - Return step by step derivation.

        ``verb`` - Return verb in Devanagari without accent marks.

        ``verbaccent`` - Return the verb in Devanagari with accent marks.

        ``lakara`` - Return the lakAra (tense / mood) in which this form is generated.

        ``gana`` - Return the gaNa (class) of the verb.

        ``meaning`` - Return meaning of the verb in SLP1 transliteration.

        ``number`` - Return number of the verb in dhAtupATha.

        ``madhaviya`` - Return link to mAdhaviyadhAtuvRtti.
        http://sanskrit.uohyd.ac.in/scl/dhaatupaatha is the home page.

        ``kshiratarangini`` - Return link to kSIrataraGgiNI.
        http://sanskrit.uohyd.ac.in/scl/dhaatupaatha is the home page.

        ``dhatupradipa`` - Return link to dhAtupradIpa.
        http://sanskrit.uohyd.ac.in/scl/dhaatupaatha is the home page.

        ``jnu`` - Return link to JNU site for this verb form.
        http://sanskrit.jnu.ac.in/tinanta/tinanta.jsp is the home page.

        ``uohyd`` - Return link to UoHyd site for this verb form.
        http://sanskrit.uohyd.ac.in/cgi-bin/scl/skt_gen/verb/verb_gen.cgi is the home page.

        ``upasarga`` - Return upasarga, if any.
        Currently we do not support verb forms with upasargas.

        ``padadecider_id`` - Return the rule number which decides whether the verb is
        parasmaipadI, AtmanepadI or ubhayapadI.

        ``padadecider_sutra`` - Return the rule text which decides whether the verb is
        parasmaipadI, AtmanepadI or ubhayapadI.

        ``it_id`` - Returns whether the verb is seT, aniT or veT, provided the form has iDAgama.

        ``it_status`` - Returns whether the verb form has iDAgama or not.
        seT, veT, aniT are the output.

        ``it_sutra`` - Returns rule number if iDAgama is caused by some special rule.

        ``purusha`` - Returns the purusha of the given verb form.

        ``vachana`` - Returns the vacana of the given verb form.


    transliteration
    ---------------

    If you want to set the input or output transliteration, follow these steps.

      >>> from prakriya import Prakriya
      >>> p = Prakriya()
      >>> p.input_translit('hk') # Customize 'hk'
      >>> p.output_translit('devanagari') # Customize 'devanagari'
      >>> p.get_info('bhavati') # Input in HK and output in Devanagari.
      >>> p.input_translit('devanagari')
      >>> p.output_translit('iast')
      >>> p.get_info('गच्छति') # Input in Devanagari and output in IAST.

    Valid transliterations are slp1, itrans, hk, iast, devanagari, wx, bengali,
    gujarati, gurmukhi, kannada, malayalam, oriya and telugu.
    They can be used both as input transliteration and output transliteration.
    """

    def __init__(self):
        """Start the class. Decompress tar file if asked for."""
        # Find the directory of the module.
        self.appdir = app_dir('prakriya')
        # Path where to store the file
        self.filename = 'composite_v003.tar.gz'
        self.tarfile = os.path.join(self.appdir, 'composite_v003.tar.gz')
        self.intran = 'slp1'
        self.outtran = 'slp1'
        # If the file does not exist, download from Github.
        if not os.path.exists(self.appdir):
            os.makedirs(self.appdir)
            os.makedirs(os.path.join(self.appdir, 'json'))
        # Download tar.gz data file
        download_from_github(self.appdir, 'composite_v003.tar.gz')
        self.tar = tarfile.open(self.tarfile, 'r:gz')
        # keep only first thee letters from verbform
        download_from_github(self.appdir, 'jsonindex.json')
        self.jsonindex = read_json(os.path.join(self.appdir, 'jsonindex.json'))
        # Read sutrainfo file. This is needed to convert sutra_num to sutra_text.
        download_from_github(self.appdir, 'sutrainfo.json')
        self.sutrainfo = read_json(os.path.join(self.appdir, 'sutrainfo.json'))
        self.json_cache = {}

    def decompress(self):
        """Decompress the tar file if user asks for it."""
        self.tar.extractall(self.appdir)
        print("data files extracted.")
        print("You shall not need to use decompress() function again.")
        print("Just do regular `p = Prakriya()`.")

    def input_translit(self, tran):
        """Set input transliteration."""
        # If valid transliteration, set transliteration.
        if tran in ['slp1', 'itrans', 'hk', 'iast', 'devanagari', 'velthuis',
                    'wx', 'kolkata', 'bengali', 'gujarati', 'gurmukhi',
                    'kannada', 'malayalam', 'oriya', 'telugu', 'tamil']:
            self.intran = tran
        # If not valid, throw error.
        else:
            print('Error. Not a valid transliteration scheme.')
            exit(0)

    def output_translit(self, tran):
        """Set output transliteration."""
        # If valid transliteration, set transliteration.
        if tran in ['slp1', 'itrans', 'hk', 'iast', 'devanagari', 'velthuis',
                    'wx', 'kolkata', 'bengali', 'gujarati', 'gurmukhi',
                    'kannada', 'malayalam', 'oriya', 'telugu', 'tamil']:
            self.outtran = tran
        # If not valid, throw error.
        else:
            print('Error. Not a valid transliteration scheme.')
            exit(0)

    def get_data(self, verbform, tar, intran='slp1', outtran='slp1'):
        """Get whole data from the json file for given verb form."""
        # Find the parent directory
        slugname = self.jsonindex[verbform[:3]]
        # path of json file.
        json_in = os.path.join(self.appdir, 'json', slugname + '.json')
        extract_from_tar(tar, json_in, slugname, self.appdir)
        compositedata = read_json(json_in)
        # Keep only the data related to inquired verbform.
        data = compositedata[verbform]
        # Return results
        return storeresult(data, intran, outtran, self.sutrainfo)

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
        verbform = convert(verbform, self.intran, 'slp1')
        # Read from tar.gz file.
        data = self.get_data(verbform, self.tar, 'slp1', self.outtran)
        # If there is no argument, return whole data.
        if argument == '':
            result = data
        # Else, keep only the data related to the provided argument.
        else:
            result = keep_specific(data, argument)
        # print(datetime.datetime.now())
        # Return the result.
        return result

    def get_info(self, verbform, field='prakriya'):
        """Return the data requested by user."""
        items = [verbform, field]
        return self.__getitem__(items)


def convertible(argument):
    """Returns whether the item is convertible to Devanagari or not."""
    result = False
    if argument in set(['verb', 'lakara', 'gana', 'meaning', 'upasarga',
                        'padadecider_id', 'padadecider_sutra', 'suffix',
                        'it_status', 'it_sutra', 'it_id', 'vachana',
                        'purusha']):
        result = True
    return result


def extract_from_tar(tar, filename, slugname, appdir):
    """Extracts a file from given tar object and places in the outdir."""
    if not os.path.isfile(filename):
        member = tar.getmember('json/' + slugname + '.json')
        tar.extract(member, appdir)


def storeresult(data, intran, outtran, sutrainfo):
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
                    subresult[item] = convert(tmp, intran, outtran)
                else:
                    subresult[item] = tmp
            # derivation is a list (as compared to others which are strings.)
            elif item == 'derivation':
                # For member of the list
                for member in datum['derivation']:
                    # Fetch sutratext
                    if member['sutra_num'] not in sutrainfo:
                        sutratext = ''
                    else:
                        sutratext = sutrainfo[member['sutra_num']]
                    sutratext = convert(sutratext, intran, outtran)
                    # Replace tilde with hyphen.
                    # Otherwise wrong transliteration will happen.
                    sutranum = member['sutra_num'].replace('~', '-')
                    # sutranum = convert(sutranum, intran, outtran)
                    # A decent representation for rutva.
                    form = member['form'].replace('@', 'u~')
                    form = convert(form, intran, outtran)
                    # Add to derivationlist.
                    derivationlist.append({'sutra': sutratext,
                                           'sutra_num': sutranum, 'form': form})
        # Add the derivationlist to the prakriya key.
        subresult['prakriya'] = derivationlist
        # Append subresult to result and start again.
        result.append(subresult)
    # Give result.
    return result


def keep_specific(data, argument):
    """Create a list of only the relavent argument."""
    return [member[argument] for member in data]


def download_from_github(appdir, filename):
    """Download specific data file from Github release page."""
    if not os.path.isfile(os.path.join(appdir, filename)):
        print('downloading ' + filename)
        url = 'https://github.com/drdhaval2785/python-prakriya/releases/download/v0.0.2/' + filename
        with open(os.path.join(appdir, filename), "wb") as fin:
            ret = requests.get(url)
            fin.write(ret.content)
        print('downloaded ' + filename)
