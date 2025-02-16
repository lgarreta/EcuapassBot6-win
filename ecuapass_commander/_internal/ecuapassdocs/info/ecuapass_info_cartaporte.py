#!/usr/bin/env python3

import re, os, json, sys, locale
from datetime import datetime, timedelta

from .ecuapass_info import EcuInfo
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
	mainFields = CartaporteInfo.extractEcuapassFields (fieldsJsonFile, runningDir)
	Utils.saveFields (mainFields, fieldsJsonFile, "Results")

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class CartaporteInfo (EcuInfo):

	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		super().__init__ ("CARTAPORTE", runningDir, empresa, pais, ecudocFields)
		self.daysFechaEntrega = 7

	#-- Get data and value from document main fields"""
	def extractEcuapassFields (self, docFieldsPath, analysisType="BOT"):
		#--------------------------------------------------------------
		print ("\n>>>>>> Carta de Porte Internacional por Carretera <<<")
		#--------------------------------------------------------------
		self.ecudoc ["01_Distrito"]	         = self.getDistrito ()
		self.ecudoc ["02_NumeroCPIC"]        = self.getNumeroDocumento ()
		self.ecudoc ["03_MRN"]               = self.getMRN ()
		self.ecudoc ["04_MSN"]               = self.getMSN () 
		self.ecudoc ["05_TipoProcedimiento"] = self.getTipoProcedimiento ()

		#-- Empresa
		self.ecudoc ["06_EmpresaTransporte"] = self.getNombreEmpresa ()
		self.ecudoc ["07_DepositoMercancia"] = self.getDepositoMercancia ()
		self.ecudoc ["08_DirTransportista"]	 = self.getDireccionEmpresa ()
		self.ecudoc ["09_NroIdentificacion"] = self.getIdNumeroEmpresa ()

		#--------------------------------------------------------------
		# print ("\n>>>>>> Datos Generales de la CPIC: Sujetos <<<<<<<<")
		#--------------------------------------------------------------
		#-- Remitente 
		remitente                             = Utils.checkLow (self.getSubjectInfo ("02_Remitente"))
		self.ecudoc ["10_PaisRemitente"]      = remitente ["pais"]
		self.ecudoc ["11_TipoIdRemitente"]    = remitente ["tipoId"]
		self.ecudoc ["12_NroIdRemitente"]     = remitente ["numeroId"]
		self.ecudoc ["13_NroCertSanitario"]	  = None
		self.ecudoc ["14_NombreRemitente"]    = remitente ["nombre"]
		self.ecudoc ["15_DireccionRemitente"] = remitente ["direccion"]

		#-- Destinatario 
		destinatario                             = Utils.checkLow (self.getSubjectInfo ("03_Destinatario"))
		self.ecudoc ["16_PaisDestinatario"]	     = destinatario ["pais"] 
		self.ecudoc ["17_TipoIdDestinatario"]    = destinatario ["tipoId"] 
		self.ecudoc ["18_NroIdDestinatario"]     = destinatario ["numeroId"] 
		self.ecudoc ["19_NombreDestinatario"]    = destinatario ["nombre"] 
		self.ecudoc ["20_DireccionDestinatario"] = destinatario ["direccion"] 

		#-- Consignatario 
		consignatario                             = Utils.checkLow (self.getSubjectInfo ("04_Consignatario"))
		self.ecudoc ["21_PaisConsignatario"]      = consignatario ["pais"] 
		self.ecudoc ["22_TipoIdConsignatario"]    = consignatario ["tipoId"] 
		self.ecudoc ["23_NroIdConsignatario"]     = consignatario ["numeroId"] 
		self.ecudoc ["24_NombreConsignatario"]    = consignatario ["nombre"] 
		self.ecudoc ["25_DireccionConsignatario"] = consignatario ["direccion"] 

		#-- Notificado 
		notificado                                = self.getSubjectInfo ("05_Notificado")
		self.ecudoc ["26_NombreNotificado"]	      = notificado ["nombre"] 
		self.ecudoc ["27_DireccionNotificado"]    = notificado ["direccion"] 
		self.ecudoc ["28_PaisNotificado"]         = notificado ["pais"] 

		#--------------------------------------------------------------
		# print ("\n>>>>>> Datos Generales de la CPIC: Locaciones <<<<<<<<")
		#--------------------------------------------------------------
		#-- Recepcion 
		recepcion                           = self.getLocationInfo ("06_Recepcion")
		self.ecudoc ["29_PaisRecepcion"]    = recepcion ["pais"] 
		self.ecudoc ["30_CiudadRecepcion"]  = recepcion ["ciudad"] 
		self.ecudoc ["31_FechaRecepcion"]   = recepcion ["fecha"] 

		#-- Embarque location box
		embarque                           = self.getLocationInfo ("07_Embarque")
		self.ecudoc ["32_PaisEmbarque"]    = embarque ["pais"] 
		self.ecudoc ["33_CiudadEmbarque"]  = embarque ["ciudad"] 
		self.ecudoc ["34_FechaEmbarque"]   = embarque ["fecha"] 

		#-- Entrega location box
		entrega	                          = self.getLocationInfo ("08_Entrega")
		self.ecudoc ["35_PaisEntrega"]    = entrega ["pais"] 
		self.ecudoc ["36_CiudadEntrega"]  = entrega ["ciudad"] 
		self.ecudoc ["37_FechaEntrega"]   = entrega ["fecha"] 

		#--------------------------------------------------------------
		# print ("\n>>>>>> Datos Generales de la CPIC: Condiciones <<<<<<<<")
		#--------------------------------------------------------------
		condiciones                              = Utils.checkLow (self.getCondiciones ())
		self.ecudoc ["38_CondicionesTransporte"] = condiciones ["transporte"]
		self.ecudoc ["39_CondicionesPago"]       = condiciones ["pago"]

		unidades                       = self.getUnidadesMedidaInfo ()
		bultosInfo                     = self.getBultosInfoCartaporte (analysisType)
		self.ecudoc ["40_PesoNeto"]	   = unidades ["pesoNeto"]
		self.ecudoc ["41_PesoBruto"]   = unidades ["pesoBruto"]
		self.ecudoc ["42_TotalBultos"] = bultosInfo ["cantidad"]
		self.ecudoc ["43_Volumen"]	   = unidades ["volumen"]
		self.ecudoc ["44_OtraUnidad"]  = unidades ["otraUnidad"]

		# Gastos
		gastos                                     = self.getGastosInfo ()
		self.ecudoc ["50_GastosRemitente"]         = gastos ["fleteRemi"] 
		self.ecudoc ["51_MonedaRemitente"]	       = gastos ["monedaRemi"] 
		self.ecudoc ["52_GastosDestinatario"]      = gastos ["fleteDest"] 
		self.ecudoc ["53_MonedaDestinatario"]      = gastos ["monedaDest"] 
		self.ecudoc ["54_OtrosGastosRemitente"]    = gastos ["otrosRemi"] 
		self.ecudoc ["55_OtrosMonedaRemitente"]    = gastos ["otrosRemiMoneda"] 
		self.ecudoc ["56_OtrosGastosDestinatario"] = gastos ["otrosDest"] 
		self.ecudoc ["57_OtrosMonedaDestinataio"]  = gastos ["otrosDestMoneda"] 
		self.ecudoc ["58_TotalRemitente"]          = gastos ["totalRemi"] 
		self.ecudoc ["59_TotalDestinatario"]       = gastos ["totalDest"] 

		# Documentos remitente
		self.ecudoc ["60_DocsRemitente"]   = self.getDocsRemitente ()

		# Emision location box
		emision	                           = self.getLocationInfo ("19_Emision")
		self.ecudoc ["61_FechaEmision"]    = emision ["fecha"] 
		self.ecudoc ["62_PaisEmision"]     = emision ["pais"] 
		self.ecudoc ["63_CiudadEmision"]   = emision ["ciudad"] 
		
		# Incoterm
		text                                = self.fields ["16_Incoterms"]
		incoterms                           = self.getIncotermInfo (text)
		self.ecudoc ["45_PrecioMercancias"]	= incoterms ["precio"]
		self.ecudoc ["46_INCOTERM"]	        = incoterms ["incoterm"] 
		self.ecudoc ["47_TipoMoneda"]       = incoterms ["moneda"] 
		self.ecudoc ["48_PaisMercancia"]    = incoterms ["pais"] 
		self.ecudoc ["49_CiudadMercancia"]	= incoterms ["ciudad"] 

		# Instrucciones y Observaciones
		instObs	                           = self.getInstruccionesObservaciones ()
		self.ecudoc ["64_Instrucciones"]   = instObs ["instrucciones"]
		self.ecudoc ["65_Observaciones"]   = instObs ["observaciones"]
		#self.ecudoc ["64_Instrucciones"]   = None
		#self.ecudoc ["65_Observaciones"]   = None

		# Detalles
		self.ecudoc ["66_Secuencia"]      = "1"
		self.ecudoc ["67_TotalBultos"]    = self.ecudoc ["42_TotalBultos"]
		self.ecudoc ["68_Embalaje"]       = bultosInfo ["embalaje"]
		self.ecudoc ["69_Marcas"]         = bultosInfo ["marcas"]
		self.ecudoc ["70_PesoNeto"]	      = self.ecudoc ["40_PesoNeto"]
		self.ecudoc ["71_PesoBruto"]      = self.ecudoc ["41_PesoBruto"]
		self.ecudoc ["72_Volumen"]	      = self.ecudoc ["43_Volumen"]
		self.ecudoc ["73_OtraUnidad"]     = self.ecudoc ["44_OtraUnidad"]

		# IMOs
		self.ecudoc ["74_Subpartida"]       = None
		self.ecudoc ["75_IMO1"]             = None
		self.ecudoc ["76_IMO2"]             = None
		self.ecudoc ["77_IMO2"]             = None
		self.ecudoc ["78_NroCertSanitario"] = self.ecudoc ["13_NroCertSanitario"]
		self.ecudoc ["79_DescripcionCarga"] = bultosInfo ["descripcion"]

		# Update fields depending of other fields (or depending of # "empresa")
		self.updateExtractedEcuapassFields ()

		return (self.ecudoc)
	
	#------------------------------------------------------------------
	# Return ecudoc field keys containing ciudad,pais 
	#------------------------------------------------------------------
	def getCiudadPaisKeys (self):
		ciudadPaisKeys = [
				("30_CiudadRecepcion", "29_PaisRecepcion"),
				("33_CiudadEmbarque", "32_PaisEmbarque"),
				("36_CiudadEntrega", "35_PaisEntrega"),
				("63_CiudadEmision", "62_PaisEmision")]
		return ciudadPaisKeys
			
	#------------------------------------------------------------------
	#-- First level functions for each Ecuapass field
	#------------------------------------------------------------------
	def getMSN (self):
		return "0001||LOW"

	#------------------------------------------------------------
	# Return the code number from the text matching a "deposito"
	#-- BOTERO-SOTO en casilla 21 o 22, NTA en la 22 ------------
	#------------------------------------------------------------
	def getDepositoMercancia (self):
		for casilla in ["21_Instrucciones", "22_Observaciones"]:
			text = ""
			try:
				text        = Utils.getValue (self.fields, casilla)
				reWordSep  = r'\s+(?:EL\s+)?'
				#reBodega    = rf'BODEGA[S]?\s+\b(\w*)\b'
				reBodega    = rf'BODEGA[S]?{reWordSep}\b(\w*)\b'
				bodegaText  = Extractor.getValueRE (reBodega, text)
				if bodegaText != None:
					Utils.printx (f"Extrayendo código para el deposito '{bodegaText}'")
					depositosDic = Extractor.getDataDic ("depositos_tulcan.txt", self.resourcesPath)
					
					for id in depositosDic:
						if bodegaText in depositosDic [id]:
							return id
			except:
				Utils.printException (f"Obteniendo bodega desde texto '{text}'")
		return "||LOW"

	#-------------------------------------------------------------------
	#-- Get location info: ciudad, pais, fecha -------------------------
	#-- Boxes: Recepcion, Embarque, Entrega ----------------------------
	#-------------------------------------------------------------------
	def getLocationInfo (self, key):
		text     = self.fields [key]
		location = Extractor.extractLocationDate (text, self.resourcesPath, key)
		print (f"+++ Location/Date text for '{key}': '{location}'")
		if key == "08_Entrega" and location ["fecha"] == "||LOW":
			location ["fecha"] = self.getFechaEntrega (location["fecha"])

		print (f"+++ Location/Date info for '{key}': '{location}'")
		return (location)

	#-- Called when update extracted fields
	#-- Add one or tww weeks to 'entrega' from 'embarque' date
	def getFechaEntrega (self, fechaEntrega=None):
		try:
			if fechaEntrega == "||LOW" or fechaEntrega is None:
				fechaEmbarque = self.ecudoc ["34_FechaEmbarque"]
				fechaEmbarque = datetime.strptime (fechaEmbarque, "%d-%m-%Y") # Fecha igual a la de Embarque
				fechaEntrega  = fechaEmbarque + timedelta (days=self.daysFechaEntrega)

				if self.getTipoProcedimiento () == "TRANSITO":
					fechaEntrega = fechaEmbarque + timedelta (days=2*self.daysFechaEntrega)

				fechaEntrega = fechaEntrega.strftime ("%d-%m-%Y") + "||LOW"
				return fechaEntrega
		except:
			Utils.printException ("Obteniendo información de Fecha de entrega")

		return fechaEntrega

	#-----------------------------------------------------------
	# Get "transporte" and "pago" conditions
	#-----------------------------------------------------------
	def getCondiciones (self):
		conditions = {'pago':None, 'transporte':None}
		# Condiciones transporte
		text = self.fields ["09_Condiciones"].upper ()
		try:
			if "SIN CAMBIO" in text or "SIN TRASBORDO" in text:
				conditions ["transporte"] = "DIRECTO, SIN CAMBIO DEL CAMION"
			elif "CON CAMBIO" in text or "CON TRASBORDO" in text:
				conditions ["transporte"] = "DIRECTO, CON CAMBIO DEL TRACTO-CAMION"
			elif "TRANSBORDO" in text or "TRASBORDO" in text: 
				conditions ["transporte"] = "TRANSBORDO"
		except:
			Utils.printException ("Extrayendo condiciones de transporte en texto", text)

		# Condiciones pago
		try:
			if "CREDITO" in text:
				conditions ["pago"] = "POR COBRAR||LOW"
			elif "ANTICIPADO" in text:
				conditions ["pago"] = "PAGO ANTICIPADO||LOW"
			elif "CONTADO" in text:
				conditions ["pago"] = "PAGO ANTICIPADO||LOW"
			else:
				pagoString = Extractor.getDataString ("condiciones_pago.txt", self.resourcesPath)
				rePagos    = rf"\b({pagoString})\b" # RE to find a match string
				pago       = Extractor.getValueRE (rePagos, text)
				conditions ["pago"] = pago if pago else "POR COBRAR||LOW"
		except:
			Utils.printException ("Extrayendo condiciones de pago en texto:", text)

		print (f"+++ Condiciones Pago/Transporte '{conditions}'")
		return (conditions)

	#-----------------------------------------------------------
	# Get info from unidades de medida:"peso neto, volumente, otras
	#-----------------------------------------------------------
	def getUnidadesMedidaInfo (self):
		unidades = {"pesoNeto":None, "pesoBruto": None, "volumen":None, "otraUnidad":None}
		try:
			unidades ["pesoNeto"]   = Utils.checkQuantity (Extractor.getNumber (self.fields ["13a_Peso_Neto"]))
			unidades ["pesoBruto"]  = Utils.checkQuantity (Extractor.getNumber (self.fields ["13b_Peso_Bruto"]))
			unidades ["volumen"]    = Utils.checkQuantity (Extractor.getNumber (self.fields ["14_Volumen"]))
			unidades ["otraUnidad"] = Utils.checkQuantity (Extractor.getNumber (self.fields ["15_Otras_Unidades"]))

			#for k,value in unidades.items():
			#	unidades [k] = "" if not value else Utils.stringToAmericanFormat (value)

			print (f"+++ Unidades de Medida: '{unidades}'")
		except:
			Utils.printException ("Obteniendo información de 'Unidades de Medida'")
		return unidades

	#-----------------------------------------------------------
	# Get 'total bultos' and 'tipo embalaje' 
	# Uses base function "getBultosInfo" with cartaporte fields
	#-----------------------------------------------------------
	def getBultosInfoCartaporte (self, analysisType="BOT"):
		ecuFieldsCartaporte = {"cantidad": "10_CantidadClase_Bultos", "marcas":
			   "11_MarcasNumeros_Bultos", "descripcion": "12_Descripcion_Bultos"}

		bultosInfo = self.getBultosInfo (ecuFieldsCartaporte, analysisType)
		print (f"+++ Mercancia info '{bultosInfo}'")
		return bultosInfo

	#--------------------------------------------------------------------
	#-- Search "pais" for "ciudad" in previous document boxes
	#--------------------------------------------------------------------
	def searchPaisPreviousBoxes (self, ciudad, pais):
		try:
			# Search 'pais' in previos boxes
			if (ciudad != None and pais == None):
				if self.ecudoc ["30_CiudadRecepcion"] and ciudad in self.ecudoc ["30_CiudadRecepcion"]:
					pais = self.ecudoc ["29_PaisRecepcion"]
				elif self.ecudoc ["33_CiudadEmbarque"] and ciudad in self.ecudoc ["33_CiudadEmbarque"]:
					pais = self.ecudoc ["32_PaisEmbarque"]
				elif self.ecudoc ["36_CiudadEntrega"] and ciudad in self.ecudoc ["36_CiudadEntrega"]:
					pais = self.ecudoc ["35_PaisEntrega"]

		except:
			Utils.printException ("Obteniendo informacion de 'mercancía'")
		return ciudad, pais

	#-----------------------------------------------------------
	# Get info from 'documentos recibidos remitente'
	#-----------------------------------------------------------
	def getDocsRemitente (self):
		docs = None
		try:
			docs = self.fields ["18_Documentos"]
			print (f"+++ Documentos info: '{docs}'")
		except:
			Utils.printException("Obteniendo valores 'DocsRemitente'")
		return docs

	#-----------------------------------------------------------
	#-- Get instrucciones y observaciones ----------------------
	#-----------------------------------------------------------
	def getInstruccionesObservaciones (self):
		instObs = {"instrucciones":None, "observaciones":None}
		try:
			instObs ["instrucciones"] = self.fields ["21_Instrucciones"]
			instObs ["observaciones"] = self.fields ["22_Observaciones"]
			print (f"+++ 21: Instrucciones info: {instObs['instrucciones']}")
			print (f"+++ 22: Observaciones info: {instObs['observaciones']}")
		except:
			Utils.printException ("Obteniendo informacion de 'Instrucciones y Observaciones'")
		return instObs

	#-----------------------------------------------------------
	# Get 'gastos' info: monto, moneda, otros gastos
	#-----------------------------------------------------------
	def getGastosInfo (self):
		gastos = {"fleteRemi":None, "monedaRemi":None,       "fleteDest":None,       "monedaDest":None,
			"otrosRemi":None, "otrosRemiMoneda":None, "otrosDest":None, "otrosDestMoneda": None,
			"totalRemi":None, "totalRemiMoneda": None, "totalDest":None, "totalDestMoneda":None}
		try:
			# DESTINATARIO:
			USD = "USD"
			gastos ["fleteDest"]	   = Utils.checkQuantity (self.fields ["17_Gastos:ValorFlete,MontoDestinatario"])
			gastos ["monedaDest"]      = USD if gastos ["fleteDest"] else None
			gastos ["seguroDest"]      = Utils.checkQuantity (self.fields ["17_Gastos:Seguro,MontoDestinatario"])
			gastos ["otrosDest"]       = Utils.checkQuantity (self.fields ["17_Gastos:OtrosGastos,MontoDestinatario"])
			gastos ["otrosDestMoneda"] = USD if gastos ["otrosDest"] else None
			gastos ["totalDest"]       = Utils.checkQuantity (self.fields ["17_Gastos:Total,MontoDestinatario"])
			gastos ["totalDestMoneda"] = USD if gastos ["totalDest"] else None

			# REMITENTE: 
			gastos ["fleteRemi"]       = Utils.checkQuantity (self.fields ["17_Gastos:ValorFlete,MontoRemitente"])
			gastos ["monedaRemi"]      = USD if gastos ["fleteRemi"] else None
			gastos ["seguroRemi"]      = Utils.checkQuantity (self.fields ["17_Gastos:Seguro,MontoRemitente"])
			gastos ["otrosRemi"]       = Utils.checkQuantity (self.fields ["17_Gastos:OtrosGastos,MontoRemitente"])
			gastos ["otrosRemiMoneda"] = USD if gastos ["otrosRemi"] else None
			gastos ["totalRemi"]       = Utils.checkQuantity (self.fields ["17_Gastos:Total,MontoRemitente"])
			gastos ["totalRemiMoneda"] = USD if gastos ["totalRemi"] else None

			# Check and convert to american format
