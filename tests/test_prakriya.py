#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prakriya` package."""


import unittest
import json
import os.path
from click.testing import CliRunner
from prakriya import Prakriya, VerbFormGenerator
from prakriya import cli


def readJson(path):
    """Read the given JSON file into python object."""
    with open(path, 'r') as fin:
        return json.load(fin)


def comparetranslit(verbform, inTran, outTran, arguments=''):
    p = Prakriya()
    p.inputTranslit(inTran)
    p.outputTranslit(outTran)
    calculated = p.get_info(verbform, arguments)
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
        g = VerbFormGenerator()
        # assert(g['BU', 'law', 'praTama', 'eka'] == {u'10.0277': [u'BAvayate'], u'10.0382': [u'BAvayate'], u'01.0001': [u'Bavati']})
        # assert(g['BU', 'law', 'praTama', 'dvi'] == {u'10.0277': [u'BAvayete'], u'10.0382': [u'BAvayete'], u'01.0001': [u'BavataH']})
        # assert(g['BU', 'law', 'praTama', 'bahu'] == {u'10.0277': [u'BAvayante'], u'10.0382': [u'BAvayante'], u'01.0001': [u'Bavanti']})
        # assert(g['BU', 'law', 'maDyama', 'eka'] == {u'10.0277': [u'BAvayase'], u'10.0382': [u'BAvayase'], u'01.0001': [u'Bavasi']})
        # assert(g['BU', 'law', 'maDyama', 'dvi'] == {u'10.0277': [u'BAvayeTe'], u'10.0382': [u'BAvayeTe'], u'01.0001': [u'BavaTaH']})
        # assert(g['BU', 'law', 'maDyama', 'bahu'] == {u'10.0277': [u'BAvayaDve'], u'10.0382': [u'BAvayaDve'], u'01.0001': [u'BavaTa']})
        # assert(g['BU', 'law', 'uttama', 'eka'] == {u'10.0277': [u'BAvaye'], u'10.0382': [u'BAvaye'], u'01.0001': [u'BavAmi']})
        # assert(g['BU', 'law', 'uttama', 'dvi'] == {u'10.0277': [u'BAvayAvahe'], u'10.0382': [u'BAvayAvahe'], u'01.0001': [u'BavAvaH']})
        # assert(g['BU', 'law', 'uttama', 'bahu'] == {u'10.0277': [u'BAvayAmahe'], u'10.0382': [u'BAvayAmahe'], u'01.0001': [u'BavAmaH']})
        # assert(g['BU', 'low', 'tip'] == {u'10.0277': [u'BAvayatu', u'BAvayatAt'], u'10.0382': [u'BAvayatu', u'BAvayatAt'], u'01.0001': [u'Bavatu', u'BavatAt']})
        # assert(g['BU', 'low', 'tas'] == {u'10.0277': [u'BAvayatAm'], u'10.0382': [u'BAvayatAm'], u'01.0001': [u'BavatAm']})
        # assert(g['BU', 'low', 'Ji'] == {u'10.0277': [u'BAvayantu'], u'10.0382': [u'BAvayantu'], u'01.0001': [u'Bavantu']})
        # assert(g['BU', 'low', 'sip'] == {u'10.0277': [u'BAvaya', u'BAvayatAt'], u'10.0382': [u'BAvaya', u'BAvayatAt'], u'01.0001': [u'Bava', u'BavatAt']})
        # assert(g['BU', 'low', 'Tas'] == {u'10.0277': [u'BAvayatam'], u'10.0382': [u'BAvayatam'], u'01.0001': [u'Bavatam']})
        # assert(g['BU', 'low', 'Ta'] == {u'10.0277': [u'BAvayata'], u'10.0382': [u'BAvayata'], u'01.0001': [u'Bavata']})
        # assert(g['BU', 'low', 'mip'] == {u'10.0277': [u'BAvayAni'], u'10.0382': [u'BAvayAni'], u'01.0001': [u'BavAni']})
        # assert(g['BU', 'low', 'vas'] == {u'10.0277': [u'BAvayAva'], u'10.0382': [u'BAvayAva'], u'01.0001': [u'BavAva']})
        # assert(g['BU', 'low', 'mas'] == {u'10.0277': [u'BAvayAma'], u'10.0382': [u'BAvayAma'], u'01.0001': [u'BavAma']})
        # Test for stripped verbs.
        # assert(g['eD', 'lfw', 'Ja'] == {u'01.0002': [u'eDizyante']})
		
		# Tests changed to use getforms function
        assert(g.getforms('BU', 'law', 'praTama', 'eka') == {u'10.0277': [u'BAvayate'], u'10.0382': [u'BAvayate'], u'01.0001': [u'Bavati']})
        assert(g.getforms('BU', 'law', 'praTama', 'dvi') == {u'10.0277': [u'BAvayete'], u'10.0382': [u'BAvayete'], u'01.0001': [u'BavataH']})
        assert(g.getforms('BU', 'law', 'praTama', 'bahu') == {u'10.0277': [u'BAvayante'], u'10.0382': [u'BAvayante'], u'01.0001': [u'Bavanti']})
        assert(g.getforms('BU', 'law', 'maDyama', 'eka') == {u'10.0277': [u'BAvayase'], u'10.0382': [u'BAvayase'], u'01.0001': [u'Bavasi']})
        assert(g.getforms('BU', 'law', 'maDyama', 'dvi') == {u'10.0277': [u'BAvayeTe'], u'10.0382': [u'BAvayeTe'], u'01.0001': [u'BavaTaH']})
        assert(g.getforms('BU', 'law', 'maDyama', 'bahu')== {u'10.0277': [u'BAvayaDve'], u'10.0382': [u'BAvayaDve'], u'01.0001': [u'BavaTa']})
        assert(g.getforms('BU', 'law', 'uttama', 'eka') == {u'10.0277': [u'BAvaye'], u'10.0382': [u'BAvaye'], u'01.0001': [u'BavAmi']})
        assert(g.getforms('BU', 'law', 'uttama', 'dvi') == {u'10.0277': [u'BAvayAvahe'], u'10.0382': [u'BAvayAvahe'], u'01.0001': [u'BavAvaH']})
        assert(g.getforms('BU', 'law', 'uttama', 'bahu') == {u'10.0277': [u'BAvayAmahe'], u'10.0382': [u'BAvayAmahe'], u'01.0001': [u'BavAmaH']})
        assert(g.getforms('BU', 'low', suffix='tip') == {u'10.0277': [u'BAvayatu', u'BAvayatAt'], u'10.0382': [u'BAvayatu', u'BAvayatAt'], u'01.0001': [u'Bavatu', u'BavatAt']})
        assert(g.getforms('BU', 'low', suffix='tas') == {u'10.0277': [u'BAvayatAm'], u'10.0382': [u'BAvayatAm'], u'01.0001': [u'BavatAm']})
        assert(g.getforms('BU', 'low', suffix='Ji') == {u'10.0277': [u'BAvayantu'], u'10.0382': [u'BAvayantu'], u'01.0001': [u'Bavantu']})
        assert(g.getforms('BU', 'low', suffix='sip') == {u'10.0277': [u'BAvaya', u'BAvayatAt'], u'10.0382': [u'BAvaya', u'BAvayatAt'], u'01.0001': [u'Bava', u'BavatAt']})
        assert(g.getforms('BU', 'low', suffix='Tas') == {u'10.0277': [u'BAvayatam'], u'10.0382': [u'BAvayatam'], u'01.0001': [u'Bavatam']})
        assert(g.getforms('BU', 'low', suffix='Ta') == {u'10.0277': [u'BAvayata'], u'10.0382': [u'BAvayata'], u'01.0001': [u'Bavata']})
        assert(g.getforms('BU', 'low', suffix='mip') == {u'10.0277': [u'BAvayAni'], u'10.0382': [u'BAvayAni'], u'01.0001': [u'BavAni']})
        assert(g.getforms('BU', 'low', suffix='vas') == {u'10.0277': [u'BAvayAva'], u'10.0382': [u'BAvayAva'], u'01.0001': [u'BavAva']})
        assert(g.getforms('BU', 'low', suffix='mas') == {u'10.0277': [u'BAvayAma'], u'10.0382': [u'BAvayAma'], u'01.0001': [u'BavAma']})
        # Test for stripped verbs.
        assert(g.getforms('eD', 'lfw', suffix='Ja') == {u'01.0002': [u'eDizyante']})

    def test_generate_without_suffix(self):
        g = VerbFormGenerator()
        # assert('01.0002' in g['eD', 'law'])
        # assert('01.0001' in g['BU', 'low'])
        # assert('01.0001' in g['BU'])
        assert('01.0002' in g.getforms('eD', suffix='law'))
        assert('01.0001' in g.getforms('BU', suffix='low'))
        assert('01.0001' in g.getforms('BU'))

    def test_generate_translit(self):
        g = VerbFormGenerator()
        g.inputTranslit('hk')
        g.outputTranslit('itrans')
        # assert(g['bhU', 'laT', 'jhi'] == {u'01.0001': [u'bhavanti'], u'10.0382': [u'bhAvayanti'], u'10.0277': [u'bhAvayanti']})
        assert(g.getforms('bhU', 'laT', suffix='jhi') == {u'01.0001': [u'bhavanti'], u'10.0382': [u'bhAvayanti'], u'10.0277': [u'bhAvayanti']})

    def test_false_in(self):
        """Test for false input transliteration."""
        g = VerbFormGenerator()
        with self.assertRaises(SystemExit):
            g.inputTranslit('asdfasdf')

    def test_false_out(self):
        """Test for false output transliteration."""
        g = VerbFormGenerator()
        with self.assertRaises(SystemExit):
            g.outputTranslit('fdasfdas')

    def test_wrong_verb(self):
        """Test for verb absent in database."""
        g = VerbFormGenerator()
        with self.assertRaises(SystemExit):
            # g['adsfasdf', 'tip']
            g.getforms('adsfasdf', suffix='tip')
