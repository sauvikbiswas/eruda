from parser import tokenizer
from pprint import pprint as pp

x = tokenizer()
x.add_regex('example/pre_tokenizer.regexp')
#x.add_abbrev('example/abbreviation.list')
x.add_function_repo('example/fnscanner.py', test=True)
x.add_function('example/pre_functions.list', op_seq='pre')
x.add_function('example/post_functions.list', op_seq='post')
pp(x.tokenize('I don\'t know.'))
