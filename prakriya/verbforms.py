#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create a python library which returns details about a verb form.

Example
-------

>>> from prakriya import Prakriya
>>> p = Prakriya()
# If you are using the library the first time, be patient.
# This will take a long time, because the data file (30 MB) is being downloaded.
# If you can spare around 600 MB space, decompress the tar.gz first time.
# Subsequent actions will be very fast. This is one time requirement.
>>> p.decompress()
>>> p['Bavati']
>>> p['Bavati', 'prakriya']
>>> p['Bavati', 'verb']

For details of valid arguments, see documentation on prakriya class.
"""
import os.path
import json
import sys
import tarfile
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

    Example
    -------
    >>> from verbforms import Prakriya
    >>> p = Prakriya()
    # If you are using the library the first time, be patient.
    # This will take a long time, because the data file (30 MB) is being downloaded.
    # If you can spare around 600 MB space, decompress the tar.gz first time.
    # Subsequent actions will be very fast. This is one time requirement.
    >>> p.decompress()
    >>> p['Bavati']
    [{u'gana': u'BvAdi', u'verb': u'BU', u'dhatupradipa': u'http://sanskrit.uohyd.ac.in/scl/dhaatupaatha/files-15-03-2017//XA1.html', u'kshiratarangini': u'http://sanskrit.uohyd.ac.in/scl/dhaatupaatha/files-15-03-2017//kRi1.html', u'padadecider_sutra': u'', u'jnu': u'http://sanskrit.jnu.ac.in/tinanta/tinanta.jsp?t=1', u'padadecider_id': u'parasmEpadI', u'madhaviya': u'http://sanskrit.uohyd.ac.in/scl/dhaatupaatha/files-15-03-2017//mA1.html', 'prakriya': [{'sutra': u'BUvAdayo DAtavaH', 'sutra_num': u'1.3.1', 'form': u'BU'}, {'sutra': u'laH karmaRi ca BAve cAkarmakeByaH.', 'sutra_num': u'3.4.69', 'form': u'BU'}, {'sutra': u'vartamAne law', 'sutra_num': u'3.2.123', 'form': u'BU+la~w'}, {'sutra': u'lasya', 'sutra_num': u'3.4.77', 'form': u'BU+la~w'}, {'sutra': u'halantyam', 'sutra_num': u'1.3.3', 'form': u'BU+la~w'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+la~'}, {'sutra': u"upadeSe'janunAsika it", 'sutra_num': u'1.3.2', 'form': u'BU+la~'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+l'}, {'sutra': u'tiptasJisipTasTamibvasmas tAtAMJaTAsATAMDvamiqvahimahiN', 'sutra_num': u'3.4.78', 'form': u'BU+tip'}, {'sutra': u'laH parasmEpadam', 'sutra_num': u'1.4.99', 'form': u'BU+tip'}, {'sutra': u'tiNastrIRi trIRi praTamamaDyamottamAH', 'sutra_num': u'1.4.101', 'form': u'BU+tip'}, {'sutra': u'tAnyekavacanadvivacanabahuvacanAnyekaSaH', 'sutra_num': u'1.4.102', 'form': u'BU+tip'}, {'sutra': u'Seze praTamaH', 'sutra_num': u'1.4.108', 'form': u'BU+tip'}, {'sutra': u'tiNSitsArvaDAtukam', 'sutra_num': u'3.4.113', 'form': u'BU+tip'}, {'sutra': u'kartari Sap\u200c', 'sutra_num': u'3.1.68', 'form': u'BU+Sap+tip'}, {'sutra': u'tiNSitsArvaDAtukam', 'sutra_num': u'3.4.113', 'form': u'BU+Sap+tip'}, {'sutra': u'laSakvatadDite', 'sutra_num': u'1.3.8', 'form': u'BU+Sap+tip'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+ap+tip'}, {'sutra': u'halantyam', 'sutra_num': u'1.3.3', 'form': u'BU+ap+tip'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+a+ti'}, {'sutra': u'sArvaDAtukArDaDAtukayoH', 'sutra_num': u'7.3.84', 'form': u'Bo+a+ti'}, {'sutra': u"eco'yavAyAvaH", 'sutra_num': u'6.1.78', 'form': u'Bav+a+ti'}, {'sutra': u'antimaM rUpam', 'sutra_num': u'-2', 'form': u'Bavati'}], u'number': u'01.0001', u'uohyd': u'http://sanskrit.uohyd.ac.in/cgi-bin/scl/skt_gen/verb/verb_gen.cgi?vb=BU1_BU_BvAxiH_sawwAyAm&prayoga=karwari&encoding=WX&upasarga=-&paxI=parasmEpaxI', u'it_status': u'', u'meaning': u'sattAyAm', u'vachana': u'eka', u'purusha': u'praTama', u'verbaccent': u'\u092d\u0942\u0951', u'lakara': u'law', u'it_id': u'', u'it_sutra': u'', u'upasarga': u'', u'suffix': u'tip'}]
    >>> p['Bavati', 'verb']
    [u'BU']
    >>> p['Bavati', 'prakriya']
    [[{'sutra': u'BUvAdayo DAtavaH', 'sutra_num': u'1.3.1', 'form': u'BU'}, {'sutra': u'laH karmaRi ca BAve cAkarmakeByaH.', 'sutra_num': u'3.4.69', 'form': u'BU'}, {'sutra': u'vartamAne law', 'sutra_num': u'3.2.123', 'form': u'BU+la~w'}, {'sutra': u'lasya', 'sutra_num': u'3.4.77', 'form': u'BU+la~w'}, {'sutra': u'halantyam', 'sutra_num': u'1.3.3', 'form': u'BU+la~w'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+la~'}, {'sutra': u"upadeSe'janunAsika it", 'sutra_num': u'1.3.2', 'form': u'BU+la~'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+l'}, {'sutra': u'tiptasJisipTasTamibvasmas tAtAMJaTAsATAMDvamiqvahimahiN', 'sutra_num': u'3.4.78', 'form': u'BU+tip'}, {'sutra': u'laH parasmEpadam', 'sutra_num': u'1.4.99', 'form': u'BU+tip'}, {'sutra': u'tiNastrIRi trIRi praTamamaDyamottamAH', 'sutra_num': u'1.4.101', 'form': u'BU+tip'}, {'sutra': u'tAnyekavacanadvivacanabahuvacanAnyekaSaH', 'sutra_num': u'1.4.102', 'form': u'BU+tip'}, {'sutra': u'Seze praTamaH', 'sutra_num': u'1.4.108', 'form': u'BU+tip'}, {'sutra': u'tiNSitsArvaDAtukam', 'sutra_num': u'3.4.113', 'form': u'BU+tip'}, {'sutra': u'kartari Sap\u200c', 'sutra_num': u'3.1.68', 'form': u'BU+Sap+tip'}, {'sutra': u'tiNSitsArvaDAtukam', 'sutra_num': u'3.4.113', 'form': u'BU+Sap+tip'}, {'sutra': u'laSakvatadDite', 'sutra_num': u'1.3.8', 'form': u'BU+Sap+tip'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+ap+tip'}, {'sutra': u'halantyam', 'sutra_num': u'1.3.3', 'form': u'BU+ap+tip'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+a+ti'}, {'sutra': u'sArvaDAtukArDaDAtukayoH', 'sutra_num': u'7.3.84', 'form': u'Bo+a+ti'}, {'sutra': u"eco'yavAyAvaH", 'sutra_num': u'6.1.78', 'form': u'Bav+a+ti'}, {'sutra': u'antimaM rUpam', 'sutra_num': u'-2', 'form': u'Bavati'}]]

    """

    def __init__(self, decompress=False):
        """Start the class. Decompress tar file if asked for."""
        # Find the directory of the module.
        self.directory = os.path.abspath(os.path.dirname(__file__))
        # Path where to store the file
        self.filename = 'composite_v002.tar.gz'
        self.tr = os.path.join(self.directory, 'data', self.filename)
        # If the file does not exist, download from Github.
        if not os.path.isfile(self.tr):
            url = 'https://github.com/drdhaval2785/python-prakriya/raw/master/prakriya/data/' + self.filename
            import requests
            print('Downloading data file. It will take a few minutes. Please be patient.')
            with open(self.tr, "wb") as f:
                r = requests.get(url)
                f.write(r.content)
            print('Completed downloading data file.')
            print('If you can spare 600 MB of storage space, use .decompress() method. This will speed up subsequent runs very fast.')
        # Open self.tar so that it can be used by function later on.
        self.tar = tarfile.open(self.tr, 'r:gz')

    def decompress(self):
        """Decompress the tar file if user asks for it.

        It makes the future operations very fast.
        """
        self.tar.extractall(os.path.join(self.directory, 'data'))
        print("data files extracted. You shall not need to use decompress() function again. Just do regular `p = Prakriya()`.")

    def __getitem__(self, items):
        """Return the requested data by user."""
        # Initiate without arguments
        argument = ''
        # print(datetime.datetime.now())
        # If there is only one entry in items, it is treated as verbform.
        if isinstance(items, str):
            verbform = items
        # Otherwise, first is verbform and the next is argument1.
        else:
            verbform = items[0]
            if len(items) > 1:
                argument = items[1]
        # Read from tar.gz file.
        data = get_full_data_from_composite(verbform, self.tar)
        # If there is no argument, return whole data.
        if argument == '':
            result = data
        # Else, keep only the data related to the provided argument.
        else:
            result = keepSpecific(data, argument)
        # print(datetime.datetime.now())
        # Return the result.
        return result


