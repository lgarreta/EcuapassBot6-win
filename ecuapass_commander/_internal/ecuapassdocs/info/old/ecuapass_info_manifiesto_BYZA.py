#!/usr/bin/env python3

import re, os, json, sys

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
	mainFields = ManifiestoInfo.extractEcuapassFields ()
	Utils.saveFields (mainFields, fieldsJsonFile, "Results")

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Manifiesto_BYZA (ManifiestoInfo):
	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		self.coordinatesFile = "coordinates_pdfs_docs_CODEBIN.json"
		super().__init__ (runningDir, empresa, pais, ecudocFields)

	def __str__(self):
		return f"{self.numero}"

	#-- For vehicles: None for BYZA
	def getCheckCertificado (self, type, key):
		if type == "REMOLQUE":
			return None
		else:
			return super().getCheckCertificado (type, key)

	#-- None for BYZA 
	def getCargaDescripcion (self):
			return None

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

