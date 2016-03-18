from pprint import pprint as pp
from parser import PSG

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
# pp(psg.grammar)
psg.CNF_unary_expansion()
pp(psg.grammar)
pp(psg.lexicon)
psg.CNF_remove_redundant()
pp(psg.grammar)
pp(psg.lexicon)
psg.CNF_remove_higher_order()
pp(psg.grammar)
# print lexicon
