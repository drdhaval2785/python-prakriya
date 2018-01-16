#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prakriya` package."""


import unittest
import json
import os.path
from click.testing import CliRunner
from prakriya import Prakriya, Generate
from prakriya import cli


def readJson(path):
    """Read the given JSON file into python object."""
    with open(path, 'r') as fin:
        return json.load(fin)


def comparetranslit(verbform, inTran, outTran, arguments=''):
    p = Prakriya()
    p.inputTranslit(inTran)
    p.outputTranslit(outTran)
    calculated = p[verbform, arguments]
    superdata = readJson(os.path.join('tests', 'testdata', 'Bavati.json'))
    wholedata = superdata[outTran]
    if arguments == '':
        assert(calculated == wholedata)
    else:
        result = [member[arguments] for member in wholedata]
        assert(calculated == result)


class TestPrakriya(unittest.TestCase):
    """Tests for `prakriya` package."""

    def test_setUp(self):
        """Set up test fixtures, if any."""
        p = Prakriya()
        p.decompress()
        print(p['Bavati'])

    def test_false_input(self):
        """Test for false input transliteration."""
        p = Prakriya()
        with self.assertRaises(SystemExit):
            p.inputTranslit('asdfasdf')

    def test_false_output(self):
        """Test for false output transliteration."""
        p = Prakriya()
        with self.assertRaises(SystemExit):
            p.outputTranslit('fdasfdas')

    def test_bhavati(self):
        """Test something."""
        for (verbform, inTran) in [('Bavati', 'slp1'), ('ഭവതി', 'malayalam'),
                                   ('భవతి', 'telugu'), ('bhavati', 'iast'),
                                   ('भवति', 'devanagari'), ('Bavawi', 'wx'),
                                   ('ભવતિ', 'gujarati'), ('bhavati', 'itrans'),
                                   ('ଭଵତି', 'oriya'), ('ಭವತಿ', 'kannada'),
                                   ('bhavati', 'hk'), ('ভবতি', 'bengali'),
                                   ('ਭਵਤਿ', 'gurmukhi')]:
            for outTran in ['slp1', 'itrans', 'hk', 'iast', 'devanagari', 'wx',
                            'bengali', 'gujarati', 'gurmukhi', 'kannada',
                            'malayalam', 'oriya', 'telugu']:
                print('Testing ' + inTran + ' ' + outTran)
                comparetranslit(verbform, inTran, outTran)
                comparetranslit(verbform, inTran, outTran, 'prakriya')
                comparetranslit(verbform, inTran, outTran, 'verb')
                comparetranslit(verbform, inTran, outTran, 'verbaccent')
                comparetranslit(verbform, inTran, outTran, 'lakara')
                comparetranslit(verbform, inTran, outTran, 'gana')
                comparetranslit(verbform, inTran, outTran, 'meaning')
                comparetranslit(verbform, inTran, outTran, 'number')
                comparetranslit(verbform, inTran, outTran, 'madhaviya')
                comparetranslit(verbform, inTran, outTran, 'kshiratarangini')
                comparetranslit(verbform, inTran, outTran, 'dhatupradipa')
                comparetranslit(verbform, inTran, outTran, 'jnu')
                comparetranslit(verbform, inTran, outTran, 'uohyd')
                comparetranslit(verbform, inTran, outTran, 'upasarga')
                comparetranslit(verbform, inTran, outTran, 'padadecider_id')
                comparetranslit(verbform, inTran, outTran, 'padadecider_sutra')
                comparetranslit(verbform, inTran, outTran, 'it_id')
                comparetranslit(verbform, inTran, outTran, 'it_status')
                comparetranslit(verbform, inTran, outTran, 'it_sutra')
                comparetranslit(verbform, inTran, outTran, 'purusha')
                comparetranslit(verbform, inTran, outTran, 'vachana')

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main, ['Bavati', 'prakriya'])
        assert(result.exit_code == 0)
        assert('BUvAdayo DAtavaH' in result.output)
        help_result = runner.invoke(cli.main, ['--help'])
        assert(help_result.exit_code == 0)
        assert('Show this message and exit.' in help_result.output)
        result1 = runner.invoke(cli.generate, ['BU', 'law', 'praTama', 'eka'])
        assert(result1.exit_code == 0)
        assert('Bavati' in result1.output)

    def test_generate(self):
        """Test generation class."""
        g = Generate()
        assert(g['BU', 'law', 'praTama', 'eka'] == [u'Bavati', u'BAvayati', u'BAvayate'])
        assert(g['BU', 'law', 'praTama', 'dvi'] == [u'BavataH', u'BAvayataH', u'BAvayete'])
        assert(g['BU', 'law', 'praTama', 'bahu'] == [u'Bavanti', u'BAvayanti', u'BAvayante'])
        assert(g['BU', 'law', 'maDyama', 'eka'] == [u'Bavasi', u'BAvayasi', u'BAvayase'])
        assert(g['BU', 'law', 'maDyama', 'dvi'] == [u'BavaTaH', u'BAvayaTaH', u'BAvayeTe'])
        assert(g['BU', 'law', 'maDyama', 'bahu'] == [u'BavaTa', u'BAvayaTa', u'BAvayaDve'])
        assert(g['BU', 'law', 'uttama', 'eka'] == [u'BavAmi', u'BAvayAmi', u'BAvaye'])
        assert(g['BU', 'law', 'uttama', 'dvi'] == [u'BavAvaH', u'BAvayAvaH', u'BAvayAvahe'])
        assert(g['BU', 'law', 'uttama', 'bahu'] == [u'BavAmaH', u'BAvayAmaH', u'BAvayAmahe'])
        assert(g['BU', 'low', 'tip'] == [u'BAvayatu', u'BAvayatAt', u'Bavatu', u'BavatAt'])
        assert(g['BU', 'low', 'tas'] == [u'BAvayatAm', u'BavatAm'])
        assert(g['BU', 'low', 'Ji'] == [u'BAvayantu', u'Bavantu'])
        assert(g['BU', 'low', 'sip'] == [u'BAvaya', u'BAvayatAt', u'Bava', u'BavatAt'])
        assert(g['BU', 'low', 'Tas'] == [u'BAvayatam', u'Bavatam'])
        assert(g['BU', 'low', 'Ta'] == [u'BAvayata', u'Bavata'])
        assert(g['BU', 'low', 'mip'] == [u'BAvayAni', u'BavAni'])
        assert(g['BU', 'low', 'vas'] == [u'BAvayAva', u'BavAva'])
        assert(g['BU', 'low', 'mas'] == [u'BAvayAma', u'BavAma'])
        # Test for stripped verbs.
        assert(g['eD', 'low', 'Ja'] == [u'eDantAm'])
        g.inputTranslit('hk')
        g.outputTranslit('itrans')
        assert(g['bhU', 'laT', 'jhi'] == [u'bhavanti', u'bhAvayanti'])
        g.inputTranslit('devanagari')
        g.outputTranslit('iast')
        assert(g['भू', 'लट्', 'झि'] == [u'bhavanti', u'bh\u0101vayanti'])

    def test_false_in(self):
        """Test for false input transliteration."""
        g = Generate()
        with self.assertRaises(SystemExit):
            g.inputTranslit('asdfasdf')

    def test_false_out(self):
        """Test for false output transliteration."""
        g = Generate()
        with self.assertRaises(SystemExit):
            g.outputTranslit('fdasfdas')

    def test_absent_purusha_vachana(self):
        """Test for false output transliteration."""
        g = Generate()
        with self.assertRaises(SystemExit):
            g['BU', 'law']

    def test_absent_purusha(self):
        """Test for false output transliteration."""
        g = Generate()
        with self.assertRaises(SystemExit):
            g['BU', 'law' 'eka']

    def test_absent_vachana(self):
        """Test for false output transliteration."""
        g = Generate()
        with self.assertRaises(SystemExit):
            g['BU', 'law', 'maDyama']

    def test_absent_lakara(self):
        """Test for false output transliteration."""
        g = Generate()
        with self.assertRaises(SystemExit):
            g['BU']

    def test_absent_verb(self):
        """Test for false output transliteration."""
        g = Generate()
        with self.assertRaises(SystemExit):
            g['adsfasdf', 'tip']
