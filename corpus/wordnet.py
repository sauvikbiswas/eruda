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
from pymongo import MongoClient

# Self imports
from wnet_pointer_sym import pointer_sym


class wordnet(object):

    def __init__(self, mongourl=None, wnetdb='wnetdb'):
        '''Initialize the WordNet database'''
        self.wnetdb = None
        self.pointer_sym = pointer_sym
        self.client = MongoClient() if not mongourl \
            else MongoClient(mongourl)
        db = self.client[wnetdb]
        self.wnetdb = db['root']
        return

    def __add_wnet_indices__(self, filename):
        commentre = re.compile('^  [0-9]+ .*')
        entryre = re.compile('^(?P<lemma>[^ ]+) (?P<pos>[a-z]) ' +
                             '(?P<synset_cnt>[0-9]+) (?P<p_cnt>[0-9]+) ' +
                             '(?P<ptr_symbol>[^0-9]+ )+(?P<sense_cnt>[0-9]+) ' +
                             '(?P<tagsense_cnt>[0-9]+) (?P<synset_offset>[0-9 ]+)')
        with open(filename, 'rU') as fp:
            data = fp.read().split('\n')
        for line in data:
            match = commentre.match(line)
            if not match:
                ematch = entryre.match(line)
                if ematch:
                    matchdict = ematch.groupdict()
                    matchdict['ptr_symbol'] = \
                        matchdict['ptr_symbol'].strip().split(' ')
                    matchdict['synset_offset'] = \
                        matchdict['synset_offset'].strip().split(' ')
                    m_id = self.wnetdb.insert_one(matchdict)
                    print m_id, matchdict
        return

    def grind(self, folder):
        '''Grind a database into the db'''
        # Clear any exixting data
        print self.wnetdb
        self.client.drop_database('wnetdb')
        # Add data
        self.__add_wnet_indices__(os.path.join(folder, 'index.noun'))
        return


x = wordnet()
x.grind('./wnetdb')
