#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create a python library which gives derivation for given verb and tense."""
import os.path
import sys
import json
from .utils import appDir, readJson, convert
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
      >>> g.inputTranslit('hk') # Customize 'hk'
      >>> g.outputTranslit('devanagari') # Customize 'devanagari'
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
        self.appdir = appDir('prakriya')
        self.inTran = 'slp1'
        self.outTran = 'slp1'
        self.mapform = 'mapforms2.json'
        self.mp = os.path.join(self.appdir, self.mapform)
        # If the file does not exist, download from Github.
        if not os.path.exists(self.appdir):
            os.makedirs(self.appdir)
        if not os.path.isfile(self.mp):
            url = 'https://github.com/drdhaval2785/python-prakriya/releases/download/v0.0.2/mapforms2.json'
            import requests
            # print('Downloading mapform file. Roughly 8 MB.')
            with open(self.mp, "wb") as f:
                r = requests.get(url)
                f.write(r.content)
        self.data = readJson(os.path.join(self.appdir, 'mapforms2.json'))
        if not os.path.isfile(os.path.join(self.appdir, 'verbmap.json')):
            url = 'https://github.com/drdhaval2785/python-prakriya/releases/download/v0.0.2/verbmap.json'
            import requests
            # print('Downloading verbmap file. Roughly 32 KB.')
            with open(os.path.join(self.appdir, 'verbmap.json'), "wb") as f:
                r = requests.get(url)
                f.write(r.content)
        self.verbmap = readJson(os.path.join(self.appdir, 'verbmap.json'))

    def inputTranslit(self, tran):
        """Set input transliteration."""
        # If valid transliteration, set transliteration.
        if tran in self.validtrans:
            self.inTran = tran
        # If not valid, throw error.
        else:
            print('Error. Not a valid transliteration scheme.')
            exit(0)

    def outputTranslit(self, tran):
        """Set output transliteration."""
        # If valid transliteration, set transliteration.
        if tran in self.validtrans:
            self.outTran = tran
        # If not valid, throw error.
        else:
            print('Error. Not a valid transliteration scheme.')
            exit(0)

    def getforms(self, inputverb, lakara='', purusha='', vachana='', suffix=''):
        # Change the transliteration to SLP1.
        inputverb = convert(inputverb, self.inTran, 'slp1')
        lakara = convert(lakara, self.inTran, 'slp1')
        suffix = convert(suffix, self.inTran, 'slp1')
        purusha = convert(purusha, self.inTran, 'slp1')
        vachana = convert(vachana, self.inTran, 'slp1')
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
        output = self.removeUnnecessary(wholeresult, lakara, suffices)
        # Transliterate the output
        outputstr = json.dumps(output)
        outputstr = convert(outputstr, 'slp1', self.outTran)
        output = json.loads(outputstr)
        return output


    def removeUnnecessary(self, wholeresult, lakara='', suffices=['']):
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
                arguments = [convert(member.decode('utf-8'), self.inTran, 'slp1') for member in items[1:]]
            # py3
            elif len(items) > 1:
                arguments = [convert(member, self.inTran, 'slp1') for member in items[1:]]
            # Convert verbform from desired input transliteration to SLP1.
            if sys.version_info[0] < 3:
                inputverb = inputverb.decode('utf-8')
            inputverb = convert(inputverb, self.inTran, 'slp1')
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
        return json.loads(convert(json.dumps(result), 'slp1', self.outTran))


def getsuffix(purusha, vachana):
    if purusha == 'praTama' and vachana == 'eka':
        return ['tip', 'ta']
    elif purusha == 'praTama' and vachana == 'dvi':
        return ['tas', 'AtAm']
    elif purusha == 'praTama' and vachana == 'bahu':
        return ['Ji', 'Ja']
    elif purusha == 'maDyama' and vachana == 'eka':
        return ['sip', 'TAs']
    elif purusha == 'maDyama' and vachana == 'dvi':
        return ['Tas', 'ATAm']
    elif purusha == 'maDyama' and vachana == 'bahu':
        return ['Ta', 'Dvam']
    elif purusha == 'uttama' and vachana == 'eka':
        return ['mip', 'iw']
    elif purusha == 'uttama' and vachana == 'dvi':
        return ['vas', 'vahi']
    elif purusha == 'uttama' and vachana == 'bahu':
        return ['mas', 'mahiN']