#			for k in gastos.keys ():
#				if "moneda" in k.lower ():
#					continue
#				gastos [k] = Utils.getEcuapassFloatValue (gastos [k])
#
#				orgValue = gastos [k]
#				newValue = Utils.stringToAmericanFormat (gastos [k])
#				gastos [k] = "0.0" if gastos [k] == "" else Utils.stringToAmericanFormat (gastos [k])
			print (f"\n+++ Gastos Info: '{gastos}'")
			gastos = self.totalizeGastos (gastos)
		except:
			Utils.printException ("Obteniendo valores de 'gastos'")

		print (f"\n+++ Gastos info totals: '{gastos}'")
		return gastos

	#-------------------------------------------------------------------
	#-------------------------------------------------------------------
	def totalizeGastos (self, gastos):
		locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')
		try: 
			gastos ["otrosRemi"] = str (locale.atof (gastos ["otrosRemi"]) + locale.atof (gastos ["seguroRemi"]))
		except:
			gastos ["otrosRemi"] = "0.0||LOW"
			Utils.printException ()

		try: 
			gastos ["otrosDest"] = str (locale.atof (gastos ["otrosDest"]) + locale.atof (gastos ["seguroDest"]))
		except:
			gastos ["otrosDest"] = "0.0||LOW"
			Utils.printException ()

		return gastos

		                      
	#-------------------------------------------------------------------
	#-- For NTA and BYZA:
	#   Get subject info: nombre, dir, pais, ciudad, id, idNro ---------
	#-- BYZA format: <Nombre>\n<Direccion>\n<PaisCiudad><TipoID:ID> -----
	#-------------------------------------------------------------------
	#-- Get subject info: nombre, dir, pais, ciudad, id, idNro
