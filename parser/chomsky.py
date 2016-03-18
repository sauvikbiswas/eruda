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

# Helper functions


def _remove_tuple_item(tup, item):
    # Removes an item from a tuple
    return tuple([iter_item for iter_item in tup if iter_item != item])


def _index_inject(alist, adict):
    # adict is of the form key->value = item_index->item
    # alist will be modified with items inserted just after item_index.
    for key in sorted(adict.keys(), reverse=True):
        if type(key) == type(1):
            if adict[key] not in alist:
                alist.insert(key + 1, adict[key])
    return alist


class PSG(object):

    def __init__(self, grammar=[], lexicon=[]):
        self.grammar = grammar
        self.lexicon = lexicon
        return

    def __add__(self, other):
        return PSG(self.grammar + other.grammer, self.lexicon + other.lexicon)

    def append_grammar(self, grammar):
        self.grammar += grammar
        return

    def append_lexicon(self, lexicon):
        self.lexicon += lexicon
        return

    def CNF_epsilon_removal(self):
        # Split the grammar into entries to be removed and entries
        # to be kept.
        # All epsilon values will be removed
        # In some literature this is also null definition remover.
        removal_list = [entry for entry in self.grammar if entry[1] == ()]
        grammar_new = [entry for entry in self.grammar if entry[1] != ()]
        add_entries = {}
        for replace, empty in removal_list:
            for i, (symbol, definition) in enumerate(grammar):
                new_definition = _remove_tuple_item(definition, replace)
                if new_definition != definition and new_definition != ():
                    add_entries[i] = (symbol, new_definition)
            grammar_new = _index_inject(grammar_new, add_entries)
        self.grammar = grammar_new
        return

    def _modify_lexicon(self, unary_entry):
        # Lexicon augmentation with a unary entry where a non-terminal def.
        # becomes a terminal def.
        symbol, definition = unary_entry
        add_entries = {}
        for i, (symtype, lex) in enumerate(self.lexicon):
            if symtype == definition[0]:
                add_entries[i] = (symbol, lex)
        self.lexicon = _index_inject(self.lexicon, add_entries)
        return

    def CNF_unary_expansion(self):
        removal_list = [entry for entry in self.grammar if len(entry[1]) == 1]
        if len(removal_list) == 0:
            return
        add_entries = {}
        s_symbol, s_definition = removal_list[0]
        # We don't need to operate when a rule (NP -> NP) is encountered
        # However it must be deleted. see grammar.remove line
        if s_symbol != s_definition[0]:
            found = False
            for i, (symbol, definition) in enumerate(self.grammar):
                if symbol == s_definition[0]:
                    found = True
                    # This means that a non terminal symbol is found.
                    # No need to alter the lexicon
                    add_entries[i] = (s_symbol, definition)
            self.grammar = _index_inject(self.grammar, add_entries)
            if not found:
                # If a non terminal symbol is not found, there is a chance
                # that it could be a terminal symbol. In such a case,
                # lexicon must be altered.
                self._modify_lexicon(removal_list[0])
        self.grammar.remove(removal_list[0])
        self.CNF_unary_expansion()
        return

    def CNF_remove_redundant(self):
        # Resolution may lead to a lexical entry whose symbol is never
        # resolved by the grammar. Such entries can be deleted.
        terminals = reduce(lambda x, y: list(x) + list(y),
                           [symbol for empty, symbol in self.grammar])
        self.lexicon = [entry for entry in lexicon if entry[0] in terminals]
        return

    def CNF_remove_higher_order(self):
        # Binarization of grammar
        add_entries = {}
        found = False
        for i, (symbol, definition) in enumerate(self.grammar):
            if len(definition) > 2:
                found = True
                new_sym = '@' + symbol + '_' + definition[0]
                add_entries[i] = (new_sym, definition[1:])
                self.grammar[i] = (symbol, (definition[0], new_sym))
        self.grammar = _index_inject(self.grammar, add_entries)
        # If there was a split, there is a possibility that the split might
        # have still retained higher order grammars for cases where length
        # of definition was greater than 3)
        if found:
            self.CNF_remove_higher_order()
        else:
            return

    def CNF(self):
        # Chains all CNF ops
        self.CNF_epsilon_removal()
        self.CNF_unary_expansion()
        self.CNF_remove_redundant()
        self.CNF_remove_higher_order()
        return


from pprint import pprint as pp
grammar = [('S', ('NP', 'VP')),
           ('VP', ('V', 'NP')),
           ('VP', ('V', 'NP', 'PP')),
           ('NP', ('NP', 'NP')),
           ('NP', ('NP', 'PP')),
           ('NP', ('N',)),
           ('NP', ()),
           ('PP', ('P', 'NP'))]

lexicon = [('N', 'people'),
           ('N', 'fish'),
           ('N', 'tanks'),
           ('N', 'rods'),
           ('V', 'people'),
           ('V', 'fish'),
           ('V', 'tanks'),
           ('P', 'with')]

# pp(grammar)
psg = PSG(grammar, lexicon)
psg.CNF_epsilon_removal()
pp(psg.grammar)
psg.CNF_unary_expansion()
psg.CNF_remove_redundant()
pp(psg.grammar)
pp(psg.lexicon)
psg.CNF_remove_higher_order()
pp(psg.grammar)
# print lexicon
