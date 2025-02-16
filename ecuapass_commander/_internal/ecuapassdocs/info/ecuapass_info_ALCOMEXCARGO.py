#!/usr/bin/env python3

import re, os, sys

from .ecuapass_info_cartaporte import CartaporteInfo
from .ecuapass_info_manifiesto import ManifiestoInfo
from .ecuapass_extractor import Extractor
from .ecuapass_data import EcuData
from .ecuapass_utils import Utils

#----------------------------------------------------------
USAGE = "\
Extract information from application documents (PDF or Web)\n\
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
class ALCOMEXCARGO:
	def __init__ (self):
		self.urlPrefix       = "alcomexcargo"   # byza.corebd.net
		self.coordinatesFile = "coordinates_pdfs_docs_CODEBIN.json"

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Cartaporte_ALCOMEXCARGO (ALCOMEXCARGO, CartaporteInfo):
	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		super().__init__()
		CartaporteInfo.__init__ (self, runningDir, empresa, pais, ecudocFields)

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Manifiesto_ALCOMEXCARGO (ALCOMEXCARGO, ManifiestoInfo):
	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		super().__init__()
		ManifiestoInfo.__init__ (self, runningDir, empresa, pais, ecudocFields)

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

