#!/usr/bin/env python3
#
# Copyright 2020 by Philip N. Garner
#
# See the file COPYING for the licence associated with this software.
#
# Author(s):
#   Phil Garner, October 2020
#

# Oracle: https://bescherelle.com/conjugueur.php

# Prepend a string onto each element of an array
def prepend(pre, arr):
    def concat(a):
        return pre + a
    return list(map(concat, arr))

# Base class for all verbs
class Verb:
    # All verbs have an infinitive
    verb = ''

    # List of 'verb' forms of verbs with auxiliary être.
    auxEtre = [
        'venir',   'aller',    # Come, go
        'entrer',  'sortir',   # Enter, go out
        'arriver', 'partir',   # Arrive, leave
        'monter',  'decendre', # Climb, descend
        'naître',  'mourir',   # Be born, die
        'rester',  'passer',   # Stay, pass
        'tomber',  'retourner' # Fall, return
    ]

    def __init__(self, verb):
        self.verb = verb # The infinitive

    # The auxiliary for the perfect &c
    def aux(self):
        if self.verb in self.auxEtre:
            return 'être'
        return 'avoir'


# The regular conjugations, based on either the stem or the verb itself
class Regular(Verb):
    # Regular verbs have a stem, and a longer stem for the conditional
    stem = ''
    cond = ''

    # Indicative present
    preS = ['e', 'es', 'e']
    preP = ['ons', 'ez', 'ent']

    # Indicative imperfect
    impS = ['ais', 'ais', 'ait']
    impP = ['ions', 'iez', 'aient']

    # Indicative simple past
    pasS = ['ai', 'as', 'a']
    pasP = ['âmes', 'âtes', 'èrent']

    # Indicative simple future
    futS = pasS
    futP = ['ons', 'ez', 'ont']

    # Subjunctive present
    subPreS = preS
    subPreP = ['ions', 'iez', 'ent']

    # Subjunctive imperfect
    subImpS = ['asse', 'asses', 'ât']
    subImpP = ['assions', 'assiez', 'assent']

    # Participles
    parPre = ['ant']
    parPas = ['é']

    def __init__(self, verb):
        super().__init__(verb)
        self.stem = verb[:-2] # The stem, for most tenses
        self.cond = verb      # The longer stem, for future and conditional

    def sconj(self, suff):
        return prepend(self.stem, suff)

    def cconj(self, suff):
        return prepend(self.cond, suff)

    def indPresentS(self):
        return self.sconj(self.preS)

    def indPresentP(self):
        return self.sconj(self.preP)

    def indPresent(self):
        return self.indPresentS() + self.indPresentP()

    def indImperfect(self):
        return self.sconj(self.impS + self.impP)

    def indSimplePast(self):
        return self.sconj(self.pasS + self.pasP)

    def indSimpleFuture(self):
        return self.cconj(self.futS + self.futP)

    def conditional(self):
        # As indicative imperfect, but with the longer stem
        return self.cconj(self.impS + self.impP)

    def subPresent(self):
        return self.sconj(self.subPreS + self.subPreP)

    def subImperfect(self):
        return self.sconj(self.subImpS + self.subImpP)

    def partPresent(self):
        return self.sconj(self.parPre)

    def partPast(self):
        return self.sconj(self.parPas)

    def participles(self):
        return self.partPresent() + self.partPast()


# A regular base where the Indicative simple Past and Subjunctive Imperfect
# change conjugation with a leading i-
# This is the case for group 2 and many group 3 verbs
# Also set the past participle to i since it seems to work for several verbs
# (group 2, sortir, partir)
class BaseIPSI(Regular):
    pasS = ['is', 'is', 'it']
    pasP = ['îmes', 'îtes', 'irent']
    subImpS = ['isse', 'isses', 'ît']
    subImpP = ['issions', 'issiez', 'issent']
    parPas = ['i']


# Another regular base similar to BaseIPSI, but based on a leading u-
# Again, the past participle is also set to u
class BaseUPSI(Regular):
    pasS = ['us', 'us', 'ut']
    pasP = ['ûmes', 'ûtes', 'urent']
    subImpS = ['usse', 'usses', 'ût']
    subImpP = ['ussions', 'ussiez', 'ussent']
    parPas = ['u']


# The regular group 2, ending in -ir, e.g., finir
# Characterised by lots of -iss- in the conjugations
class RegularIR(BaseIPSI):
    preS = ['is', 'is', 'it']
    preP = ['issons', 'issez', 'issent']
    parPre = ['issant']

    def indImperfect(self):
        return Regular(self.stem+'isser').indImperfect()

    def subPresent(self):
        return Regular(self.stem+'isser').subPresent()


