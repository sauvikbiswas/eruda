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
import urllib2
import urllib
from bs4 import BeautifulSoup as bsoup
import re
import string

bulletnore = re.compile('<b>(\d+|[a-z])\. </b>')
typere = re.compile('n\.|adj\.|adv\.|v\.|n\.pl\.')

def fetch_raw_data(url, values={}, headers={}, method='POST'):
    data = urllib.urlencode(values)
    if method == 'GET':
        url = url + '?' + data
    req = urllib2.Request(url, data, headers)
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            print 'Couldn\'t reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfil the request'
            print 'Error code:', e.code
    else:
        page = response.read()
        return page


def _extract_rel_words(souplist):
    '''Extracts related words from a souplist.'''
    rellist = []
    for soup in souplist:
        entries = reduce(lambda x, y: x + y,
                         [entry(text=True) for entry in soup('a')])
        rellist += entries
    return rellist

def _extract_pseg_lemma(souplist):
    for soup in souplist:
        data = [item for item in soup(lambda x: not x.has_attr('class'), recursive=False)]
        if len(data) > 1:
            print data
            for item in data:
                print item.name
                print item.text.replace(u'\xb7','').replace(u'\u2032', '')

def parse_data(page):
    soup = bsoup(page, 'html.parser')
    relationdict = {}

    # This following code will give us the Synonyms, Antonyms and Related
    # words.
    wndata = soup.find('section', attrs={'data-src': 'wn'})
    postype = ''
    for row in wndata('tr'):
        for i, col in enumerate(row('td')):
            data = col(text=True)
            if i == 0:
                temptype = data
            if i == 1 and data == [u'1.']:
                postype = temptype[0]
            if postype not in relationdict:
                relationdict[postype] = {}
                relationdict[postype]['Syn'] = []
                relationdict[postype]['Ant'] = []
                relationdict[postype]['Rel'] = []
            relationdict[postype]['Syn'] += \
                _extract_rel_words(col('div',  attrs={'class': 'Syn'}))
            relationdict[postype]['Ant'] += \
                _extract_rel_words(col('div',  attrs={'class': 'Ant'}))
            relationdict[postype]['Rel'] += \
                _extract_rel_words(col('div',  attrs={'class': 'Rel'}))

    wndata = soup.find('section', attrs={'data-src': 'hm'})
    _extract_pseg_lemma(wndata('div', attrs={'class': 'pseg'}))
    _extract_pseg_lemma(wndata('div', attrs={'class': 'runseg'}))

    return relationdict

page = fetch_raw_data('http://www.thefreedictionary.com/fly')
print parse_data(page)
