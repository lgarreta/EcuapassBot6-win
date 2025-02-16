#!/usr/bin/env python3

import os, sys

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
	mainFields = CartaporteInfo.extractEcuapassFields (fieldsJsonFile, runningDir)
	Utils.saveFields (mainFields, fieldsJsonFile, "Results")

#----------------------------------------------------------
# Base class for RODFRONTE's Cartaporte and Manifiesto
#----------------------------------------------------------
class RODFRONTE:
	def __init__ (self):
		self.urlPrefix       = "rodfronte"   # byza.corebd.net
		self.coordinatesFile = "coordinates_pdfs_docs_CODEBIN.json"

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Cartaporte_RODFRONTE (RODFRONTE, CartaporteInfo):
	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		super().__init__ ()
		CartaporteInfo.__init__ (self, runningDir, empresa, pais, ecudocFields)
		self.daysFechaEntrega = 0

	def getMRN (self):
		return Extractor.getMRNFromText (self.fields ["22_Observaciones"])

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Manifiesto_RODFRONTE (RODFRONTE, ManifiestoInfo):
	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		super().__init__ ()
		ManifiestoInfo.__init__ (self, runningDir, empresa, pais, ecudocFields)

	#-- get MRN according to empresa and docField
	def getMRN (self):
		return Extractor.getMRNFromText (self.fields ["29_Mercancia_Descripcion"])

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

