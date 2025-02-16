#!/usr/bin/env python3

import re, os, sys

from .ecuapass_info_cartaporte import CartaporteInfo
from .ecuapass_info_manifiesto import ManifiestoInfo
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
# Base class for SANCHEZPOLO's Cartaporte and Manifiesto
#----------------------------------------------------------
class RODFRONTE:
	def __init__ (self):
		self.urlPrefix       = "rodfronte"   # byza.corebd.net
		self.coordinatesFile = "coordinates_pdfs_docs_CODEBIN.json"

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Cartaporte_RODFRONTE (CartaporteInfo):
	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		self.coordinatesFile = "coordinates_pdfs_docs_CODEBIN.json"
		super().__init__ (runningDir, empresa, pais, ecudocFields)

	#------------------------------------------------------------------
	#-- get MRN according to empresa and docField
	#------------------------------------------------------------------
	def getMRN (self):
		text = self.fields ["22_Observaciones"]
		return text

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

