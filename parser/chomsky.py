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

grammer = [('S', ('NP', 'VP')),
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


def _epsilon_removal(grammer):
    # Split the grammer into entries to be removed and entries to be kept.
    # All epsilon values will be removed
    # In some literature this is also null definition remover.
    removal_list = [entry for entry in grammer if entry[1] == ()]
    grammer_new = [entry for entry in grammer if entry[1] != ()]
    add_entries = {}
    for replace, empty in removal_list:
        for i, (symbol, definition) in enumerate(grammer):
            new_definition = _remove_tuple_item(definition, replace)
            if new_definition != definition and new_definition != ():
                add_entries[i] = (symbol, new_definition)
        grammer_new = _index_inject(grammer_new, add_entries)
    return grammer_new


def _append_lexicon(lexicon, unary_entry):
    # Lexicon augmentation with a unary entry where a non-terminal def.
    # becomes a terminal def.
    symbol, definition = unary_entry
    add_entries = {}
    for i, (symtype, lex) in enumerate(lexicon):
        if symtype == definition[0]:
            add_entries[i] = (symbol, lex)
    lexicon = _index_inject(lexicon, add_entries)
    return lexicon


def _unary_expansion(grammer, lexicon):
    removal_list = [entry for entry in grammer if len(entry[1]) == 1]
    if len(removal_list) == 0:
        return grammer, lexicon
    add_entries = {}
    s_symbol, s_definition = removal_list[0]
    # We don't need to operate when a rule (NP -> NP) is encountered
    # However it must be deleted. see grammer.remove line
    if s_symbol != s_definition[0]:
        found = False
        for i, (symbol, definition) in enumerate(grammer):
            if symbol == s_definition[0]:
                found = True
                # This means that a non terminal symbol is found.
                # No need to alter the lexicon
                add_entries[i] = (s_symbol, definition)
        grammer = _index_inject(grammer, add_entries)
        if not found:
            # If a non terminal symbol is not found, there is a chance
            # that it could be a terminal symbol. In such a case,
            # lexicon must be altered.
            lexicon = _append_lexicon(lexicon, removal_list[0])
    grammer.remove(removal_list[0])
    return _unary_expansion(grammer, lexicon)


def _remove_redundant(lexicon, grammer):
    # Resolution may lead to a lexical entry whose symbol is never resolved
    # by the grammer. Such entries can be deleted.
    terminals = reduce(lambda x, y: list(x) + list(y),
                       [symbol for empty, symbol in grammer])
    return [entry for entry in lexicon if entry[0] in terminals]


def _remove_higher_order(grammer):
    # Binarization of grammer
    add_entries = {}
    found = False
    for i, (symbol, definition) in enumerate(grammer):
        if len(definition) > 2:
            found = True
            new_sym = '@' + symbol + '_' + definition[0]
            add_entries[i] = (new_sym, definition[1:])
            grammer[i] = (symbol, (definition[0], new_sym))
    grammer = _index_inject(grammer, add_entries)
    # If there was a split, there is a possibility that the split might
    # have still retained higher order grammers for cases where length
    # of definition was greater than 3)
    if found:
        return _remove_higher_order(grammer)
    else:
        return grammer

from pprint import pprint as pp
# pp(grammer)
grammer = _epsilon_removal(grammer)
pp(grammer)
grammer, lexicon = _unary_expansion(grammer, lexicon)
lexicon = _remove_redundant(lexicon, grammer)
# pp(grammer)
# pp(lexicon)
#grammer, lexicon = _unary_expansion(grammer, lexicon)
pp(grammer)
pp(lexicon)
grammer = _remove_higher_order(grammer)
pp(grammer)
# print lexicon
