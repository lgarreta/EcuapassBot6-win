#!/usr/bin/env python3
"""
Child class for cartaportes from ALDIA company
"""

import re, sys, os

from .ecuapass_info_cartaporte import CartaporteInfo
from .ecuapass_info_manifiesto import ManifiestoInfo
from .ecuapass_extractor import Extractor
from .resourceloader import ResourceLoader 
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
# Base class for SANCHEZPOLO's Cartaporte and Manifiesto
#----------------------------------------------------------
class SANCHEZPOLO :
	#-- Get text boxes coordinates from PDF file (uses external getPdfCoordinates)
	def getPdfCoordinates (self, pdfFilepath):
		return self.scrapingPdf.getPdfCoordinates (pdfFilepath)

	#-- Get MRN from special field ----------------------------------
	def getMRN (self):
		return Extractor.getMRNFromText (self.fields ["appMRN"])  # Special docField from appField

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Cartaporte_SANCHEZPOLO (SANCHEZPOLO, CartaporteInfo):
	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		CartaporteInfo.__init__ (self, runningDir, empresa, pais, ecudocFields)
		self.scrapingPdf = ScrapingPdf_SANCHEZPOLO_Cartaporte ()

	#-- Get doc number from docFields -------------------------------
	def getNumeroDocumento (self, docKey="00_Numero"):
		numero = None
		try:
			text      = self.fields [docKey]
			reNumeros = r"^(\S+).*?(\S+)$"
			match     = re.match (reNumeros, text)
			if match:
				numero  = match.group(2)
		except:
			Utils.printException ()
		return numero

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Manifiesto_SANCHEZPOLO (SANCHEZPOLO, ManifiestoInfo):
	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		ManifiestoInfo.__init__ (self, runningDir, empresa, pais, ecudocFields)
		self.scrapingPdf = ScrapingPdf_SANCHEZPOLO_Manifiesto ()

	#-- Aduana info: extract ciudad and pais for "cruce" and "destino" aduanas
	def getAduanaInfo (self):
		info = Utils.createEmptyDic (["paisCruce", "ciudadCruce", "paisDestino", "ciudadDestino"])
		text, ciudad, pais = "", "", ""
		try:
			aduanas = {}
			aduanas ["37_Aduana_Cruce"]   = {"ciudad":"ciudadCruce", "pais": "paisCruce"}
			aduanas ["38_Aduana_Destino"] = {"ciudad":"ciudadDestino", "pais": "paisDestino"}

			for key in ["37_Aduana_Cruce", "38_Aduana_Destino"]:
				text   = self.fields [key]
				ciudad = text.upper().strip ()
				for aduana in ["aduanas_ecuador", "aduanas_colombia", "aduanas_peru"]:
					aduanasPais = ResourceLoader.getEcuapassData (aduana)
					if ciudad in aduanasPais:
						ciudad, pais = ciudad, aduana.split ("_")[1].upper()
						info [aduanas [key]["ciudad"]] = ciudad if Utils.isValidText (ciudad) else "||LOW"
						info [aduanas [key]["pais"]]   = pais if Utils.isValidText (pais) else "||LOW"
						break
		except Exception as e:
			Utils.printException (f"Extrayendo pais-ciudad desde aduanas en texto: '{text}'", e)
		return info