# A regular group 3 verb class ending in -re, e.g., repondre, descendre
class RegularRE(BaseIPSI):
    preS = ['s', 's', '']
    parPas = ['u']

    def __init__(self, verb):
        self.verb = verb
        self.stem = verb[:-2]
        self.cond = verb[:-1]


class Être(Regular):
    def __init__(self):
        self.stem = 'ét'
        self.cond = 'ser'

    def indPresent(self):
        return ['suis', 'es', 'est', 'sommes', 'êtes', 'sont']

    def indSimplePast(self):
        return BaseUPSI('fer').indSimplePast()

    def subPresent(self):
        return ['sois', 'sois', 'soit', 'soyons', 'soyez', 'soient']

    def subImperfect(self):
        return BaseUPSI('fer').subImperfect()


class Avoir(Regular):
    def __init__(self):
        self.stem = 'av'
        self.cond = 'aur'

    def indPresent(self):
        return ['ai', 'as', 'a', 'avons', 'avez', 'ont']

    def indSimplePast(self):
        return BaseUPSI('eer').indSimplePast()

    def subPresent(self):
        return ['aie', 'aies', 'ait', 'ayons', 'ayez', 'aient']

    def subImperfect(self):
        return BaseUPSI('eer').subImperfect()

    def partPresent(self):
        return ['ayant']

    def partPast(self):
        return ['eu']


class Faire(Regular):
    def __init__(self):
        self.stem = 'fais'
        self.cond = 'fer'

    def indPresent(self):
        return ['fais', 'fais', 'fait', 'faisons', 'faites', 'font']

    def indSimplePast(self):
        return ['fis', 'fis', 'fit', 'fimes', 'fites', 'firent']

    def partPast(self):
        return ['fait']


class Voir(Regular):
    def __init__(self):
        self.stem = 'voy'
        self.cond = 'verr'

    def indPresent(self):
        return ['vois', 'vois', 'voit', 'voyons', 'voyez', 'voient']

    def indSimplePast(self):
        return ['vis', 'vis', 'vit', 'vîmes', 'vîtes', 'virent']

    def subPresent(self):
        return ['voie', 'voies', 'voie', 'voyions', 'voyiez', 'voient']

    def subImperfect(self):
        return ['visse', 'visses', 'vît', 'vissions', 'vissiez', 'vissent']

    def partPast(self):
        return ['vu']


class Pouvoir(Regular):
    def __init__(self):
        self.stem = 'pouv'
        self.cond = 'pourr'

    def indPresent(self):
        return ['peux', 'peux', 'peut', 'pouvons', 'pouvez', 'peuvent']

    def indSimplePast(self):
        return BaseUPSI('per').indSimplePast()

    def subPresent(self):
        return ['puisse', 'puisses', 'puisse',
                'puissions', 'puissiez', 'puissent']

    def subImperfect(self):
        return BaseUPSI('per').subImperfect()

    def partPast(self):
        return ['pu']


class Vouloir(BaseUPSI):
    def __init__(self):
        self.stem = 'voul'
        self.cond = 'voudr'

    def indPresent(self):
        return ['veux', 'veux', 'veut', 'voulons', 'voulez', 'veulent']

    def subPresent(self):
        return ['veuille', 'veuilles', 'veuille',
                'voulions', 'vouliez', 'veuillent']


class Savoir(Regular):
    def __init__(self):
        self.stem = 'sav'
        self.cond = 'saur'

    def indPresentS(self):
        return ['sais', 'sais', 'sait']

    def indSimplePast(self):
        return BaseUPSI('ser').indSimplePast()

    def subPresent(self):
        return Regular('sacher').subPresent()

    def subImperfect(self):
        return BaseUPSI('ser').subImperfect()

    def partPresent(self):
        return ['sachant']

    def partPast(self):
        return ['su']


class Aller(Regular):
    def __init__(self):
        super().__init__('aller')
        self.cond = 'ir'

    def indPresent(self):
        return ['vais', 'vas', 'va', 'allons', 'allez', 'vont']

    def subPresent(self):
        return ['aille', 'ailles', 'aille', 'allions', 'alliez', 'aillent']


class Sortir(BaseIPSI):
    def __init__(self):
        super().__init__('sortir')

    def indPresentS(self):
        return ['sors', 'sors', 'sort']


