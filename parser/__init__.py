# This class takes a file or a string or another parser and converts
# it into individual, linear list-of-list-of-strings.
# It can insert tags as required
# EOS, EOP, Phone, Place, etc.

from pprint import pprint as pp

class tokenizer(object):
	
	def __init__(self, filename = '', abbrevfile = ''):
		self.subvector = []
		self.prefuncvector = []
		self.postfuncvector = []
		if filename.strip() != '':
			self.add_subvect(filename)
		if abbrevfile.strip() != '':
			self.add_abbrev(abbrevfile)

	def add_subvect(self, filename):
		'''Reads an list of substitution vectors'''
		import re
		with open(filename, 'rU') as fp:
			data = fp.read().split('\n')
		findflag = False
		findstr = ''
		for line in data:
			if not line.startswith('#'):
				if findflag:
					self.subvector.append((re.compile(findstr),\
						findstr, line))
					findflag = False
				else:
					findstr = line
					findflag = True
		return

	def add_abbrev(self, abbrevfile):
		'''Computes the contraction of period and adds them to the substitution vector'''
		import re
		with open(abbrevfile, 'rU') as fp:
			data = fp.read().split('\n')
		source = [re.sub('^ \. ', '.', re.sub('\.', ' *\. *', item)) \
			for item in data \
			if not item.startswith('#')]
		data = [re.sub('\.$', '. ', item) for item in data \
			if not item.startswith('#')]
		self.subvector += [(re.compile(source[i]), source[i], item) \
			for i, item in enumerate(data) \
			if item.strip() != '']
		return
	
#	def add_function(self, funcfile, op_seq='pre'):
	
	def sub(self, data):
		'''Runs the substitution vector on data'''
		for subre, findstr, replacestr in self.subvector:
			data = subre.sub(replacestr, data)
		return data
		
#	def tokenize(self, data):
		

x = tokenizer('pre_tokenizer.regexp', 'abbreviation.list')
pp(x.sub('Mr. and Mrs. Smith went to San Francisco with I.O.U. their kids. Their kids got lost! ken. mccoy filename.java is a file. 999-888-999 is a number, 55.980 is also a number, so is .999. i is a variable.').split(' '))
