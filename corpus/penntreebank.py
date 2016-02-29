# Copyright 2016, Sauvik Biswas
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Custom POS class


class pos(object):

    def __init__(self, code, description):
        self.symbol = code
        self.description = description
        return

    def __repr__(self):
        return self.symbol

    def __str__(self):
        return self.__repr__()

# Penn Treebank standard POS
# Copyright, Mitchell P. Marcus, et al.
# https://www.cis.upenn.edu/~treebank/
# treebank@unagi.cis.upenn.edu

penntreebank = {
    'CC': 'Coordinating conjunction',
    'CD': 'Cardinal number',
    'DT': 'Determiner',
    'EX': 'Existential there',
    'FW': 'Foreign word',
    'IN': 'Preposition or subordinating conjunction',
    'JJ': 'Adjective',
    'JJR': 'Adjective, comparative',
    'JJS': 'Adjective, superlative',
    'LS': 'List item marker',
    'MD': 'Modal',
    'NN': 'Noun, singular or mass',
    'NNS': 'Noun, plural',
    'NNP': 'Proper noun, singular',
    'NNPS': 'Proper noun, plural',
    'PDT': 'Predeterminer',
    'POS': 'Possessive ending',
    'PRP': 'Personal pronoun',
    'PRP$': 'Possessive pronoun',
    'RB': 'Adverb',
    'RBR': 'Adverb, comparative',
    'RBS': 'Adverb, superlative',
    'RP': 'Particle',
    'SYM': 'Symbol',
    'TO': 'to',
    'UH': 'Interjection',
    'VB': 'Verb, base form',
    'VBD': 'Verb, past tense',
    'VBG': 'Verb, gerund or present participle',
    'VBN': 'Verb, past participle',
    'VBP': 'Verb, non-3rd person singular present',
    'VBZ': 'Verb, 3rd person singular present',
    'WDT': 'Wh-determiner',
    'WP': 'Wh-pronoun',
    'WP$': 'Possessive wh-pronoun',
    'WRB': 'Wh-adverb',
}

# Penn Treebank standard POS as pos objets
CC = pos('CC', penntreebank['CC'])
CD = pos('CD', penntreebank['CD'])
DT = pos('DT', penntreebank['DT'])
EX = pos('EX', penntreebank['EX'])
FW = pos('FW', penntreebank['FW'])
IN = pos('IN', penntreebank['IN'])
JJ = pos('JJ', penntreebank['JJ'])
JJR = pos('JJR', penntreebank['JJR'])
JJS = pos('JJS', penntreebank['JJS'])
LS = pos('LS', penntreebank['LS'])
MD = pos('MD', penntreebank['MD'])
NN = pos('NN', penntreebank['NN'])
NNS = pos('NNS', penntreebank['NNS'])
NNP = pos('NNP', penntreebank['NNP'])
NNPS = pos('NNPS', penntreebank['NNPS'])
PDT = pos('PDT', penntreebank['PDT'])
POS = pos('POS', penntreebank['POS'])
PRP = pos('PRP', penntreebank['PRP'])
PRP_ = pos('PRP$', penntreebank['PRP$'])
RB = pos('RB', penntreebank['RB'])
RBR = pos('RBR', penntreebank['RBR'])
RBS = pos('RBS', penntreebank['RBS'])
RP = pos('RP', penntreebank['RP'])
SYM = pos('SYM', penntreebank['SYM'])
TO = pos('TO', penntreebank['TO'])
UH = pos('UH', penntreebank['UH'])
VB = pos('VB', penntreebank['VB'])
VBD = pos('VBD', penntreebank['VBD'])
VBG = pos('VBG', penntreebank['VBG'])
VBN = pos('VBN', penntreebank['VBN'])
VBP = pos('VBP', penntreebank['VBP'])
VBZ = pos('VBZ', penntreebank['VBZ'])
WDT = pos('WDT', penntreebank['WDT'])
WP = pos('WP', penntreebank['WP'])
WP_ = pos('WP$', penntreebank['WP$'])
WRB = pos('WRB', penntreebank['WRB'])

# Other POS from Penn Treebank II POS
STOP = pos('.', 'Punctuation mark, sentence closer')
COMMA = pos(',', 'Punctuation mark, comma')
COLON = pos(':', 'Punctuation mark, colon')
LPAREN = pos('(', 'Contextual separator, left paren')
RPAREN = pos('(', 'Contextual separator, left paren')
