#!/usr/bin/env python3

#import re, os, json, sys
#from traceback import format_exc as traceback_format_exc
#from datetime import datetime, timedelta

import re, sys, os
from .ecuapass_info_cartaporte import CartaporteInfo
from .ecuapass_extractor import Extractor
from .ecuapass_data import EcuData
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
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Cartaporte_LOGITRANS (CartaporteInfo):
	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		self.coordinatesFile = "coordinates_pdfs_docs_CODEBIN.json"
		super().__init__ (runningDir, empresa, pais, ecudocFields)

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

	def getMRN (self):
		return Extractor.getMRNFromText (self.fields ["21_Instrucciones"])

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

