from pprint import pprint as pp
from corpus import ngram

presubvector = [('r', 'example/pre_tokenizer.regexp'),
				('r', 'example/pre_tokenizer_no_newline.regexp'),
				('a', 'example/abbreviation.list')]
postsubvector = [('f', 'example/post_functions.list')]
funcrepolist = ['example/fnscanner.py']

ng = ngram()
ng.set_tokenizer(presubvector, postsubvector, funcrepolist)

pp(dir(ng.tokenizer))
pp(ng.tokenizer.presubvector)
pp(ng.tokenizer.postsubvector)
ng.update('example/pg108.txt',3)
print ng.summary(True, True, True)
