#!/usr/bin/env python
#
# Copyright 2020 by Philip N. Garner
#
# See the file COPYING for the licence associated with this software.
#
# Author(s):
#   Phil Garner, October 2020
#

class Verb:
    def __init__(self, stem):
        self.stem = stem

    def conj(self, suff):
        def concat(a):
            return self.stem+a
        return list(map(concat, suff))


# This is just a base class; it is here to capitalise on the fact that the
# imperfect and conditional share conjugations.
class Regular(Verb):
    def present(self):
        return self.conj(['e', 'es', 'e', 'ons', 'ez', 'ent'])

    def imperfect(self):
        return self.conj(['ais', 'ais', 'ait', 'ions', 'iez', 'aient'])

    def future(self):
        return self.conj(['ai', 'as', 'a', 'ons', 'ez', 'ont'])

    def historic(self):
        return self.conj(['ai', 'as', 'a', 'âmes', 'âtes', 'èrent'])

    def conditional(self):
        return self.imperfect() # Same as imperfect, but with the stem

    def participles(self):
        return self.conj(['ant', 'é'])


# This is the true regular class
class RegularER(Regular):
    def future(self):
        v = Regular(self.stem+'er')
        return v.future()

    def conditional(self):
        v = Regular(self.stem+'er')
        return v.imperfect()


# E.g., finir
class RegularIR(Regular):
    def present(self):
        return self.conj(['is', 'is', 'it', 'issons', 'issez', 'issent'])

    def imperfect(self):
        v = Regular(self.stem+'iss')
        return v.imperfect()

    def future(self):
        v = Regular(self.stem+'ir')
        return v.future()

    def historic(self):
        return self.conj(['is', 'is', 'it', 'îmes', 'îtes', 'irent'])

    def conditional(self):
        v = Regular(self.stem+'ir')
        return v.conditional()

    def participles(self):
        return self.conj(['issant', 'i'])


# Based on conduire, but it's a bad example
class RegularRE(Regular):
    def present(self):
        return self.conj(['s', 's', 't', 'sons', 'sez', 'sent'])

    def imperfect(self):
        v = Regular(self.stem+'s')
        return v.imperfect()

    def future(self):
        v = Regular(self.stem+'r')
        return v.future()

    def historic(self):
        v = RegularIR(self.stem+'s')
        return v.historic()

    def conditional(self):
        v = Regular(self.stem+'r')
        return v.conditional()

    def participles(self):
        return self.conj(['ant', 'é'])


def split_stem(verb):
    stem = verb[:-2]
    suff = verb[-2:]
    return [stem, suff]

def toClass(verb):
    [stem, suff] = split_stem(verb)
    if suff == 'er':
        return RegularER(stem)
    elif suff == 're':
        return RegularRE(stem)
    elif suff == 'ir':
        return RegularIR(stem)
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
