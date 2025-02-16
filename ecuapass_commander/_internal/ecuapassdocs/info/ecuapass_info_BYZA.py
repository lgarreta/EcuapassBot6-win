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
	CartaporteInfo = CartaporteByza (fieldsJsonFile, runningDir)
	mainFields = CartaporteInfo.extractEcuapassFields ()
	Utils.saveFields (mainFields, fieldsJsonFile, "Results")

#----------------------------------------------------------
# Base class for RODFRONTE's Cartaporte and Manifiesto
#----------------------------------------------------------
class BYZA:
	def __init__ (self):
		self.urlPrefix       = "byza"   # byza.corebd.net
		self.coordinatesFile = "coordinates_pdfs_docs_CODEBIN.json"

#----------------------------------------------------------
# Cartaporte Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Cartaporte_BYZA (BYZA, CartaporteInfo):
	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		super().__init__()
		CartaporteInfo.__init__ (self, runningDir, empresa, pais, ecudocFields)
		self.daysFechaEntrega = 14

	def getMRN (self):
		return Extractor.getMRNFromText (self.fields ["12_Descripcion_Bultos"])

	#-----------------------------------------------------------
	#-- Get instrucciones y observaciones ----------------------
	#-----------------------------------------------------------
	def getInstruccionesObservaciones (self):
		instObs = {"instrucciones":None, "observaciones":None}
		return instObs

#----------------------------------------------------------
# Manifiesto Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Manifiesto_BYZA (BYZA, ManifiestoInfo):
	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		super().__init__()
		ManifiestoInfo.__init__ (self, runningDir, empresa, pais, ecudocFields)

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

	def getMRN (self):
		return Extractor.getMRNFromText (self.fields ["29_Mercancia_Descripcion"])
#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

