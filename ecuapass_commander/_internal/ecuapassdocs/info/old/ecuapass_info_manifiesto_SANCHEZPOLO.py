#!/usr/bin/env python3
"""
Child class for cartaportes from ALDIA company
"""

import re, sys, os
from .ecuapass_info_manifiesto import ManifiestoInfo
from .ecuapass_utils import Utils

from .scraping_pdf_SANCHEZPOLO import *

#----------------------------------------------------------
USAGE = "\
Extract information from document fields analized in AZURE\n\
USAGE: ecuapass_info_cartaportes.py <Json fields document>\n"
#----------------------------------------------------------
# Main
#----------------------------------------------------------
def main ():
	args = sys.argv
	docFieldsPath = args [1]
	runningDir = os.getcwd ()
	CartaporteInfo = CartaporteAldia (docFieldsPath, runningDir)
	mainFields = CartaporteInfo.extractEcuapassFields ()
	Utils.saveFields (mainFields, docFieldsPath, "Results")

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Manifiesto_SANCHEZPOLO (ManifiestoInfo):
	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		super().__init__ (runningDir, empresa, pais, ecudocFields)

	#-------------------------------------------------------------------
	# Get text boxes coordinates from PDF file (uses external getPdfCoordinates)
	#-------------------------------------------------------------------
	def getPdfCoordinates (self, pdfFilepath):
		scPdf = ScrapingPdf_SANCHEZPOLO_Manifiesto ()
		return scPdf.getPdfCoordinates (pdfFilepath)


