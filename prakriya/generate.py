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
import ujson
import tarfile
from .utils import appDir, readJson, convert
from indic_transliteration import sanscript
# import datetime


def getsuffix(purusha, vachana, suffix):
    if suffix not in ['', u'']:
        return [suffix]
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
    if suffix not in ['tip', 'tas', 'Ji', 'sip', 'Tas', 'Ta', 'mip', 'vas',
                      'mas', 'ta', 'AtAm', 'Ja', 'TAs', 'ATAm', 'Dvam', 'iw',
                      'vahi', 'mahiN']:
        print({'error': 'Select proper suffix.'})
        exit(0)
    data = readJson(os.path.join(appDir('prakriya'), 'mapforms.json'))

    suffices = getsuffix(purusha, vachana, suffix)
    result = []
    for suffix in suffices:
        if suffix in data[verb][tense]:
            lst = data[verb][tense][suffix]
            for member in lst:
                if member[0] not in result:
                    result.append(member[0])
    if len(result) == 0:
        print({'error': 'Data is not available.'})
        exit(0)
    return result