def get_full_data_from_composite(verbform, tar):
    """Get whole data from the json file for given verb form."""
    # Find the parent directory
    storagedirectory = os.path.abspath(os.path.dirname(__file__))
    # keep only first thee letters from verbform
    slugname = verbform[:3]
    # path of json file.
    jsonofinterest = os.path.join(storagedirectory, 'data', 'jsonsorted', slugname + '.json')
    # If the json is not already extracted in earlier usages, extract that.
    if not os.path.isfile(jsonofinterest):
        member = tar.getmember('jsonsorted/' + slugname + '.json')
        tar.extract(member, path=os.path.join(storagedirectory, 'data'))
    # Load from json file. Data is in {verbform1: verbdata1, verbform2: verbdata2 ...} format.
    fin = open(jsonofinterest, 'r')
    compositedata = json.load(fin)
    fin.close()
    # Keep only the data related to inquired verbform.
    data = compositedata[verbform]
    # Initialize empty result stack.
    result = []
    # Read sutrainfo file. This is needed to convert sutra_num to sutra_text.
    with open(os.path.join(storagedirectory, 'data', 'sutrainfo.json'), 'r') as sutrafile:
        sutrainfo = json.load(sutrafile)
    # For each possible derivation leading to the given verb form, e.g. baBUva can be from BU, asa~
    for datum in data:
        # Initialize a subresult stack as dict. key will be argument and value will be data.
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
                subresult[item] = tmp
            # derivation is a list (as compared to others which are strings.)
            elif item == 'derivation':
                # For member of the list
                for member in datum['derivation']:
                    # Fetch sutratext
                    sutratext = sutrainfo[member['sutra_num']]
                    # Replace tilde with hyphen. Otherwise wrong transliteration will happen.
                    sutranum = member['sutra_num'].replace('~', '-')
                    # A decent representation for rutva.
                    form = member['form'].replace('@', 'u~')
                    # Add to derivationlist.
                    derivationlist.append({'sutra': sutratext, 'sutra_num': sutranum, 'form': form})
        # Add the derivationlist to the prakriya key.
        subresult['prakriya'] = derivationlist
        # Append subresult to result and start again.
        result.append(subresult)
    # Give result.
    return result


