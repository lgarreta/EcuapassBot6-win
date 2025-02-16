#!/usr/bin/env python3

import re, os, sys

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
	mainFields = CartaporteInfo.extractEcuapassFields (fieldsJsonFile, runningDir)
	Utils.saveFields (mainFields, fieldsJsonFile, "Results")

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class CartaporteALCOMEXCARGO (CartaporteInfo):
	def __init__ (self, fieldsJsonFile, runningDir, empresa, pais, ecudocFields=None):
		super().__init__ (fieldsJsonFile, runningDir, empresa, pais, ecudocFields)

	#------------------------------------------------------------------
	#-- get MRN according to empresa and docField
	#------------------------------------------------------------------
	def getMRN (self):
		text = Utils.getValue (self.fields, "22_Observaciones")
		return text

#	#-----------------------------------------------------------
#	#-- Get 'total bultos' and 'tipo embalaje' -----------------
#	#-----------------------------------------------------------
#	def getBultosInfo (self):
#		print ("+++ DEBUG: getBultosInfo: ")
#		bultosInfo = super ().getBultosInfo ()
#		try:
#			# Embalaje
#			text = self.fields ["11_MarcasNumeros_Bultos"]["value"]
#			print ("+++ DEBUG: getBultosInfo: text: ", text)
#			bultosInfo ["embalaje"] = Extractor.getTipoEmbalaje (text)
#		except:
#			Utils.printException ("Obteniendo información de 'Embalaje'", text)
#
#		return bultosInfo

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

