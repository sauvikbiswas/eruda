# This class takes a file or a string or another parser and converts
# it into individual, linear list-of-list-of-strings.
# It can insert tags as required
# EOS, EOP, Phone, Place, etc.

from pprint import pprint as pp

class regexops(object):
	
	def __init__(self, filename, abbrevfile = ''):
		import re
		self.subvector = []
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

	def sub(self, data):
		for subre, findstr, replacestr in self.subvector:
			data = subre.sub(replacestr, data)
			print data
		return data
		
	def add_abbrev(self, abbrevfile):
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
		

class parser(object):
	def __init__(self, filename=''):
		self.raw = ''
		self.parsed = []
		
		if filename != '':
			self.update(filename)
		return

	def update(self, data):
		'''parser.update(filename) updates the data with that of a file'''
		self.raw += data
		
		# This is a tricky part from an implementation standpoint.
		# How it has to be parsed is something that must come from
		# a predefined set of rules.
	
		# Step 1: Condition the data using a vector of regexp subs
		
		self.parsed = [line.split() for line in raw.split('\n')]
		return

x = regexops('pre_tokenizer.regexp')
pp(x.add_abbrev('abbreviation.list'))
pp(x.subvector)
pp(x.sub('Mr. and Mrs. Smith went to Washington with I.O.U. their kids. Their kids got lost! ken. mccoy filename.java is a file. 999-888-999 is a number, 55.980 is also a number, so is .999'))
