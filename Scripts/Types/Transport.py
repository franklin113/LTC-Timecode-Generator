
class Transport:
	def __init__(self):
		self._myOp = op.Transport
		self.buttons = {
			'stop': self._myOp.op('Buttons/stop'),
			'play': self._myOp.op('Buttons/play'),
			'pause': self._myOp.op('Buttons/pause')
		}

	def __getitem__(self, key):
		return self.buttons[key]
