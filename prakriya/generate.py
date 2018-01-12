#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create a python library which gives derivation for given verb and tense.

Example
-------

>>> from prakriya import Generate
>>> g = Generate()
# If you are using the library the first time, be patient.
# This will take a long time.
# Data file (30 MB) is being downloaded.
# If you can spare around 600 MB space, decompress the tar.gz first time.
# Subsequent actions will be very fast. This is one time requirement.
>>> g.decompress()
The format is as follows
>>> g[verb, tense]
Actual usage will be like the following.
>>> g['BU']
>>> g['BU', 'law']

For details of valid values for field, see documentation on prakriya class.
"""
import os.path
import sys
from .utils import appDir, readJson, convert
# import datetime


class Generate():
    """Class to get the verb form from given verb, tense, suffix."""

    def __init__(self):
        self.appdir = appDir('prakriya')
        self.data = readJson(os.path.join(self.appdir, 'mapforms.json'))
        self.inTran = 'slp1'
        self.outTran = 'slp1'

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

    def __getitem__(self, items):
        """Return the requested data by user."""
        # Initiate without arguments
        arguments = ''
        # print(datetime.datetime.now())
        # If there is only one entry in items, it is treated as verbform.
        if isinstance(items, ("".__class__, u"".__class__)):
            print({'error': 'Provide purusha and vachana or suffix.'})
            exit(0)
        else:
            # Otherwise, first is verbform and the next is argument1.
            verb = items[0]
            if len(items) > 1:
                arguments = items[1:]
            # Define default values
            tense = 'law'
            purusha = 'praTama'
            vachana = 'eka'
            suffix = ''
            # Enter user defined values
            for member in arguments:
                if member in ['law', 'liw', 'luw', 'lfw', 'low', 'laN',
                              'viDiliN', 'ASIrliN', 'luN', 'lfN']:
                    tense = member
                if member in ['praTama', 'maDyama', 'uttama']:
                    purusha = member
                if member in ['eka', 'dvi', 'bahu']:
                    vachana = member
                if member in ['tip', 'tas', 'Ji', 'sip', 'Tas', 'Ta', 'mip',
                              'vas', 'mas', 'ta', 'AtAm', 'Ja', 'TAs', 'ATAm',
                              'Dvam', 'iw', 'vahi', 'mahiN']:
                    suffix = member
            if suffix == '':
                suffix = getsuffix(purusha, vachana)
        # Convert verbform from desired input transliteration to SLP1.
        if sys.version_info[0] < 3:
            verb = verb.decode('utf-8')
        verb = convert(verb, self.inTran, 'slp1')
        # Read from tar.gz file.
        result = getform(verb, tense, purusha, vachana, suffix)
        # Return the result.
        result = [convert(member, 'slp1', self.outTran) for member in result]
        return result


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


def getform(verb, tense='law', purusha='praTama', vachana='eka', suffix=''):
    if tense not in ['law', 'liw', 'luw', 'lfw', 'low', 'laN', 'viDiliN',
                     'ASIrliN', 'luN', 'lfN']:
        print({'error': 'Select proper tense.'})
        exit(0)
    if purusha not in ['praTama', 'maDyama', 'uttama']:
        print({'error': 'Select proper purusha.'})
        exit(0)
    if vachana not in ['eka', 'dvi', 'bahu']:
        print({'error': 'Select proper vachana.'})
        exit(0)
    data = readJson(os.path.join(appDir('prakriya'), 'mapforms.json'))

    result = []
    if not isinstance(suffix, ("".__class__, u"".__class__)):
        suffices = getsuffix(purusha, vachana)
    else:
        suffices = [suffix]
    for suffix in suffices:
        if suffix not in ['tip', 'tas', 'Ji', 'sip', 'Tas', 'Ta', 'mip', 'vas',
                          'mas', 'ta', 'AtAm', 'Ja', 'TAs', 'ATAm', 'Dvam', 'iw',
                          'vahi', 'mahiN']:
            print({'error': 'Select proper suffix.'})
            exit(0)
        if suffix in data[verb][tense]:
            lst = data[verb][tense][suffix]
            for member in lst:
                if member[0] not in result:
                    result.append(member[0])
    if len(result) == 0:
        print({'error': 'Data is not available.'})
        exit(0)
    return result
