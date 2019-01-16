#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prakriya` package."""


import unittest
import json
import os.path
from click.testing import CliRunner
from prakriya import Prakriya, VerbFormGenerator
from prakriya import cli


def read_json(path):
    """Read the given JSON file into python object."""
    with open(path, 'r') as fin:
        return json.load(fin)


def comparetranslit(verbform, intran, outtran, arguments=''):
    """Compare the transliteration conversion from prestored data."""
    prak = Prakriya()
    prak.input_translit(intran)
    prak.output_translit(outtran)
    calculated = prak.get_info(verbform, arguments)
    superdata = read_json(os.path.join('tests', 'testdata', 'Bavati.json'))
    wholedata = superdata[outtran]
    if arguments == '':
        assert calculated == wholedata
    else:
        result = [member[arguments] for member in wholedata]
        assert calculated == result


class TestPrakriya(unittest.TestCase):
    """Tests for `prakriya` package."""

    def test_setup(self):
        """Set up test fixtures, if any."""
        prak = Prakriya()
        prak.decompress()
        print(prak['Bavati'])

    def test_false_input(self):
        """Test for false input transliteration."""
        prak = Prakriya()
        with self.assertRaises(SystemExit):
            prak.input_translit('asdfasdf')

    def test_false_output(self):
        """Test for false output transliteration."""
        prak = Prakriya()
        with self.assertRaises(SystemExit):
            prak.output_translit('fdasfdas')

    def test_bhavati(self):
        """Test somethingen."""
        for (verbform, intran) in [('Bavati', 'slp1'), ('ഭവതി', 'malayalam'),
                                   ('భవతి', 'telugu'), ('bhavati', 'iast'),
                                   ('भवति', 'devanagari'), ('Bavawi', 'wx'),
                                   ('ભવતિ', 'gujarati'), ('bhavati', 'itrans'),
                                   ('ଭଵତି', 'oriya'), ('ಭವತಿ', 'kannada'),
                                   ('bhavati', 'hk'), ('ভবতি', 'bengali'),
                                   ('ਭਵਤਿ', 'gurmukhi')]:
            for outtran in ['slp1', 'itrans', 'hk', 'iast', 'devanagari', 'wx',
                            'bengali', 'gujarati', 'gurmukhi', 'kannada',
                            'malayalam', 'oriya', 'telugu']:
                print('Testing ' + intran + ' ' + outtran)
                comparetranslit(verbform, intran, outtran)
                comparetranslit(verbform, intran, outtran, 'prakriya')
                comparetranslit(verbform, intran, outtran, 'verb')
                comparetranslit(verbform, intran, outtran, 'verbaccent')
                comparetranslit(verbform, intran, outtran, 'lakara')
                comparetranslit(verbform, intran, outtran, 'gana')
                comparetranslit(verbform, intran, outtran, 'meaning')
                comparetranslit(verbform, intran, outtran, 'number')
                comparetranslit(verbform, intran, outtran, 'madhaviya')
                comparetranslit(verbform, intran, outtran, 'kshiratarangini')
                comparetranslit(verbform, intran, outtran, 'dhatupradipa')
                comparetranslit(verbform, intran, outtran, 'jnu')
                comparetranslit(verbform, intran, outtran, 'uohyd')
                comparetranslit(verbform, intran, outtran, 'upasarga')
                comparetranslit(verbform, intran, outtran, 'padadecider_id')
                comparetranslit(verbform, intran, outtran, 'padadecider_sutra')
                comparetranslit(verbform, intran, outtran, 'it_id')
                comparetranslit(verbform, intran, outtran, 'it_status')
                comparetranslit(verbform, intran, outtran, 'it_sutra')
                comparetranslit(verbform, intran, outtran, 'purusha')
                comparetranslit(verbform, intran, outtran, 'vachana')

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main, ['Bavati', 'prakriya'])
        assert result.exit_code == 0
        assert 'BUvAdayo DAtavaH' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output
        result1 = runner.invoke(cli.generate, ['BU', 'law', 'praTama', 'eka'])
        assert result1.exit_code == 0
        assert 'Bavati' in result1.output

    def test_generate(self):
        """Test generation class."""
        gen = VerbFormGenerator()
        assert(gen['BU', 'law', 'praTama', 'eka'] == {u'10.0277': [
            u'BAvayate'], u'10.0382': [u'BAvayate'], u'01.0001': [u'Bavati']})
        assert(gen['BU', 'law', 'praTama', 'dvi'] == {u'10.0277': [
            u'BAvayete'], u'10.0382': [u'BAvayete'], u'01.0001': [u'BavataH']})
        assert(gen['BU', 'law', 'praTama', 'bahu'] == {u'10.0277': [
            u'BAvayante'], u'10.0382': [u'BAvayante'], u'01.0001': [u'Bavanti']})
        assert(gen['BU', 'law', 'maDyama', 'eka'] == {u'10.0277': [
            u'BAvayase'], u'10.0382': [u'BAvayase'], u'01.0001': [u'Bavasi']})
        assert(gen['BU', 'law', 'maDyama', 'dvi'] == {u'10.0277': [
            u'BAvayeTe'], u'10.0382': [u'BAvayeTe'], u'01.0001': [u'BavaTaH']})
        assert(gen['BU', 'law', 'maDyama', 'bahu'] == {u'10.0277': [
            u'BAvayaDve'], u'10.0382': [u'BAvayaDve'], u'01.0001': [u'BavaTa']})
        assert(gen['BU', 'law', 'uttama', 'eka'] == {u'10.0277': [
            u'BAvaye'], u'10.0382': [u'BAvaye'], u'01.0001': [u'BavAmi']})
        assert(gen['BU', 'law', 'uttama', 'dvi'] == {u'10.0277': [
            u'BAvayAvahe'], u'10.0382': [u'BAvayAvahe'], u'01.0001': [u'BavAvaH']})
        assert(gen['BU', 'law', 'uttama', 'bahu'] == {u'10.0277': [
            u'BAvayAmahe'], u'10.0382': [u'BAvayAmahe'], u'01.0001': [u'BavAmaH']})
        assert(gen['BU', 'low', 'tip'] == {u'10.0277': [u'BAvayatu', u'BAvayatAt'], u'10.0382': [
            u'BAvayatu', u'BAvayatAt'], u'01.0001': [u'Bavatu', u'BavatAt']})
        assert(gen['BU', 'low', 'tas'] == {u'10.0277': [u'BAvayatAm'], u'10.0382': [
            u'BAvayatAm'], u'01.0001': [u'BavatAm']})
        assert(gen['BU', 'low', 'Ji'] == {u'10.0277': [u'BAvayantu'], u'10.0382': [
            u'BAvayantu'], u'01.0001': [u'Bavantu']})
        assert(gen['BU', 'low', 'sip'] == {u'10.0277': [u'BAvaya', u'BAvayatAt'], u'10.0382': [
            u'BAvaya', u'BAvayatAt'], u'01.0001': [u'Bava', u'BavatAt']})
        assert(gen['BU', 'low', 'Tas'] == {u'10.0277': [u'BAvayatam'], u'10.0382': [
            u'BAvayatam'], u'01.0001': [u'Bavatam']})
        assert(gen['BU', 'low', 'Ta'] == {u'10.0277': [u'BAvayata'], u'10.0382': [
            u'BAvayata'], u'01.0001': [u'Bavata']})
        assert(gen['BU', 'low', 'mip'] == {u'10.0277': [
            u'BAvayAni'], u'10.0382': [u'BAvayAni'], u'01.0001': [u'BavAni']})
        assert(gen['BU', 'low', 'vas'] == {u'10.0277': [
            u'BAvayAva'], u'10.0382': [u'BAvayAva'], u'01.0001': [u'BavAva']})
        assert(gen['BU', 'low', 'mas'] == {u'10.0277': [
            u'BAvayAma'], u'10.0382': [u'BAvayAma'], u'01.0001': [u'BavAma']})
        # Test for stripped verbs.
        assert(gen['eD', 'lfw', 'Ja'] == {u'01.0002': [u'eDizyante']})

        # Tests changed to use getforms function
        assert(gen.getforms('BU', 'law', 'praTama', 'eka') == {u'10.0277': [
            u'BAvayate'], u'10.0382': [u'BAvayate'], u'01.0001': [u'Bavati']})
        assert(gen.getforms('BU', 'law', 'praTama', 'dvi') == {u'10.0277': [
            u'BAvayete'], u'10.0382': [u'BAvayete'], u'01.0001': [u'BavataH']})
        assert(gen.getforms('BU', 'law', 'praTama', 'bahu') == {u'10.0277': [
            u'BAvayante'], u'10.0382': [u'BAvayante'], u'01.0001': [u'Bavanti']})
        assert(gen.getforms('BU', 'law', 'maDyama', 'eka') == {u'10.0277': [
            u'BAvayase'], u'10.0382': [u'BAvayase'], u'01.0001': [u'Bavasi']})
        assert(gen.getforms('BU', 'law', 'maDyama', 'dvi') == {u'10.0277': [
            u'BAvayeTe'], u'10.0382': [u'BAvayeTe'], u'01.0001': [u'BavaTaH']})
        assert(gen.getforms('BU', 'law', 'maDyama', 'bahu') == {u'10.0277': [
            u'BAvayaDve'], u'10.0382': [u'BAvayaDve'], u'01.0001': [u'BavaTa']})
        assert(gen.getforms('BU', 'law', 'uttama', 'eka') == {u'10.0277': [
            u'BAvaye'], u'10.0382': [u'BAvaye'], u'01.0001': [u'BavAmi']})
        assert(gen.getforms('BU', 'law', 'uttama', 'dvi') == {u'10.0277': [
            u'BAvayAvahe'], u'10.0382': [u'BAvayAvahe'], u'01.0001': [u'BavAvaH']})
        assert(gen.getforms('BU', 'law', 'uttama', 'bahu') == {u'10.0277': [
            u'BAvayAmahe'], u'10.0382': [u'BAvayAmahe'], u'01.0001': [u'BavAmaH']})
        assert(gen.getforms('BU', 'low', suffix='tip') == {u'10.0277': [u'BAvayatu', u'BAvayatAt'], u'10.0382': [
            u'BAvayatu', u'BAvayatAt'], u'01.0001': [u'Bavatu', u'BavatAt']})
        assert(gen.getforms('BU', 'low', suffix='tas') == {u'10.0277': [
            u'BAvayatAm'], u'10.0382': [u'BAvayatAm'], u'01.0001': [u'BavatAm']})
        assert(gen.getforms('BU', 'low', suffix='Ji') == {u'10.0277': [
            u'BAvayantu'], u'10.0382': [u'BAvayantu'], u'01.0001': [u'Bavantu']})
        assert(gen.getforms('BU', 'low', suffix='sip') == {u'10.0277': [u'BAvaya', u'BAvayatAt'], u'10.0382': [
            u'BAvaya', u'BAvayatAt'], u'01.0001': [u'Bava', u'BavatAt']})
        assert(gen.getforms('BU', 'low', suffix='Tas') == {u'10.0277': [
            u'BAvayatam'], u'10.0382': [u'BAvayatam'], u'01.0001': [u'Bavatam']})
        assert(gen.getforms('BU', 'low', suffix='Ta') == {u'10.0277': [
            u'BAvayata'], u'10.0382': [u'BAvayata'], u'01.0001': [u'Bavata']})
        assert(gen.getforms('BU', 'low', suffix='mip') == {u'10.0277': [
            u'BAvayAni'], u'10.0382': [u'BAvayAni'], u'01.0001': [u'BavAni']})
        assert(gen.getforms('BU', 'low', suffix='vas') == {u'10.0277': [
            u'BAvayAva'], u'10.0382': [u'BAvayAva'], u'01.0001': [u'BavAva']})
        assert(gen.getforms('BU', 'low', suffix='mas') == {u'10.0277': [
            u'BAvayAma'], u'10.0382': [u'BAvayAma'], u'01.0001': [u'BavAma']})
        # Test for stripped verbs.
        assert(gen.getforms('eD', 'lfw', suffix='Ja')
               == {u'01.0002': [u'eDizyante']})

    def test_generate_without_suffix(self):
        """Test without suffix."""
        gen = VerbFormGenerator()
        assert '01.0002' in gen['eD', 'law']
        assert '01.0001' in gen['BU', 'low']
        assert '01.0001' in gen['BU']
        assert '01.0002' in gen.getforms('eD', suffix='law')
        assert '01.0001' in gen.getforms('BU', suffix='low')
        assert '01.0001' in gen.getforms('BU')

    def test_generate_translit(self):
        """Test with HK as input and itrans as output."""
        gen = VerbFormGenerator()
        gen.input_translit('hk')
        gen.output_translit('itrans')
        assert(gen['bhU', 'laT', 'jhi'] == {u'01.0001': [u'bhavanti'], u'10.0382': [
            u'bhAvayanti'], u'10.0277': [u'bhAvayanti']})
        assert(gen.getforms('bhU', 'laT', suffix='jhi') == {u'01.0001': [
            u'bhavanti'], u'10.0382': [u'bhAvayanti'], u'10.0277': [u'bhAvayanti']})

    def test_false_in(self):
        """Test for false input transliteration."""
        gen = VerbFormGenerator()
        with self.assertRaises(SystemExit):
            gen.input_translit('asdfasdf')

    def test_false_out(self):
        """Test for false output transliteration."""
        gen = VerbFormGenerator()
        with self.assertRaises(SystemExit):
            gen.output_translit('fdasfdas')

    def test_wrong_verb(self):
        """Test for verb absent in database."""
        gen = VerbFormGenerator()
        with self.assertRaises(SystemExit):
            # gen['adsfasdf', 'tip']
            gen.getforms('adsfasdf', suffix='tip')
