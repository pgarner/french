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
    imp = ['ais', 'ais', 'ait', 'ions', 'iez', 'aient']

    def present(self):
        return self.sconj(['e', 'es', 'e', 'ons', 'ez', 'ent'])

    def imperfect(self):
        return self.sconj(self.imp)

    def future(self):
        return self.vconj(['ai', 'as', 'a', 'ons', 'ez', 'ont'])

    def historic(self):
        return self.sconj(['ai', 'as', 'a', 'âmes', 'âtes', 'èrent'])

    def conditional(self):
        return self.vconj(self.imp) # As imperfect, but with the longer stem

    def participles(self):
        return self.sconj(['ant', 'é'])


# E.g., repondre
class RegularRE(Regular):
    def present(self):
        return self.sconj(['s', 's', '', 'ons', 'ez', 'ent'])

    def historic(self):
        return self.sconj(['is', 'is', 'it', 'îmes', 'îtes', 'irent'])

    def participles(self):
        return self.sconj(['ant', 'u'])


# E.g., finir
class RegularIR(RegularRE):
    def present(self):
        return self.sconj(['is', 'is', 'it', 'issons', 'issez', 'issent'])

    def imperfect(self):
        v = Regular(self.stem+'iss')
        return v.imperfect()

    def participles(self):
        return self.sconj(['issant', 'i'])


class Conduire(RegularRE):
    def __init__(self):
        self.stem = 'conduis'
        self.verb = 'conduir'

    def present(self):
        return ['conduis', 'conduis', 'conduit', 'conduisons', 'conduisez', 'conduisent']

    def participles(self):
        return ['conduisant', 'conduit']


class Etre(Regular):
    def __init__(self):
        self.stem = 'ét'
        self.verb = 'ser'

    def present(self):
        return ['suis', 'es', 'est', 'sommes', 'êtes', 'sont']

    def historic(self):
        return ['fus', 'fus', 'fut', 'fûmes', 'fûtes', 'furent']


class Avoir(Regular):
    def __init__(self):
        self.stem = 'av'
        self.verb = 'aur'

    def present(self):
        return ['ai', 'as', 'a', 'avons', 'avez', 'ont']

    def historic(self):
        return ['eus', 'eus', 'eut', 'eûmes', 'eûtes', 'eurent']

    def participles(self):
        return ['ayant', 'eu']


class Faire(Regular):
    def __init__(self):
        self.stem = 'fais'
        self.verb = 'fer'

    def present(self):
        return ['fais', 'fais', 'fait', 'faisons', 'faites', 'font']

    def historic(self):
        return ['fis', 'fis', 'fit', 'fimes', 'fites', 'firent']

    def participles(self):
        return ['faisant', 'fait']


class Voir(Regular):
    def __init__(self):
        self.stem = 'voy'
        self.verb = 'verr'

    def present(self):
        return ['vois', 'vois', 'voit', 'voyons', 'voyez', 'voient']

    def historic(self):
        return ['vis', 'vis', 'vit', 'vîmes', 'vîtes', 'virent']

    def participles(self):
        return ['voyant', 'vu']


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
    print('Present:     %s' % v.present())
    print('Imperfect:   %s' % v.imperfect())
    print('Future:      %s' % v.future())
    print('Historic:    %s' % v.historic())
    print('Conditional: %s' % v.conditional())
    print('Participles: %s' % v.participles())

# All done; just drop out
#print("Args:", arg)
