#!/usr/bin/env python3

import re, os, json, sys
from traceback import format_exc as traceback_format_exc

from .ecuapass_info_manifiesto import ManifiestoInfo
from .ecuapass_data import EcuData
from .ecuapass_utils import Utils
from .ecuapass_extractor import Extractor  # Extracting basic info from text

#----------------------------------------------------------
USAGE = "\
Extract information from document fields analized in AZURE\n\
USAGE: ecuapass_info_manifiesto.py <Json fields document>\n"
#----------------------------------------------------------
def main ():
	args = sys.argv
	fieldsJsonFile = args [1]
	runningDir = os.getcwd ()
	mainFields = ManifiestoInfo.extractEcuapassFields (fieldsJsonFile, runningDir)
	Utils.saveFields (mainFields, fieldsJsonFile, "Results")

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Manifiesto_LOGITRANS (ManifiestoInfo):
	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		self.coordinatesFile = "coordinates_pdfs_docs_CODEBIN.json"
		super().__init__ (runningDir, empresa, pais, ecudocFields)

	def __str__(self):
		return f"{self.numero}"

	#-- Get tipo vehículo (VEHICULO/REMOLQUE) according to remolque info
	def getTipoVehiculo  (self, tipo, remolque):
		if tipo == "VEHICULO" and remolque ["placa"]:
			return "TRACTOCAMION"
		elif tipo == "VEHICULO" and not remolque ["placa"]:
			return "CAMION"                                                                                                                                                                                                                                              
		else:
			return None
	
#	#-- Try to convert certificado text to valid certificado string
#	#-- CR --> CRU
#	def formatCertificadoString (self, text, vehicleType):
#		certificadoString = super().formatCertificadoString (text, vehicleType)
#		certificadoString = certificadoString.replace ("CR-", "CRU-")
#		return certificadoString


	#-- None for BYZA 
	def getCargaDescripcion (self):
			return None

	#-----------------------------------------------------------
	#-- Search for embalaje in alternate ecufield 11
	#-----------------------------------------------------------
	def getBultosInfoManifiesto (self):
		bultosInfo = super ().getBultosInfoManifiesto ()

		if not bultosInfo ["embalaje"] or bultosInfo ["embalaje"] == "||LOW":
			text = self.fields ["31_Mercancia_Embalaje"]["value"]
			embalaje = Extractor.getTipoEmbalaje ("00 " + text)
			bultosInfo ["embalaje"] = embalaje
			bultosInfo ["marcas"] = "S/M" if embalaje else text
		return bultosInfo

	#-----------------------------------------------------------
	# Remove "DIAN" or "SENAE" from aduana text and call super
	#-----------------------------------------------------------
	def getAduanaInfo (self):
		def replacePrefix (text):
			text = text.replace ("DIAN", "IPIALES")
			text = text.replace ("SENAE", "TULCAN")
			return text

		self.fields ["37_Aduana_Cruce"]   = replacePrefix (self.fields ["37_Aduana_Cruce"])
		self.fields ["38_Aduana_Destino"] = replacePrefix (self.fields ["38_Aduana_Destino"])

		return super().getAduanaInfo ()

	def getMRN (self):
		return Extractor.getMRNFromText (self.fields ["29_Mercancia_Descripcion"])

	#-----------------------------------------------------------
	# Get info of container (id, tipo)
	#-----------------------------------------------------------
#	def getContenedorIdTipo (self, text):
#		try:
#			match = re.search (r'(\w*)\s+"(\d*)"', text)
#			id   = match.group (1)
#			type = match.group (2)
#			return id, type
#		except:
#			Utils.printx ("No se pudo obtener info de contenedor en texto:", text)
#			Utils.printException ()
#			return None, None

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

