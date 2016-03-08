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
from lxml import html
import re


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

def parse_rel(tree):
    tbody = tree.xpath('//section[@data-src="wn"]/table/tbody')
    print tbody(root)[0].tag

def parse_lemma(tree):
    for data in tree.xpath('//section[@data-src="hm"]/div[@class="pseg"]'):
        print data.text_content()
    print tree.xpath('//section[@data-src="hm"]/div[@class="pseg"]/i/following-sibling::b/text()')
    print tree.xpath('//section[@data-src="hm"]/div[@class="pseg"]/i/text()')
    print tree.xpath('//section[@data-src="hm"]/div[@class="runseg"]/b/text()')
    print tree.xpath('//section[@data-src="hm"]/div[@class="runseg"]/i/text()')


page = fetch_raw_data('http://www.thefreedictionary.com/quick') 
tree = html.fromstring(page)
parse_lemma(tree)
parse_rel(tree)
