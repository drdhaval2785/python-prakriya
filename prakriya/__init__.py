# -*- coding: utf-8 -*-

"""Top-level package for prakriya."""

__author__ = """Dr. Dhaval Patel"""
__email__ = 'drdhaval2785@gmail.com'
__version__ = '0.2.1'
__all__ = ['Prakriya', 'VerbFormGenerator', 'main', 'generate']


from .verbforms import Prakriya
from .generate import VerbFormGenerator
from .cli import main
from .cli import generate
