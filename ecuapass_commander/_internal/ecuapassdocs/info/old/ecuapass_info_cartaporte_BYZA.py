#!/usr/bin/env python3

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
class Cartaporte_BYZA (CartaporteInfo):
	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		self.coordinatesFile = "coordinates_pdfs_docs_CODEBIN.json"
		super().__init__ (runningDir, empresa, pais, ecudocFields)

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

