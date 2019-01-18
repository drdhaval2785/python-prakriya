#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create a python library which gives derivation for given verb and tense."""
import os.path
import sys
import json
from .utils import app_dir, read_json, convert
# import datetime


class VerbFormGenerator():
    """Return the verb form for given verb, tense, purusha-vachana or suffix.


    Example
    -------

    To get verb form for given verb, tense, suffix / (purusha and vachana) in a project::

        >>> from prakriya import VerbFormGenerator
        >>> g = VerbFormGenerator()

    There are four ways to get verb forms for given verb.

        >>> g.getforms(inputverb, lakara='', purusha='', vachana='')
        >>> g.getforms(inputverb, lakara='', suffix='')
        >>> g[verb, tense, purusha, vachana]
        >>> g[verb, tense, suffix]
        # Examples of four formats are as follows. Default input transliteration is SLP1.
        >>> g.getforms('BU', 'law', 'praTama', 'bahu')
        >>> g.getforms('BU', 'law', 'Ji')
        >>> g['BU', 'law', 'praTama', 'eka']
        >>> g['BU', 'law', 'tip']

        __getitem__ method is discouraged. Will be deprecated in later versions.


    transliteration
    ---------------

    For using transliterations in VerbFormGenerator class, use as below.

      >>> from prakriya import VerbFormGenerator
      >>> g = VerbFormGenerator()
      >>> g.input_translit('hk') # Customize 'hk'
      >>> g.output_translit('devanagari') # Customize 'devanagari'
      >>> g.getforms('bhU', 'laT', 'prathama', 'bahu') # Input in HK and output in Devanagari.

    Valid transliterations are slp1, itrans, hk, iast, devanagari, wx, bengali,
    gujarati, gurmukhi, kannada, malayalam, oriya and telugu.
    They can be used both as input transliteration and output transliteration.
    """

    def __init__(self):
        self.validtenses = ['law', 'liw', 'luw', 'lfw', 'low', 'laN',
                            'viDiliN', 'ASIrliN', 'luN', 'lfN']
        self.validpurushas = ['praTama', 'maDyama', 'uttama']
        self.validvachanas = ['eka', 'dvi', 'bahu']
        self.validsuffices = ['tip', 'tas', 'Ji', 'sip', 'Tas', 'Ta', 'mip',
                              'vas', 'mas', 'ta', 'AtAm', 'Ja', 'TAs', 'ATAm',
                              'Dvam', 'iw', 'vahi', 'mahiN']
        self.validtrans = ['slp1', 'itrans', 'hk', 'iast', 'devanagari',
                           'wx', 'bengali', 'gujarati',
                           'gurmukhi', 'kannada', 'malayalam', 'oriya',
                           'telugu', 'tamil']
        self.appdir = app_dir('prakriya')
        self.intran = 'slp1'
        self.outtran = 'slp1'
        self.mapform = 'mapforms2.json'
        self.mapjson = os.path.join(self.appdir, self.mapform)
        # If the file does not exist, download from Github.
        if not os.path.exists(self.appdir):
            os.makedirs(self.appdir)
        if not os.path.isfile(self.mapjson):
            url1 = 'https://github.com/drdhaval2785/python-prakriya/releases/download/v0.0.2/mapforms2.json'
            import requests
            # print('Downloading mapform file. Roughly 8 MB.')
            with open(self.mapjson, "wb") as fin1:
                ret1 = requests.get(url1)
                fin1.write(ret1.content)
        self.data = read_json(os.path.join(self.appdir, 'mapforms2.json'))
        if not os.path.isfile(os.path.join(self.appdir, 'verbmap.json')):
            url2 = 'https://github.com/drdhaval2785/python-prakriya/releases/download/v0.0.2/verbmap.json'
            import requests
            # print('Downloading verbmap file. Roughly 32 KB.')
            with open(os.path.join(self.appdir, 'verbmap.json'), "wb") as fin2:
                ret2 = requests.get(url2)
                fin2.write(ret2.content)
        self.verbmap = read_json(os.path.join(self.appdir, 'verbmap.json'))

    def input_translit(self, tran):
        """Set input transliteration."""
        # If valid transliteration, set transliteration.
        if tran in self.validtrans:
            self.intran = tran
        # If not valid, throw error.
        else:
            print('Error. Not a valid transliteration scheme.')
            exit(0)

    def output_translit(self, tran):
        """Set output transliteration."""
        # If valid transliteration, set transliteration.
        if tran in self.validtrans:
            self.outtran = tran
        # If not valid, throw error.
        else:
            print('Error. Not a valid transliteration scheme.')
            exit(0)

    def getforms(self, inputverb, lakara='', purusha='', vachana='', suffix=''):
        """Get verb form data for given input."""
        # Change the transliteration to SLP1.
        inputverb = convert(inputverb, self.intran, 'slp1')
        lakara = convert(lakara, self.intran, 'slp1')
        suffix = convert(suffix, self.intran, 'slp1')
        purusha = convert(purusha, self.intran, 'slp1')
        vachana = convert(vachana, self.intran, 'slp1')
        suffices = ['']
        # Get suffices
        if suffix in self.validsuffices:
            suffices = [suffix]
        elif purusha in self.validpurushas and vachana in self.validvachanas:
            suffices = getsuffix(purusha, vachana)
        # Start calculations
        output = []
        if inputverb in self.data:
            verbs = [inputverb]
        elif inputverb in self.verbmap:
            verbs = self.verbmap[inputverb]
        else:
            print('Verb is not in our database. Sorry!')
            exit(0)
        for verb in verbs:
            wholeresult = self.data[verb]
        output = self._remove_unnecessary(wholeresult, lakara, suffices)
        # Transliterate the output
        outputstr = json.dumps(output)
        outputstr = convert(outputstr, 'slp1', self.outtran)
        output = json.loads(outputstr)
        return output

    def _remove_unnecessary(self, wholeresult, lakara='', suffices=['']):
        """Remove redundant data."""
        output = {}
        for member in wholeresult:
            if lakara == '' and suffices == ['']:
                output[member] = wholeresult[member]
            elif lakara != '' and suffices == ['']:
                output[member] = wholeresult[member][lakara]
            elif lakara != '' and suffices != ['']:
                for suffix in suffices:
                    if suffix in wholeresult[member][lakara]:
                        output[member] = wholeresult[member][lakara][suffix]
        return output

    def __getitem__(self, items):
        """Return the requested data by user."""
        # Initiate without arguments
        arguments = ''
        # print(datetime.datetime.now())
        # If there is only one entry in items, it is treated as verb.
        if isinstance(items, ("".__class__, u"".__class__)):
            inputverb = items
        else:
            # Otherwise, first is verbform and the next is argument1.
            inputverb = items[0]
            # py2
            if len(items) > 1 and sys.version_info[0] < 3:
                arguments = [convert(member.decode(
                    'utf-8'), self.intran, 'slp1') for member in items[1:]]
            # py3
            elif len(items) > 1:
                arguments = [convert(member, self.intran, 'slp1')
                             for member in items[1:]]
            # Convert verbform from desired input transliteration to SLP1.
            if sys.version_info[0] < 3:
                inputverb = inputverb.decode('utf-8')
            inputverb = convert(inputverb, self.intran, 'slp1')
            # Enter user defined values
            for member in arguments:
                if member in self.validtenses:
                    tense = member
                if member in self.validpurushas:
                    purusha = member
                if member in self.validvachanas:
                    vachana = member
                if member in self.validsuffices:
                    suffix = member

        # Start calculations
        result = {}
        if inputverb in self.data:
            verbs = [inputverb]
        elif inputverb in self.verbmap:
            verbs = self.verbmap[inputverb]
        else:
            print('Verb is not in our database. Sorry!')
            exit(0)
        for verb in verbs:
            wholeresult = self.data[verb]
            for verb_num in wholeresult:
                # Tense not specified. Return whole data
                if 'tense' not in vars():
                    result[verb_num] = wholeresult
                # Tense specified.
                else:
                    # Tense defined, but suffices not clarified.
                    if 'suffix' not in vars() and ('purusha' not in vars() or 'vachana' not in vars()):
                        result[verb_num] = wholeresult[verb_num][tense]
                    # suffices clarified
                    elif 'suffix' in vars() and suffix in wholeresult[verb_num][tense]:
                        result[verb_num] = wholeresult[verb_num][tense][suffix]
                    elif 'purusha' in vars() and 'vachana' in vars():
                        suffices = getsuffix(purusha, vachana)
                        for suff in suffices:
                            if suff in wholeresult[verb_num][tense]:
                                result[verb_num] = wholeresult[verb_num][tense][suff]
        # Return the result.
        return json.loads(convert(json.dumps(result), 'slp1', self.outtran))


def getsuffix(purusha, vachana):
    """Get suffices for given purusha and vachana."""
    if purusha == 'praTama' and vachana == 'eka':
        result = ['tip', 'ta']
    elif purusha == 'praTama' and vachana == 'dvi':
        result = ['tas', 'AtAm']
    elif purusha == 'praTama' and vachana == 'bahu':
        result = ['Ji', 'Ja']
    elif purusha == 'maDyama' and vachana == 'eka':
        result = ['sip', 'TAs']
    elif purusha == 'maDyama' and vachana == 'dvi':
        result = ['Tas', 'ATAm']
    elif purusha == 'maDyama' and vachana == 'bahu':
        result = ['Ta', 'Dvam']
    elif purusha == 'uttama' and vachana == 'eka':
        result = ['mip', 'iw']
    elif purusha == 'uttama' and vachana == 'dvi':
        result = ['vas', 'vahi']
    elif purusha == 'uttama' and vachana == 'bahu':
        result = ['mas', 'mahiN']
    return result
