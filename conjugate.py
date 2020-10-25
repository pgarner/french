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
    pre = ['e', 'es', 'e', 'ons', 'ez', 'ent']
    imp = ['ais', 'ais', 'ait', 'ions', 'iez', 'aient']
    pas = ['ai', 'as', 'a', 'âmes', 'âtes', 'èrent']
    fut = ['ai', 'as', 'a', 'ons', 'ez', 'ont']
    subPre = ['e', 'es', 'e', 'ions', 'iez', 'ent']
    subImp = ['asse', 'asses', 'ât', 'assions', 'assiez', 'assent']
    parPre = ['ant']
    parPas = ['é']

    def indPresent(self):
        return self.sconj(self.pre)

    def indImperfect(self):
        return self.sconj(self.imp)

    def indSimplePast(self):
        return self.sconj(self.pas)

    def indSimpleFuture(self):
        return self.vconj(self.fut)

    def conditional(self):
        # As indicative imperfect, but with the longer stem
        return self.vconj(self.imp)

    def subPresent(self):
        return self.sconj(self.subPre)

    def subImperfect(self):
        return self.sconj(self.subImp)

    def partPresent(self):
        return self.sconj(self.parPre)

    def partPast(self):
        return self.sconj(self.parPas)

    def participles(self):
        return self.partPresent() + self.partPast()


# E.g., repondre
class RegularRE(Regular):
    pre = ['s', 's', '', 'ons', 'ez', 'ent']
    pas = ['is', 'is', 'it', 'îmes', 'îtes', 'irent']
    subImp = ['isse', 'isses', 'ît', 'issions', 'issiez', 'issent']
    parPas = ['u']


# E.g., finir
class RegularIR(RegularRE):
    pre = ['is', 'is', 'it', 'issons', 'issez', 'issent']
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


class Etre(Regular):
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

    def partPast(self):
        return ['pu']


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

# This is the main program
import argparse
ap = argparse.ArgumentParser("conjugate")
ap.add_argument('verbs', metavar='VERB', type=str, nargs='+',
                help='verbs to conjugate')
arg = ap.parse_args()

for verb in arg.verbs:
    print(verb)
    v = toClass(verb)
    print('Ind. Present:       %s' % v.indPresent())
    print('Ind. Imperfect:     %s' % v.indImperfect())
    print('Ind. Simple past:   %s' % v.indSimplePast())
    print('Ind. Simple future: %s' % v.indSimpleFuture())
    print('Conditional:        %s' % v.conditional())
    print('Sub. Present:       %s' % v.subPresent())
    print('Sub. Imperfect:     %s' % v.subImperfect())
    print('Participles:        %s' % v.participles())

# All done; just drop out
#print("Args:", arg)
