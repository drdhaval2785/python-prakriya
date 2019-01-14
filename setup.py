#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'requests',
    'indic-transliteration'
]

setup_requirements = []

test_requirements = []

setup(
    name='prakriya',
    version='0.2.1',
    description="prakriya is a package to derive information about given Sanskrit verb form.",
    long_description=readme + '\n\n' + history,
    author="Dr. Dhaval Patel",
    author_email='drdhaval2785@gmail.com',
    url='https://github.com/drdhaval2785/python-prakriya',
    packages=find_packages(include=['prakriya'],
                           exclude=['docs', 'tests', 'scrap']),
    entry_points={
        'console_scripts': [
            'prakriya=prakriya.cli:main',
            'generate=prakriya.cli:generate'
        ]
    },
    include_package_data=True,
    package_data={
        'prakriya': ['data/sutrainfo.json']
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='prakriya,panini,Sanskrit,grammar,tinanta',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