#	def getSubjectInfo (self, subjectType):
#		text	= Utils.getValue (self.fields, subjectType)
#		subject = Extractor.getSubjectInfoFromText (text, self.resourcesPath, subjectType)
#		return (subject)

	#-------------------------------------------------------------------
	#-- Get subject info: nombre, dir, pais, ciudad, id, idNro ---------
	#-- NTA format: <Nombre> <Direccion> <ID> <PaisCiudad> -----
	#-------------------------------------------------------------------
	#-- Get subject info: nombre, dir, pais, ciudad, id, idNro
	def getSubjectInfo (self, key):
		subject = Utils.createEmptyDic (["nombre","direccion","pais","ciudad","tipoId","numeroId"])
		text	= self.fields [key]
		print (f"\n\n+++ SubjectInfo for '{key}' in text:\n{text}")
		try:
			text, subject = Extractor.removeSubjectId (text, subject, key)
			print (f"+++ Subject Info: Removed Id '{subject}'\n'{text}'")
			text, subject = Extractor.removeSubjectCiudadPais (text, subject, self.resourcesPath, key)
			print (f"+++ Subject Info: Removed Ciudad-Pais '{subject}'\n'{text}'")
			text, subject = Extractor.removeSubjectNombreDireccion (text, subject, key)
			print (f"+++ Subject Info: Removed NombreDireccion '{subject}'\n'{text}'")
		except:
			Utils.printException (f"Obteniendo datos del sujeto: '{key}' en el texto:\n'{text}'")

		print (f"+++ Subject info: '{subject}'")
		return (subject)

	#-------------------------------------------------------------------
	# Origin pais determines the procedure type: IMPORTACION or EXPORTACION
	#-------------------------------------------------------------------
	def getPaisOrigen (self):
		p1 = Utils.toString (Extractor.delLow (self.ecudoc ["10_PaisRemitente"]))
		p2 = Utils.toString (EExtractor.delLow (self.ecudoc ["29_PaisRecepcion"]))
		p3 = Utils.toString (EExtractor.delLow (self.ecudoc ["62_PaisEmision"]))

		if p1 == p2 or p1 == p3:
			return p1
		elif p2 == p1 or p2 == p3:
			return p2
		elif p3 == p1 or p3 == p2:
			return p3
		else: 
			return None

	#-------------------------------------------------------------------
	#-- Get pais destinatario
	#-------------------------------------------------------------------
	def getPaisDestinatario (self):
		return self.ecudoc ["16_PaisDestinatario"]

	#-----------------------------------------------------------
	#-----------------------------------------------------------
	# Basic functions
	#-----------------------------------------------------------
	#-----------------------------------------------------------
	def getPaisDestinoDocumento (self):
		try:
			paisDestino = self.getPaisDestinatario ()
			if not paisDestino:
				paisDestino = self.ecudoc ["35_PaisEntrega"] 
			return paisDestino
		except:
			return None

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

