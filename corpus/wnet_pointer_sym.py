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

# These pointer symbols are a modified version of what is available
# in https://wordnet.princeton.edu/wordnet/man/wninput.5WN.html

pointer_sym = {
	'noun': {
		'!': 'Antonym',
		'@': 'Hypernym',
		'@i': 'Instance Hypernym',
		' ~': 'Hyponym',
		' ~i': 'Instance Hyponym',
		'#m': 'Member holonym',
		'#s': 'Substance holonym',
		'#p': 'Part holonym',
		'%m': 'Member meronym',
		'%s': 'Substance meronym',
		'%p': 'Part meronym',
		'=': 'Attribute',
		'+': 'Derivationally related form',
		';': 'Domain',
		';c': 'Domain of synset - TOPIC',
		'-c': 'Member of this domain - TOPIC',
		';r': 'Domain of synset - REGION',
		'-r': 'Member of this domain - REGION',
		';u': 'Domain of synset - USAGE',
		'-u': 'Member of this domain - USAGE',
	},
	'verb': {
		'!': 'Antonym',
		'@': 'Hypernym',
		'~': 'Hyponym',
		'*': 'Entailment',
		'>': 'Cause',
		'^': 'Also see',
		'$': 'Verb Group',
		'+': 'Derivationally related form',
		';': 'Domain',
		';c': 'Domain of synset - TOPIC',
		';r': 'Domain of synset - REGION',
		';u': 'Domain of synset - USAGE',
	},
	'adjective': {
		'!': 'Antonym',
		'&': 'Similar to',
		'<': 'Participle of verb',
		'\\': 'Pertainym (pertains to noun)',
		'=': 'Attribute',
		'^': 'Also see',
		';': 'Domain',
		';c': 'Domain of synset - TOPIC',
		';r': 'Domain of synset - REGION',
		';u': 'Domain of synset - USAGE',
	},
	'adverb': {
		'!': 'Antonym',
		'\\': 'Derived from adjective',
		';': 'Domain',
		';c': 'Domain of synset - TOPIC',
		';r': 'Domain of synset - REGION',
		';u': 'Domain of synset - USAGE',
	},
}
