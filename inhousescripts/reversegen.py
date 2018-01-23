#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate the derivation for given verb and tense."""


import glob
import os
import csv
import ujson
import datetime


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


def reversegen():
    appdata = appDir('prakriya')
    result = {}
    with open(os.path.join(appdata, 'verbdetail.json')) as verbdetailfile:
        verbdetail = ujson.loads(verbdetailfile.read())
    with open(os.path.join(appdata, 'generatedcsv11012018.csv')) as csvfile:
        reader = csv.DictReader(csvfile, ['verbform', 'verb', 'lakara',
                                          'suffix', 'number'])
        counter = 1
        for row in reader:
            verbform = row['verbform']
            verb = row['verb']
            lakara = row['lakara']
            suffix = row['suffix']
            number = row['number']
            # Extract necessary details from verbdetail.json
            verbdet = verbdetail[number]
            verbwithoutanubandha = verbdet['verbwithoutanubandha']
            if verb not in result:
                result[verb] = {}
            if number not in result[verb]:
                result[verb][number] = {}
                # Add additional information about that verb.
                result[verb][number]['gana'] = verbdet['gana']
                result[verb][number]['meaning'] = verbdet['meaning']
                result[verb][number]['verbwithoutanubandha'] = verbdet['verbwithoutanubandha']
                result[verb][number]['padI'] = verbdet['padI']
                result[verb][number]['it'] = verbdet['it']
            if lakara not in result[verb][number]:
                result[verb][number][lakara] = {}
            if suffix not in result[verb][number][lakara]:
                result[verb][number][lakara][suffix] = []
            result[verb][number][lakara][suffix].append(verbform)
            if counter % 100 == 0:
                print counter
            counter += 1
        ujson.dump(result, open(os.path.join(appdata, 'mapforms2.json'), 'w'))

reversegen()
def printrevgen():
    print(datetime.datetime.now())
    data = ujson.loads(open(os.path.join(appdata, 'mapforms.json')).read())
    print(data['BU']['law']['mas'])
    print(datetime.datetime.now())
