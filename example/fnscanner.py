def Mrs_to_Mr(data):
	import re
	return re.sub('Mrs\.', 'Mr.', data)

def expansion_nt(data):
	import re
	return re.sub('n\'t', 'not', data)

def exp(f, t):
    return f+t

def _ff(f):
    return f[1:-1]

def gg(f):
    return _ff(f)