def keepSpecific(data, argument):
    """Create a list of only the relavent argument."""
    return [member[argument] for member in data]


if __name__ == '__main__':
    # print(timestamp())
    syslen = len(sys.argv)
    # There can be only zero / one argument. Throw error otherwise.
    if syslen < 2 or syslen > 3:
        print(json.dumps({'error': 'Kindly use the following syntax. `python prakriya.py verbform [argument]`.'}))
        exit(0)
    # Initialize verbform
    if syslen >= 2:
        verbform = sys.argv[1]
    # Initialize argument, if any.
    if syslen == 3:
        argument = sys.argv[2]
    # Parent directory.
    directory = os.path.abspath(os.path.dirname(__file__))
    # Path to tar.gz file.
    tr = os.path.join(directory, 'data', 'composite_v002.tar.gz')
    # Open tar file
    tar = tarfile.open(tr, 'r:gz')
    # Fetch data. In the process, function also decompresses the queried json.
    data = get_full_data_from_composite(verbform, tar)
    # If there is no argument, return the whole data.
    if syslen == 2:
        result = data
    # If there is an argument, return only the data relavent to that argument.
    else:
        result = keepSpecific(data, argument)
    # Print result to the screen with proper indenting.
    print(json.dumps(result, indent=4, encoding='utf-8'))
