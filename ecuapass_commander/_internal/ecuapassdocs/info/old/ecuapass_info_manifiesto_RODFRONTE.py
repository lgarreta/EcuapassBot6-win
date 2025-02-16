#!/usr/bin/env python3

import os, sys
from .ecuapass_info_manifiesto import ManifiestoInfo
from .ecuapass_utils import Utils

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
class Manifiesto_RODFRONTE (ManifiestoInfo):
	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		self.coordinatesFile = "coordinates_pdfs_docs_CODEBIN.json"
		super().__init__ (runningDir, empresa, pais, ecudocFields)

	#------------------------------------------------------------------
	#-- get MRN according to empresa and docField
	#------------------------------------------------------------------
	def getMRN (self):
		text = self.fields ["29_Mercancia_Descripcion"]
		return text

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

