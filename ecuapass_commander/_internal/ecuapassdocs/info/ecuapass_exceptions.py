
#-----------------------------------------------------------
# Custom Ecupasssdocs exceptions
#-----------------------------------------------------------
class EcudocException (Exception):
	pass

class EcudocWebException (EcudocException):
	pass

class EcudocDocumentNotFoundException (EcudocException):
	pass

class EcudocConnectionNotOpenException (EcudocException):
	defaultMessage = "No se pudo conectar a CODEBIN"

	def __init__(self, message=None):
		self.message = message or self.defaultMessage

class EcudocBotStopException (EcudocException):
	pass

class EcudocBotCartaporteNotFound (EcudocException):
	pass

class EcudocEcuapassException (EcudocException):
	pass

class EcudocExtractionException (EcudocException):
	pass

class EcudocDocumentNotValidException (EcudocException):
	pass

class EcudocDocumentNotValidException (EcudocException):
	pass

class IllegalEmpresaException (EcudocException):
	pass

class EcudocCloudException (EcudocException):
	pass
