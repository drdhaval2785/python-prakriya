#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prakriya` package."""


import unittest
import json
import os.path
from click.testing import CliRunner
from prakriya import Prakriya
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
    # superdata = readJson(os.path.join('tests', 'testdata', verbform + '.json'))
    superdata = readJson(os.path.join('tests', 'testdata', 'Bavati.json'))
    wholedata = superdata[outTran]
    if arguments == '':
        assert(calculated == wholedata)
    else:
        result = [member[arguments] for member in wholedata]
        assert(calculated == result)


class TestPrakriya(unittest.TestCase):
    """Tests for `prakriya` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

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
        assert '--help  Show this message and exit.' in help_result.output
