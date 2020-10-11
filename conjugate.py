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


# E.g., finir
class RegularIR(Regular):
    def present(self):
        return self.sconj(['is', 'is', 'it', 'issons', 'issez', 'issent'])

    def imperfect(self):
        v = Regular(self.stem+'iss')
        return v.imperfect()

    def historic(self):
        return self.sconj(['is', 'is', 'it', 'îmes', 'îtes', 'irent'])

    def participles(self):
        return self.sconj(['issant', 'i'])


# Based on conduire, but it's a bad example
class RegularRE(Regular):
    def present(self):
        return self.sconj(['s', 's', 't', 'sons', 'sez', 'sent'])

    def imperfect(self):
        v = Regular(self.stem+'s')
        return v.imperfect()

    def historic(self):
        v = RegularIR(self.stem+'s')
        return v.historic()

    def participles(self):
        return self.sconj(['sant', 't'])


def split_stem(verb):
    stem = verb[:-2]
    suff = verb[-2:]
    return [stem, suff]

def toClass(verb):
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
