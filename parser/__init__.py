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

# Env imports
import re
import os.path
import sys


class tokenizer(object):

    def __init__(self,):

        self.FUNCTION = 1
        self.PRE = 2
        self.POST = 3

        # Substitution vectors
        self.presubvector = []
        self.funcvector = {}
        self.postsubvector = []

        return

    def add_regex(self, filename, op_seq='pre'):
        '''Reads an list of substitution vectors'''
        with open(filename, 'rU') as fp:
            data = fp.read().split('\n')
        findflag = False
        findstr = ''
        for line in data:
            if not line.startswith('#'):
                if findflag:
                    if op_seq == self.PRE or op_seq == 'pre':
                        self.presubvector.append((re.compile(findstr),
                                                  findstr, line))
                    else:
                        self.postsubvector.append((re.compile(findstr),
                                                   findstr, line))
                    findflag = False
                else:
                    findstr = line
                    findflag = True
        return

    def add_abbrev(self, abbrevfile, op_seq='pre'):
        '''
        Computes the contraction of period and adds them to the 
        substitution vector
        '''
        with open(abbrevfile, 'rU') as fp:
            data = fp.read().split('\n')
        source = [re.sub('^ \. ', '.', re.sub('\.', ' *\. *', item))
                  for item in data
                  if not item.startswith('#')]
        data = [re.sub('\.$', '. ', item) for item in data
                if not item.startswith('#')]
        subvector = [(re.compile(source[i]), source[i], item)
                     for i, item in enumerate(data)
                     if item.strip() != '']
        if op_seq == self.PRE or op_seq == 'pre':
            self.presubvector += subvector
        else:
            self.postsubvector += subvector
        return

    def add_function_repo(self, funcfile):
        '''
        Adds all L1 functions to the current object.
        '''
        fnre = re.compile('\ndef (.*)\(')
        with open(funcfile, 'rU') as fp:
            code = '\n' + fp.read()
        funclist = fnre.findall(code)
        funcpath, funcmodule = os.path.split(re.sub('.pyc*$', '', funcfile))
        if funcpath != '':
            sys.path.insert(0, funcpath)
        fn = __import__(funcmodule, globals(), locals(), funclist, -1)
        fndict = {funcmodule + '.' + funcname: getattr(fn, funcname)
                  for funcname in funclist}
        self.funcvector.update(fndict)
        return

    def add_function(self, fnvectfile, op_seq='pre'):
        with open(fnvectfile, 'rU') as fp:
            data = fp.read().split('\n')
        fnsubvector = [(self.funcvector[item.strip()], item, self.FUNCTION)
                       for item in data if item.strip() != '']
        if op_seq == self.PRE or op_seq == 'pre':
            self.presubvector += fnsubvector
        else:
            self.postsubvector += fnsubvector
        return

    def sub(self, data, op_seq='pre'):
        '''Runs the substitution vector on data'''
        if op_seq == self.PRE or op_seq == 'pre':
            subvector = self.presubvector
        else:
            subvector = self.postsubvector

        for subre, findstr, replacestr in subvector:
            if replacestr == self.FUNCTION:
                if op_seq == self.PRE or op_seq == 'pre':
                    data = subre(data)
                else:
                    data = [subre(item) for item in data]
            else:
                if op_seq == self.PRE:
                    data = subre.sub(replacestr, data)
                else:
                    data = [subre.sub(replacestr, item) for item in data]
        return data

    def tokenize(self, data):
        return self.sub(self.sub(data, self.PRE).split(' '), self.POST)
