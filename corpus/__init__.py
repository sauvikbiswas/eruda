class ngram(object):
	def __init__(self, filename=''):
		self.histogram = {}		# Histogram data of the corpus
		self.probability = {}	# Conditional probability
		self.frequency = {}		# Frequency of frequency
		self.size = 0			# Corpus size
		self.tokenizer = None	# Tokenizer object used to parse this ngram
		return
	
	def set_tokenizer(self, presubvector, postsubvector, funcrepolist):
		'''
		This initiates a set of substitution vectors for the corpus to be
		digested.
		'''
		from parser import tokenizer
		tokobj = tokenizer()
		for funcrepo in funcrepolist: tokobj.add_function_repo(funcrepo)
		for vector in (presubvector, postsubvector):
			if vector==presubvector: loc='pre'
			else: loc='post'
			for vecttype, vectfile in vector:
				if vecttype.lower() == 'r':
					tokobj.add_subvect(vectfile, op_seq=loc)
				elif vecttype.lower() == 'f':
					tokobj.add_function(vectfile, op_seq=loc)
				else:
					tokobj.add_abbrev(vectfile, op_seq=loc)
		self.tokenizer = tokobj
		return

	def __condition__(self, data):
		'''
		This function takes a list of strings and breaks it into
		a list of list of strings. Each sentence is represented as
		a list of strings.
		'''
		import re
		eos = re.compile('^[\.?!]$')
		# We don't need '' for ngram analysis
		data = [item for item in data if item != '']
		datanew = []
		initflag = True
		for item in data:
			if initflag:
				sentence = ['<s>']
				initflag = False
			if not eos.match(item):
				sentence.append(item)
			else:
				sentence.append('</s>')
				if sentence != ['<s>', '</s>']:
					datanew.append(sentence)
				initflag = True
		if not initflag:
			sentence.append('</s>')
			if sentence != ['<s>', '</s>']:
				datanew.append(sentence)
		return datanew

	def hist_update(self, item):
		if len(item) == 1:
			self.size += 1
		if item in self.histogram:
			self.histogram[item] += 1
		else:
			self.histogram[item] = 1
		return

	def p_compute(self):
		'''
		This probability counts the max. likelihood estimate MLE of
		an n-gram where n!=1. MLE = count(n-gram) / count(n-1-gram)
		In case of an unigram, it computes the count(unigram) / N-corpus
		Stores the log10 of p
		'''
		from math import log10
		h = self.histogram
		for item in h:
			if len(item) > 1:
				self.probability[item] = \
					log10(float(h[item])/h[item[:-1]])
			else:
				self.probability[item] = \
					log10(float(h[item])/self.size)
		return		

	def update(self, filename, order=2):
		with open(filename, 'rU') as fp:
			data = fp.read()

		datastream = self.tokenizer.tokenize(data)
		cdata = self.__condition__(datastream)

		for sentence in cdata:
			length = order if len(sentence) >= order else len(sentence)
			for itlen in range(length):
				# itlen = iteration len
				for i, word in enumerate(sentence):
					if i >= itlen:		
					# i.e. clustering possible
						wset = [sentence[j]\
							for j in range(i-itlen, i+1)]
						self.hist_update(tuple(wset))

		# Recompute the frequency of frequencies
		for word in self.histogram:
			freq = self.histogram[word]
			if freq in self.frequency:
				self.frequency[freq] += 1
			else:
				self.frequency[freq] = 1

		# Recompute the probabilities / MLEs
		self.p_compute()
		return

	def summary(self, histogram=False, probability=False, frequency=False):
		repr_str = 'Vocabulary size	: '+str(self.size)+'\n'+\
			'Entries			: '+str(len(self.histogram))

		if histogram:
			repr_str += '\nHistogram :\n'+'-'*80+'\n'+\
				'\n'.join(sorted(['%s : %s' % \
				(str(self.histogram[key]).zfill(5),key)\
				for key in self.histogram]))
		if probability:
			repr_str += '\nProbability :\n'+'-'*80+'\n'+\
				'\n'.join(sorted(['%s : %s' % \
				(str(self.probability[key]),key)\
				for key in self.probability]))
		if frequency:
			repr_str += '\nFrequency :\n'+'-'*80+'\n'+\
				'\n'.join(sorted(['%s : %s' % \
				(str(self.frequency[key]).zfill(5),key)\
				for key in self.frequency]))
		
		repr_str +='\n'
		return repr_str
