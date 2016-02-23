from parser import tokenizer
from pprint import pprint as pp

x = tokenizer()
x.add_subvect('test/pre_tokenizer.regexp')
#x.add_abbrev('test/abbreviation.list')
x.add_function_repo('test/fnscanner.py')
x.add_function('test/post_functions.list', op_seq='post')
pp(x.tokenize('I don\'t know.'))