class Partir(BaseIPSI):
    def __init__(self):
        super().__init__('partir')

    def indPresentS(self):
        return ['pars', 'pars', 'part']


class Naître(BaseIPSI):
    def __init__(self):
        self.stem = 'naiss'
        self.cond = 'naîtr'

    def indPresentS(self):
        return ['nais', 'nais', 'naît']

    def indSimplePast(self):
        return BaseIPSI('naquer').indSimplePast()

    def subImperfect(self):
        return BaseIPSI('naquer').subImperfect()

    def partPast(self):
        return ['né']


class Mourir(BaseUPSI):
    def __init__(self):
        self.verb = 'mourir'
        self.stem = 'mour'
        self.cond = 'mourr'

    def indPresentS(self):
        return ['meurs', 'meurs', 'meurt']

    def subPresent(self):
        return ['meure', 'meures', 'meure',
                'mourions', 'mouriez', 'meurent']

    def partPast(self):
        return ['mort']


class Venir(Regular):
    def __init__(self):
        self.verb = 'venir'
        self.stem = 'ven'
        self.cond = 'viendr'

    def indPresent(self):
        return ['viens', 'viens', 'vient', 'venons', 'venez', 'viennent']

    def indSimplePast(self):
        return ['vins', 'vins', 'vint', 'vînmes', 'vîntes', 'vinrent']

    def subPresent(self):
        return ['vienne', 'viennes', 'vienne',
                'venions', 'veniez', 'viennent']

    def subImperfect(self):
        return ['vinsse', 'vinsses', 'vînt',
                'vinssions', 'vinssiez', 'vinssent']

    def partPast(self):
       return ['venu']


class Conduire(BaseIPSI):
    def __init__(self):
        self.stem = 'conduis'
        self.cond = 'conduir'

    def indPresentS(self):
        return ['conduis', 'conduis', 'conduit']

    def partPast(self):
        return ['conduit']


def split_stem(verb):
    stem = verb[:-2]
    suff = verb[-2:]
    return [stem, suff]

def toClass(verb):
    # First check if the (irregular) verb exists as an explicit class
    cverb = verb.capitalize()
    if cverb in globals():
        return globals()[cverb]()

    # Otherwise, try a (regular) solution via the suffix
    [stem, suff] = split_stem(verb)
    if suff == 'er':
        return Regular(verb)
    elif suff == 'ir':
        return RegularIR(verb)
    elif suff == 're':
        return RegularRE(verb)
    print('Unknown suffix: %s (%s)' % (verb, suff))
    exit()

def format2(conj):
    print('     je {0:22}tu {1:22}elle {2}'.format(
        conj[0], conj[1], conj[2]))
    print('     nous {0:20}vous {1:20}elles {2}'.format(
        conj[3], conj[4], conj[5]))


def conjSimple(verb):
    v = toClass(verb)
    print(verb.capitalize())
    print('     en {0:22}on {1} {2}'.format(
        v.partPresent()[0], toClass(v.aux()).indPresent()[2], v.partPast()[0]))
    print('Ind. Present'); format2(v.indPresent())
    print('Ind. Imperfect'); format2(v.indImperfect())
    print('Ind. Simple Past'); format2(v.indSimplePast())
    print('Ind. Simple Future'); format2(v.indSimpleFuture())
    print('Conditional'); format2(v.conditional())
    print('Sub. Present'); format2(v.subPresent())
    print('Sub. Imperfect'); format2(v.subImperfect())


# Tests
import unittest
import filecmp
import sys
class TestSimple(unittest.TestCase):
    verbs = ['rester', 'passer', 'finir', 'descendre',
             'être', 'avoir', 'faire', 'voir', 'pouvoir', 'vouloir',
             'savoir', 'aller', 'sortir', 'partir', 'naître', 'mourir',
             'venir', 'conduire']
    def testSimple(self):
        out = 'testSimple-out.txt'
        ref = 'testSimple-ref.txt'
        with open(out, 'w') as f:
            sys.stdout = f
            for verb in self.verbs:
                conjSimple(verb)
        self.assertTrue(filecmp.cmp(out, ref))


# This is the main program
import argparse
ap = argparse.ArgumentParser("conjugate")
ap.add_argument('verb', type=str, nargs='*', help='verbs to conjugate')
ap.add_argument('-t',   action='store_true', help='run the tests')
arg = ap.parse_args()

for verb in arg.verb:
    conjSimple(verb)

if arg.t:
    suite  = unittest.TestLoader().loadTestsFromTestCase(TestSimple)
    runner = unittest.TextTestRunner()
    runner.run(suite)
