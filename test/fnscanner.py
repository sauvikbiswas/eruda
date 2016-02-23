def Mrs_to_Mr(data):
	import re
	return re.sub('Mrs\.', 'Mr.', data)

def expansion_nt(data):
	import re
	return re.sub('n\'t', 'not', data)
