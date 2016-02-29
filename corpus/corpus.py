# Not part of Eruda. This is here to hijack code into the ngram class
import re
from pprint import pprint as pp
from math import log


class corpus(object):

    def __init__(self, filename=''):
        self.histogram = {}		# Histogram data of the corpus
        self.probability = {}  # Conditional probability
        self.frequency = {}		# Frequency of frequency
        self.size = 0			# Corpus size
        if filename != '':
            self.update(filename)
        return

    def update(self, filename, order=4):
        # Update the histogram
        try:
            with open(filename, 'rU') as fp:
                data = []
                lines = self.eos_condition(fp.read()).lower().split('\n')
                for line in lines:
                    ignore_bool = bool(re.match('^ *<s> *</s> *$', line))
                    if not ignore_bool:
                        data.append([item.strip('"\'').lower()
                                     for item in line.split()
                                     if item.strip('"\' ') != ''])

                for sentence in data:
                    # Length is the maximum order possible.
                    # A shorter sentence will not have the order specified.
                    length = order if len(sentence) >= order\
                        else len(sentence)
                    for itlen in range(length):		# itlen = iteration len
                        for i, word in enumerate(sentence):
                            if i >= itlen:		# i.e. clustering possible
                                wset = [sentence[j]
                                        for j in range(i - itlen, i + 1)]
                                self.hist_update(tuple(wset))

                for word in self.histogram:
                    freq = self.histogram[word]
                    if freq in self.frequency:
                        self.frequency[freq] += 1
                    else:
                        self.frequency[freq] = 1
        except IOError:
            raise IOError('Cannot read %s')

        self.p_compute()
        return

    def eos_condition(self, sentence):
        eos = re.compile(' *[.?!\n] *', re.I)
        sentence = '<s> ' + sentence
        sentence = eos.sub(' </s>\n<s> ', sentence)
        if sentence[-5:] != '</s> ':
            sentence += ' </s> '
        return sentence

    def hist_update(self, item):
        if len(item) == 1:
            self.size += 1
        if item in self.histogram:
            self.histogram[item] += 1
        else:
            self.histogram[item] = 1
        return

    def p_compute(self):
        # This probability counts the max. likelihood estimate MLE of
        # an n-gram where n!=1. MLE = count(n-gram) / count(n-1-gram)
        # In case of an unigram, it computes the count(unigram) / N-corpus
        # Stores the log10 of p
        h = self.histogram
        for item in h:
            if len(item) > 1:
                self.probability[item] = \
                    log(float(h[item]) / h[item[:-1]], 10)
            else:
                self.probability[item] = \
                    log(float(h[item]) / self.size, 10)
        return

    def ngram(self, sentence):
        words = self.eos_condition(sentence).lower().strip().split()
        p = self.probability
        pc = 0.0
        for itlen in range(len(words)):
            for i, word in enumerate(words):
                if i >= itlen:		# i.e. clustering possible
                    wset = [words[j]
                            for j in range(i - itlen, i + 1)]
                    if tuple(wset) in p:
                        pc += p[tuple(wset)]
                    else:
                        pc += log(float(self.frequency[1]) / self.count, 10)
        return pc

    def bigram(self, sentence):
        words = self.eos_condition(sentence).lower().strip().split()
        p = self.probability
        pc = 0.0
        for i, word in enumerate(words):
            if i != 0:
                if (words[i - 1], word) in p:
                    pc += p[(words[i - 1], word)]
                else:
                    pc += log(float(self.frequency[1]) / self.count, 10)
        return pc

    def shannon_sentence(self, word):
        word = word.lower().strip()
        p = self.probability
        blist = filter(lambda x: x[0] == word, p.keys())
        flist = [p[item] for item in blist]
        fmax = reduce(lambda x, y: x if x > y else y, flist)
        maxppair = blist[flist.index(fmax)]
        if maxppair[1] == '</s>':
            return word
        else:
            return word + ' ' + self.shannon_sentence(maxppair[1])

    def stupid_backoff(self, sentence, knockdown=0.4):
        words = self.eos_condition(sentence).lower().strip().split()
        p = self.probability
        print words
        if tuple(words) in p:
            return p[tuple(words)]
        else:
            if len(words) == 1:
                return -100.0
            else:
                return math.log(knockdown, 10) \
                    + self.stupid_backoff(' '.join(words[2:-1]),
                                          knockdown)

x = corpus('tdata/pg108.txt')
x.update('tdata/pg244.txt')
print x.bigram('I am the weapon')
print x.ngram('I am the weapon')
print x.stupid_backoff('Elementary My Dear Wattson')
# print x.shannon_sentence('weapon')
pp(sorted(['%s : %s' % (str(x.histogram[key]).zfill(5), key)
           for key in x.histogram]))
# print '--------------------------'
#pp(sorted(['%s : %s' % (str(x.frequency[key]).zfill(5), key) for key in x.frequency]))
