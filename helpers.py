class Variables(object):
	def __init__(self, data):
		for key in data:
			setattr(self, key, data[key])

class Types(object):
	def __init__(self, data):
		for key in data:
			setattr(self, key, Variables(data[key]) if isinstance(data[key], dict) else data[key])

class Parameters(object):
	def __init__(self, data):
		for key in data:
			setattr(self, key, Types(data[key]))
