#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prakriya` package."""


import unittest
from click.testing import CliRunner
from prakriya import Prakriya
from prakriya import cli


class TestPrakriya(unittest.TestCase):
    """Tests for `prakriya` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.bhavati = [[{'sutra': u'BUvAdayo DAtavaH', 'sutra_num': u'1.3.1', 'form': u'BU'}, {'sutra': u'laH karmaRi ca BAve cAkarmakeByaH.', 'sutra_num': u'3.4.69', 'form': u'BU'}, {'sutra': u'vartamAne law', 'sutra_num': u'3.2.123', 'form': u'BU+la~w'}, {'sutra': u'lasya', 'sutra_num': u'3.4.77', 'form': u'BU+la~w'}, {'sutra': u'halantyam', 'sutra_num': u'1.3.3', 'form': u'BU+la~w'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+la~'}, {'sutra': u"upadeSe'janunAsika it", 'sutra_num': u'1.3.2', 'form': u'BU+la~'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+l'}, {'sutra': u'tiptasJisipTasTamibvasmas tAtAMJaTAsATAMDvamiqvahimahiN', 'sutra_num': u'3.4.78', 'form': u'BU+tip'}, {'sutra': u'laH parasmEpadam', 'sutra_num': u'1.4.99', 'form': u'BU+tip'}, {'sutra': u'tiNastrIRi trIRi praTamamaDyamottamAH', 'sutra_num': u'1.4.101', 'form': u'BU+tip'}, {'sutra': u'tAnyekavacanadvivacanabahuvacanAnyekaSaH', 'sutra_num': u'1.4.102', 'form': u'BU+tip'}, {'sutra': u'Seze praTamaH', 'sutra_num': u'1.4.108', 'form': u'BU+tip'}, {'sutra': u'tiNSitsArvaDAtukam', 'sutra_num': u'3.4.113', 'form': u'BU+tip'}, {'sutra': u'kartari Sap\u200c', 'sutra_num': u'3.1.68', 'form': u'BU+Sap+tip'}, {'sutra': u'tiNSitsArvaDAtukam', 'sutra_num': u'3.4.113', 'form': u'BU+Sap+tip'}, {'sutra': u'laSakvatadDite', 'sutra_num': u'1.3.8', 'form': u'BU+Sap+tip'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+ap+tip'}, {'sutra': u'halantyam', 'sutra_num': u'1.3.3', 'form': u'BU+ap+tip'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+a+ti'}, {'sutra': u'sArvaDAtukArDaDAtukayoH', 'sutra_num': u'7.3.84', 'form': u'Bo+a+ti'}, {'sutra': u"eco'yavAyAvaH", 'sutra_num': u'6.1.78', 'form': u'Bav+a+ti'}, {'sutra': u'antimaM rUpam', 'sutra_num': u'-2', 'form': u'Bavati'}]]
    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
        p = Prakriya()
        output = p['Bavati', 'prakriya']
        assert(output == self.bhavati)

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main, ['Bavati', 'prakriya'])
        assert(result.exit_code == 0)
        assert('BUvAdayo DAtavaH' in result.output)
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
