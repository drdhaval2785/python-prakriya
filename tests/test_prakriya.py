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


def compareresult(verbform, arguments=''):
    """Compare the calculated and prestored results."""
    p = Prakriya()
    calculated = p[verbform, arguments]
    wholedata = readJson(os.path.join('tests', 'testdata', verbform + '.json'))
    if arguments == '':
        assert(calculated == wholedata)
    else:
        assert(calculated == wholedata[arguments])


class TestPrakriya(unittest.TestCase):
    """Tests for `prakriya` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
        compareresult('Bavati')
        compareresult('Bavati', 'prakriya')
        compareresult('Bavati', 'verb')
        compareresult('Bavati', 'verbaccent')
        compareresult('Bavati', 'lakara')
        compareresult('Bavati', 'gana')
        compareresult('Bavati', 'meaning')
        compareresult('Bavati', 'number')
        compareresult('Bavati', 'madhaviya')
        compareresult('Bavati', 'kshiratarangini')
        compareresult('Bavati', 'dhatupradipa')
        compareresult('Bavati', 'jnu')
        compareresult('Bavati', 'uohyd')
        compareresult('Bavati', 'upasarga')
        compareresult('Bavati', 'padadecider_id')
        compareresult('Bavati', 'padadecider_sutra')
        compareresult('Bavati', 'it_id')
        compareresult('Bavati', 'it_status')
        compareresult('Bavati', 'it_sutra')
        compareresult('Bavati', 'purusha')
        compareresult('Bavati', 'vachana')

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main, ['Bavati', 'prakriya'])
        assert(result.exit_code == 0)
        assert('BUvAdayo DAtavaH' in result.output)
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
