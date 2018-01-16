=======
History
=======

0.0.1 (2017-12-30)
------------------

* First release on PyPI.

0.0.2 (2018-01-01)
------------------

Broken release. Kindly update to v0.0.3 immediately.

0.0.3 (2018-01-02)
------------------

A fix for broken v0.0.2 release.
jsonindex.json file which was crucial and missed in v0.0.2, added back.

0.0.4 (2018-01-03)
------------------

1. Added transliteration support. See #5 .
2. Adding data file in system specific locations like APPDATA. See #6 .
3. Made code python 2.7, 3.3, 3.4, 3.5, 3.6 compliant.
4. Corrected all errors / smells identified by landscape.io.

0.0.5 (2018-01-13)
------------------

1. Added verb form generation facility. See https://github.com/drdhaval2785/prakriya/issues/39.

0.0.6 (2018-10-16)
------------------

1. Added CLI functionality 'generate'. See https://github.com/drdhaval2785/python-prakriya/issues/12.
2. Guess the correct verb e.g. eD -> eDa~. See https://github.com/drdhaval2785/python-prakriya/issues/13.
3. All data files moved to appdata folder. See https://github.com/drdhaval2785/python-prakriya/issues/14.
4. Memoize data read from JSONs for speedup. See https://github.com/drdhaval2785/python-prakriya/issues/15.
5. Removed unnecessary duplicate loading of JSONs. See https://github.com/drdhaval2785/python-prakriya/issues/11.
