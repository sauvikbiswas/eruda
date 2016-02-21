import parser
from pprint import pprint as pp
x = parser.parser('LICENSE')
pp(x.parsed)
