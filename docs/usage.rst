=====
Usage
=====

prakriya
--------

To use prakriya in a project::

    >>> from prakriya import Prakriya
    >>> p = Prakriya()

If you are using the library the first time, be patient.
This will take a long time, because the data file (30 MB) is being downloaded.

If you can spare around 600 MB space, It is highly recommended to decompress the tar.gz first time.
Subsequent actions will be very fast. This is one time requirement.
If the data is not decompressed, the code will read from tar.gz file every time.
It introduces slowness to a great extent. So highly recommended to decompress.

    >>> p.decompress()

Now you are ready to roll!

The generic format for usage is as follows:

    >>> p[verbform, field]

``verbform`` is mandatory. It is the verb form to be investigated.
The input should be in SLP1 encoding.

``field`` is optional.

Actual usage examples will be like the following.

    >>> p['Bavati']
    >>> p['Bavati', 'prakriya']
    >>> p['Bavati', 'verb']


Valid values of ``field`` and expected output are as follows.

    ``prakriya`` - Return step by step derivation.

    ``verb`` - Return verb in Devanagari without accent marks.

    ``verbaccent`` - Return the verb in Devanagari with accent marks.

    ``lakara`` - Return the lakAra (tense / mood) in which this form is generated.

    ``gana`` - Return the gaNa (class) of the verb.

    ``meaning`` - Return meaning of the verb in SLP1 transliteration.

    ``number`` - Return number of the verb in dhAtupATha.

    ``madhaviya`` - Return link to mAdhaviyadhAtuvRtti. http://sanskrit.uohyd.ac.in/scl/dhaatupaatha is the home page.

    ``kshiratarangini`` - Return link to kSIrataraGgiNI. http://sanskrit.uohyd.ac.in/scl/dhaatupaatha is the home page.

    ``dhatupradipa`` - Return link to dhAtupradIpa. http://sanskrit.uohyd.ac.in/scl/dhaatupaatha is the home page.

    ``jnu`` - Return link to JNU site for this verb form. http://sanskrit.jnu.ac.in/tinanta/tinanta.jsp is the home page.

    ``uohyd`` - Return link to UoHyd site for this verb form. http://sanskrit.uohyd.ac.in/cgi-bin/scl/skt_gen/verb/verb_gen.cgi is the home page.

    ``upasarga`` - Return upasarga, if any. Currently we do not support verb forms with upasargas.

    ``padadecider_id`` - Return the rule number which decides whether the verb is parasmaipadI, AtmanepadI or ubhayapadI.

    ``padadecider_sutra`` - Return the rule text which decides whether the verb is parasmaipadI, AtmanepadI or ubhayapadI.

    ``it_id`` - Returns whether the verb is seT, aniT or veT, provided the form has iDAgama.

    ``it_status`` - Returns whether the verb form has iDAgama or not. seT, veT, aniT are the output.

    ``it_sutra`` - Returns rule number if iDAgama is caused by some special rule.

    ``purusha`` - Returns the purusha of the given verb form.

    ``vachana`` - Returns the vacana of the given verb form.

Generate verb forms
-------------------

To get verb form for given verb, tense, suffix / (purusha and vachana) in a project::

    >>> from prakriya import Generate
    >>> g = Generate()

There are two ways to get verb forms for given verb.

    >>> g[verb, tense, purusha, vachana]

    >>> g[verb, tense, suffix]

Examples are as follows

  >>> g['BU', 'law', 'praTama', 'eka']

  >>> g['BU', 'law', 'tip']


Transliteration
---------------

If you want to set the input or output transliteration, follow these steps.

>>> from prakriya import Prakriya
>>> p = Prakriya()
>>> p.inputTranslit('hk') # Customize 'hk'
>>> p.outputTranslit('devanagari') # Customize 'devanagari'
>>> p['bhavati'] # Takes the input in hk Transliteration
# Gives output in Devangari.
>>> p.inputTranslit('devanagari')
>>> p.outputTranslit('iast')
>>> p['गच्छति']

Valid transliterations are slp1, itrans, hk, iast, devanagari, wx, bengali,
gujarati, gurmukhi, kannada, malayalam, oriya and telugu.
They can be used both as input transliteration and output transliteration schemes.

For using transliterations in Generate class, use as below.

>>> from prakriya import Generate
>>> g = Generate()
>>> g.inputTranslit('hk') # Customize 'hk'
>>> g.outputTranslit('devanagari') # Customize 'devanagari'
>>> g['bhU', 'laT', 'jhi'] # Takes the input in hk Transliteration
