#!/usr/bin/env python3

#import re, os, json, sys
#from traceback import format_exc as traceback_format_exc
#from datetime import datetime, timedelta

import re, sys, os
from .ecuapass_info_cartaporte import CartaporteInfo
from .ecuapass_info_manifiesto import ManifiestoInfo
from .ecuapass_extractor import Extractor
from .ecuapass_utils import Utils

#----------------------------------------------------------
USAGE = "\
Extract information from document fields analized in AZURE\n\
USAGE: ecuapass_info_cartaportes.py <Json fields document>\n"
#----------------------------------------------------------
# Main
#----------------------------------------------------------
def main ():
	args = sys.argv
	fieldsJsonFile = args [1]
	runningDir = os.getcwd ()
	CartaporteInfo = CartaporteByza (fieldsJsonFile, runningDir)
	mainFields = CartaporteInfo.extractEcuapassFields ()
	Utils.saveFields (mainFields, fieldsJsonFile, "Results")

#----------------------------------------------------------
# Base class for RODFRONTE's Cartaporte and Manifiesto
#----------------------------------------------------------
class LOGITRANS:
	def __init__ (self):
		self.urlPrefix       = "logitrans"   # logitrans.corebd.net
		self.coordinatesFile = "coordinates_pdfs_docs_CODEBIN.json"

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Cartaporte_LOGITRANS (LOGITRANS, CartaporteInfo):
	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		super().__init__()
		CartaporteInfo.__init__ (self, runningDir, empresa, pais, ecudocFields)

	#-----------------------------------------------------------
	#-- Search for embalaje in alternate ecufield 11
	#-----------------------------------------------------------
	def getBultosInfoCartaporte (self, analysisType="BOT"):
		bultosInfo = super ().getBultosInfoCartaporte ()
		print ("+++ bultosInfo:", bultosInfo)

		if not bultosInfo ["embalaje"] or bultosInfo ["embalaje"] == "||LOW":
			text = self.fields ["11_MarcasNumeros_Bultos"]["value"]
			embalaje = Extractor.getTipoEmbalaje ("00 " + text)
			bultosInfo ["embalaje"] = embalaje
			bultosInfo ["marcas"] = "S/M" if embalaje else text
		return bultosInfo

	#-----------------------------------------------------------
	#-----------------------------------------------------------
	def getMRN (self):
		return Extractor.getMRNFromText (self.fields ["21_Instrucciones"])

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Manifiesto_LOGITRANS (LOGITRANS, ManifiestoInfo):
	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		super().__init__()
		ManifiestoInfo.__init__ (self, runningDir, empresa, pais, ecudocFields)

	def __str__(self):
		return f"{self.numero}"

	#-----------------------------------------------------------
	#-----------------------------------------------------------
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

	#-----------------------------------------------------------
	#-----------------------------------------------------------
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

