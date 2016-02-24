from pprint import pprint as pp
from corpus import ngram

presubvector = [('r', 'test/pre_tokenizer.regexp'),
				('a', 'test/abbreviation.list')]
postsubvector = [('f', 'test/post_functions.list')]
funcrepolist = ['test/fnscanner.py']

ng = ngram()
ng.set_tokenizer(presubvector, postsubvector, funcrepolist)

pp(dir(ng.tokenizer))
pp(ng.tokenizer.presubvector)
pp(ng.tokenizer.postsubvector)
ng.update('test/pg108.txt',3)
print ng.summary(True, True, True)
