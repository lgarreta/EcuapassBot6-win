#!/usr/bin/env python3
"""
Child class for cartaportes from ALDIA company
"""

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
	docFieldsPath = args [1]
	runningDir = os.getcwd ()
	CartaporteInfo = Cartaporte_ALDIA (docFieldsPath, runningDir)
	mainFields = CartaporteInfo.extractEcuapassFields ()
	Utils.saveFields (mainFields, docFieldsPath, "Results")

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Cartaporte_ALDIA (CartaporteInfo):
	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		self.coordinatesFile = "coordinates_pdfs_docs_ALDIA.json"
		super().__init__ (runningDir, empresa, pais, ecudocFields)

	#------------------------------------------------------------------
	# No Instrucciones nor observacione
	#------------------------------------------------------------------
	def getInstruccionesObservaciones (self):
		instObs = {"instrucciones":None, "observaciones":None}
		return instObs
		
	#------------------------------------------------------------------
	#-- Return the document "pais" from docFields
	#------------------------------------------------------------------
	def getPaisDocumento (self):
		text = self.fields ["00a_Pais"]
		if "-CO-" in text:
			return "COLOMBIA"
		elif "-EC-" in text:
			return "ECUADOR"
		elif "-PE-" in text:
			return "PERU"
		else:
			print (f"+++ ERROR: Pais no identificado desde texto '{text}'")
			return None

	#------------------------------------------------------------
	# In ALDIA: Deposito in last line of field 21_Instrucciones
	#------------------------------------------------------------
	def getDepositoMercancia (self):
		try:
			text         = Utils.getValue (self.fields, "21_Instrucciones")
			lineDeposito = text.split ("\n")[-1]
			reBodega     = r':\s*(.*)'
			bodega       = Extractor.getValueRE (reBodega, lineDeposito)
			depositosDic = Extractor.getDataDic ("depositos_tulcan.txt", self.resourcesPath)
			for id, textBodega in depositosDic.items ():
				if bodega in textBodega:
					print (f"+++ Deposito '{id}' : '{textBodega}'")
					return id
			raise
		except:
			Utils.printx (f"+++ No se puedo obtener deposito desde texto '{text}'")
			return "||LOW"


	#-------------------------------------------------------------------
	# Get subject info: nombre, dir, pais, ciudad, id, idNro 
	# ALDIA format: <Nombre>\nID\n<Direccion>\n<CiudadPais>-
	#-------------------------------------------------------------------
	def getSubjectInfo (self, key):
		subject = {"nombre":"||LOW", "direccion":"||LOW", "pais": "||LOW", 
				   "ciudad":"||LOW", "tipoId":"||LOW", "numeroId": "||LOW"}
		try:
			text	   = Utils.getValue (self.fields, key)
			textLines  = text.split ("\n")

			# Case: 05_Notificado, 2 or 1 line
			if len (textLines) <= 2:
				subject = self.getSubjectInfoOneLine (subject, text)
				print (f"\n+++ Subject '{key}': '{subject}'")
				return subject

			subject ["nombre"]    = textLines [0]
			idInfo                = Extractor.getIdInfo (textLines [1])
			subject ["tipoId"]    = idInfo ["tipoId"]
			subject ["numeroId"]  = idInfo ["numeroId"]
			subject ["direccion"] = textLines [2]

			if key == "05_Notificado": # Take pais and direccion from "destinatario"
				subject ["pais"]      = self.ecudoc ["16_PaisDestinatario"]
				subject ["direccion"] = self.ecudoc ["20_DireccionDestinatario"]
			else:                      # Destinatario and Consignatario
				ciudad, pais          = Extractor.getCiudadPais (textLines [3], self.resourcesPath)
				subject ["ciudad"]    = Utils.checkLow (ciudad)
				subject ["pais"]      = Utils.checkLow (pais)
				# Add ciudad-pais to direccion
				ciudad, pais          = Extractor.getCiudadPais (textLines [3], self.resourcesPath, ECUAPASS=False)
				subject ["direccion"] = "%s. %s-%s" % (subject ["direccion"], Utils.toString (ciudad), Utils.toString (pais))

			print (f"\n+++ Subject '{key}': '{subject}'")
		except:
			Utils.printException (f"Obteniendo datos del sujeto: '{key}' en el texto: '{text}'")
		subject = Utils.checkLow (subject)
		return subject

	#-- When info is all in one line
	def getSubjectInfoOneLine (self, subject, text):
		text = text.replace ("\n","")
		text, tmpSubject = Extractor.removeSubjectId (text, subject, "05_Notificado")

		empresaTokens = ["S.A.S", "SAS", "S.A", "SA"]
		for token in empresaTokens:
			if token in text:
				index = text.index (token) + len (token)
				subject ["nombre"]    = text [:index] + "||LOW"
				subject ["direccion"] = text [index:] + "||LOW"
				subject ["pais"]    = Extractor.getPaisAndino (text) + "||LOW"
				return subject

		print (f"+++ No se pudo encontrar info subject desde texto de una linea: '{texto}'")
		return subject

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

