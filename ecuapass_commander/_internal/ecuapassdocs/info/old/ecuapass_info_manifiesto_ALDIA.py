#!/usr/bin/env python3

import os, sys, re, json

from .ecuapass_info_manifiesto import ManifiestoInfo
from .ecuapass_data import EcuData
from .ecuapass_utils import Utils
from .ecuapass_extractor import Extractor  # Extracting basic info from text

#----------------------------------------------------------
USAGE = "\
Extract information from document fields analized in AZURE\n\
USAGE: ecuapass_info_manifiesto.py <Json fields document>\n"
#----------------------------------------------------------
def main ():
	args = sys.argv
	docFieldsPath = args [1]
	runningDir = os.getcwd ()
	mainFields = ManifiestoInfo.extractEcuapassFields (docFieldsPath, runningDir)
	Utils.saveFields (mainFields, docFieldsPath, "Results")

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class Manifiesto_ALDIA (ManifiestoInfo):
	def __init__(self, runningDir, empresa, pais):
		self.coordinatesFile = "coordinates_pdfs_docs_ALDIA.json"
		super().__init__ (runningDir, empresa, pais)

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

#	#------------------------------------------------------------------
#	# Permisos info: Overwritten in subclasses
#	#------------------------------------------------------------------
#	def getPermisosInfo (self):
#		originario = self.fields ["02_Permiso_Originario"]
#		servicios  = None
#
#		permisos = {"tipoPermisoCI"    : "1" if originario.startswith ("CI") else None,
#			        "tipoPermisoPEOTP" : "1" if originario.startswith ("PE") else None,
#			        "tipoPermisoPO"    : "1" if originario.startswith ("PO") else None,
#			        "permisoOriginario": originario,
#			        "permisoServicios1": servicios
#		}
#		return permisos

	#------------------------------------------------------------------
	# ALDIA: Cabezote: XXXX - YYYY    Trailer: WWWW - ZZZZZ
	# Get four certificado strings
	#------------------------------------------------------------------
	def getCheckCertificado (self, vehicleType, key):
		# Non needed for ALDIA
		if vehicleType == "REMOLQUE":
			return None

		#-- XXXX-YYYY or YYYY-XXXX In ALDIA subempresas
		def getCertificadoString (valuesList):
			if any ([x in valuesList [0] for x in ["CH", "CR"]]):
				return valuesList [0]
			elif any ([x in valuesList [1] for x in ["CH", "CR"]]):
				return valuesList [1]
			else:
				return None
		#---------------------------------------------------
		text    = self.fields [key]
		print (f"+++ textCertificado '{text}'")

		labels  = {"VEHICULO":"Cabezote", "REMOLQUE":"Trailer"}
		label   = labels [vehicleType]
		matches = re.search (rf"{label}:\s*([\w-]+)?\s*([\w-]+)?", text)
		strings = [matches.group(i) if matches and matches.group(i) else None for i in range(1, 3)]
		certStr = getCertificadoString (strings)

		certificado  = super().formatCertificadoString (certStr, vehicleType)
		certChecked  = self.checkCertificado (certificado, vehicleType)

		print (f"+++ Certificado '{vehicleType} : '{certChecked}'")
		return certChecked

	#----------------------------------------------------------------
	# Check if certificate string is in correct format
	#----------------------------------------------------------------
	def checkCertificado (self, certificadoString, vehicleType):
		try:
			if vehicleType == "VEHICULO":
				pattern = re.compile (r'^CH-(CO|EC)-\d{4,5}-\d{2}')
			elif vehicleType == "REMOLQUE":
				pattern = re.compile (r'^(CRU|CR)-(CO|EC)-\d{4,5}-\d{2}')

			if (certificadoString == None): 
				return "||LOW" if vehicleType == "VEHICULO" else None

			if bool (pattern.match (certificadoString)) == False:
				Utils.printx (f"Error validando certificado de <{vehicleType}> en texto: '{certificadoString}'")
				certificadoString = "||LOW"
		except:
			Utils.printException (f"Obteniendo/Verificando certificado '{certificadoString}' para '{vehicleType}'")

		return certificadoString;

	#-----------------------------------------------------------
	#-- Search for embalaje in alternate ecufield 11
	#-----------------------------------------------------------
	def getBultosInfoManifiesto (self):
		mercancia = super ().getBultosInfoManifiesto ()
		print (f"+++ mercancia parcial: '{mercancia}'")

		# Cantidad en Cantidad
		mercancia ["cantidad"] = Extractor.getNumber (self.fields ["30_Mercancia_Bultos"])
		text                   = self.fields ["31_Mercancia_Embalaje"]
		mercancia ["embalaje"] = Extractor.getTipoEmbalaje (self.fields ["31_Mercancia_Embalaje"])

		print (f"+++ Mercancia '{mercancia}'")
		return mercancia

	#-- Get marcas from cartaporte JSON file
	def getMarcasText (self, marcasField=None):
		cpiMarcas = "||LOW"
		try:
			cpiNumber      = self.fields ["28_Mercancia_Cartaporte"]
			cpiDocFilepath = os.path.dirname (self.docFieldsPath)
			cpiFilename    = os.path.join (cpiDocFilepath, f"CPI-{cpiNumber}-DOCFIELDS.json")
			print (f"+++ cpiFilename for marcas '{cpiFilename}'")

			cpiDocFields = json.load (open (cpiFilename, encoding="utf-8"))
			cpiMarcas    = cpiDocFields ["11_MarcasNumeros_Bultos"]
		except:
			Utils.printException ("Obteniendo marcas desde cartaporte")

		return cpiMarcas


	#-- Get Carga Tipo from docFiels 25_CargaTipo
	def getTipoCarga (self):
		cargaTipo = None
		try:
			text = self.fields ["25_Carga_Tipo"].upper ()
			if  "NORMAL" in text or "SUELTA" in text:
				return "CARGA SUELTA"
			elif "GENERAL" in text:
				return "CARGA GENERAL"
			elif "CONTENERIZADA" in text:
				return "CARGA CONTENERIZADA"
			elif "GRANEL" in text:
				return "CARGA A GRANEL"
		except:
			Utils.printException ("Obteniendo Tipo de Carga")
		return cargaTipo

	#-- Get info of container (id, tipo)
#	def getContenedorIdTipo (self, text):
#		match = re.search(r'([A-Z]{4}[-\s]*\d{6,7}[-\s]*\d)?([\s]*\w+)?\s*DE\s*(\d+)\s*PIES', text)
#		match = re.search(r'([A-Z]{4}[-\s]*\d{6,7}[-\s]*\d)?([\s]*\w+)?\s*DE\s*(\d+)\s*PIES', text)
#		if match:
#			initial_string = match.group(1).replace("-", "").replace(" ", "")
#			number = match.group(3)
#			return initial_string, number
#		return None, None
#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

