#!/usr/bin/env python3
#
# Copyright 2020 by Philip N. Garner
#
# See the file COPYING for the licence associated with this software.
#
# Author(s):
#   Phil Garner, October 2020
#

class Verb:
    aux = 'avoir'    # The auxiliary for the perfect &c

    def __init__(self, stem, verb=None):
        self.stem = stem # The stem, for most tenses
        self.verb = verb # The longer stem, for future and conditional

    def sconj(self, suff):
        def concat(a):
            return self.stem+a
        return list(map(concat, suff))

    def vconj(self, suff):
        def concat(a):
            return self.verb+a
        return list(map(concat, suff))


# The regular conjugations, based on either the stem or the verb itself
class Regular(Verb):
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

    def indPresent(self):
        return self.sconj(self.preS + self.preP)

    def indImperfect(self):
        return self.sconj(self.impS + self.impP)

    def indSimplePast(self):
        return self.sconj(self.pasS + self.pasP)

    def indSimpleFuture(self):
        return self.vconj(self.futS + self.futP)

    def conditional(self):
        # As indicative imperfect, but with the longer stem
        return self.vconj(self.impS + self.impP)

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


# E.g., repondre
class RegularRE(Regular):
    preS = ['s', 's', '']
    pasS = ['is', 'is', 'it']
    pasP = ['îmes', 'îtes', 'irent']
    subImpS = ['isse', 'isses', 'ît']
    subImpP = ['issions', 'issiez', 'issent']
    parPas = ['u']


# E.g., finir
class RegularIR(RegularRE):
    preS = ['is', 'is', 'it']
    preP = ['issons', 'issez', 'issent']
    parPre = ['issant']
    parPas = ['i']

    def indImperfect(self):
        v = Regular(self.stem+'iss')
        return v.indImperfect()

    def subPresent(self):
        v = Regular(self.stem+'iss')
        return v.subPresent()


class Conduire(RegularRE):
    def __init__(self):
        self.stem = 'conduis'
        self.verb = 'conduir'

    def indPresent(self):
        return ['conduis', 'conduis', 'conduit', 'conduisons', 'conduisez', 'conduisent']

    def partPast(self):
        return ['conduit']


class Être(Regular):
    def __init__(self):
        self.stem = 'ét'
        self.verb = 'ser'

    def indPresent(self):
        return ['suis', 'es', 'est', 'sommes', 'êtes', 'sont']

    def indSimplePast(self):
        return ['fus', 'fus', 'fut', 'fûmes', 'fûtes', 'furent']

    def subPresent(self):
        return ['sois', 'sois', 'soit', 'soyons', 'soyez', 'soient']

    def subImperfect(self):
        return ['fusse', 'fusses', 'fût', 'fussions', 'fussiez', 'fussent']


class Avoir(Regular):
    def __init__(self):
        self.stem = 'av'
        self.verb = 'aur'

    def indPresent(self):
        return ['ai', 'as', 'a', 'avons', 'avez', 'ont']

    def indSimplePast(self):
        return ['eus', 'eus', 'eut', 'eûmes', 'eûtes', 'eurent']

    def subPresent(self):
        return ['aie', 'aies', 'ait', 'ayons', 'ayez', 'aient']

    def subImperfect(self):
        return ['eusse', 'eusses', 'eût', 'eussions', 'eussiez', 'eussent']

    def partPresent(self):
        return ['ayant']

    def partPast(self):
        return ['eu']


class Faire(Regular):
    def __init__(self):
        self.stem = 'fais'
        self.verb = 'fer'

    def indPresent(self):
        return ['fais', 'fais', 'fait', 'faisons', 'faites', 'font']

    def indSimplePast(self):
        return ['fis', 'fis', 'fit', 'fimes', 'fites', 'firent']

    def partPast(self):
        return ['fait']


class Voir(Regular):
    def __init__(self):
        self.stem = 'voy'
        self.verb = 'verr'

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
        self.verb = 'pourr'

    def indPresent(self):
        return ['peux', 'peux', 'peut', 'pouvons', 'pouvez', 'peuvent']

    def indSimplePast(self):
        return ['pus', 'pus', 'put', 'pûmes', 'pûtes', 'purent']

    def subPresent(self):
        return ['puisse', 'puisses', 'puisse', 'puissions', 'puissiez', 'puissent']

    def subImperfect(self):
        return ['pusse', 'pusses', 'pût', 'pussions', 'pussiez', 'pussent']

    def partPast(self):
        return ['pu']


class Savoir(Regular):
    def __init__(self):
        self.stem = 'sav'
        self.verb = 'saur'

    def indPresent(self):
        return ['sais', 'sais', 'sait', 'savons', 'savez', 'savent']

    def indSimplePast(self):
        return ['sus', 'sus', 'sut', 'sûmes', 'sûtes', 'surent']

    def subPresent(self):
        v = Regular('sach')
        return v.subPresent()

    def subImperfect(self):
        return ['susse', 'susses', 'sût', 'sussions', 'sussiez', 'sussent']

    def partPresent(self):
        return ['sachant']

    def partPast(self):
        return ['su']


class Venir(Regular):
    aux = 'être'

    def __init__(self):
        self.stem = 'ven'
        self.verb = 'viendr'

    def indPresent(self):
        return ['viens', 'viens', 'vient', 'venons', 'venez', 'viennent']

    def indSimplePast(self):
        return ['vins', 'vins', 'vint', 'vînmes', 'vîntes', 'vinrent']

    def subPresent(self):
        v = Regular('sach')
        return v.subPresent()

    def subPresent(self):
        return ['vienne', 'viennes', 'vienne', 'venions', 'veniez', 'viennent']

    def subImperfect(self):
        return ['vinsse', 'vinsses', 'vînt', 'vinssions', 'vinssiez', 'vinssent']

    def partPast(self):
       return ['venu']


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
        return Regular(stem, verb)
    elif suff == 'ir':
        return RegularIR(stem, verb)
    elif suff == 're':
        return RegularRE(stem, stem+'r')
    print('Unknown suffix: %s (%s)' % (verb, suff))
    exit()

def format2(conj):
    print('     je {0:22}tu {1:22}elle {2}'.format(
        conj[0], conj[1], conj[2]))
    print('     nous {0:20}vous {1:20}elles {2}'.format(
        conj[3], conj[4], conj[5]))

# This is the main program
import argparse
ap = argparse.ArgumentParser("conjugate")
ap.add_argument('verbs', metavar='VERB', type=str, nargs='+',
                help='verbs to conjugate')
arg = ap.parse_args()

for verb in arg.verbs:
    v = toClass(verb)
    print(verb.capitalize())
    print('     en {0:22}on {1} {2}'.format(
        v.partPresent()[0], toClass(v.aux).indPresent()[2], v.partPast()[0]))
    print('Ind. Present'); format2(v.indPresent())
    print('Ind. Imperfect'); format2(v.indImperfect())
    print('Ind. Simple Past'); format2(v.indSimplePast())
    print('Ind. Simple Future'); format2(v.indSimpleFuture())
    print('Conditional'); format2(v.conditional())
    print('Sub. Present'); format2(v.subPresent())
    print('Sub. Imperfect'); format2(v.subImperfect())

# All done; just drop out
#print("Args:", arg)
