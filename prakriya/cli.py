# -*- coding: utf-8 -*-

"""Console script for prakriya."""

import click


@click.command()
@click.argument('verbform')
@click.argument('field', required=False, default='')
def main(verbform, field):
    """Console script for prakriya.

    Usage
    -----
    prakriya [verbform] [field]

    Valid values of field and expected output are as follows.

    "prakriya" - Return step by step derivation.

    "verb" - Return verb in Devanagari without accent marks.

    "verbaccent" - Return the verb in Devanagari with accent marks.

    "lakara" - Return the lakAra (tense / mood) in which this form is generated.

    "gana" - Return the gaNa (class) of the verb.

    "meaning" - Return meaning of the verb in SLP1 transliteration.

    "number" - Return number of the verb in dhAtupATha.

    "madhaviya" - Return link to mAdhaviyadhAtuvRtti. http://sanskrit.uohyd.ac.in/scl/dhaatupaatha is the home page.

    "kshiratarangini" - Return link to kSIrataraGgiNI. http://sanskrit.uohyd.ac.in/scl/dhaatupaatha is the home page.

    "dhatupradipa" - Return link to dhAtupradIpa. http://sanskrit.uohyd.ac.in/scl/dhaatupaatha is the home page.

    "jnu" - Return link to JNU site for this verb form. http://sanskrit.jnu.ac.in/tinanta/tinanta.jsp is the home page.

    "uohyd" - Return link to UoHyd site for this verb form. http://sanskrit.uohyd.ac.in/cgi-bin/scl/skt_gen/verb/verb_gen.cgi is the home page.

    "upasarga" - Return upasarga, if any. Currently we do not support verb forms with upasargas.

    "padadecider_id" - Return the rule number which decides whether the verb is parasmaipadI, AtmanepadI or ubhayapadI.

    "padadecider_sutra" - Return the rule text which decides whether the verb is parasmaipadI, AtmanepadI or ubhayapadI.

    "it_id" - Returns whether the verb is seT, aniT or veT, provided the form has iDAgama.

    "it_status" - Returns whether the verb form has iDAgama or not. seT, veT, aniT are the output.

    "it_sutra" - Returns rule number if iDAgama is caused by some special rule.

    """
    from prakriya import Prakriya
    p = Prakriya()
    result = p[verbform, field]
    click.echo(result)


if __name__ == "__main__":
    main()
