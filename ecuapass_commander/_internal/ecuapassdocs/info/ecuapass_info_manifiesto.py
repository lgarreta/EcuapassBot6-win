#!/usr/bin/env python3

import re, os, json, sys
from traceback import format_exc as traceback_format_exc

from .ecuapass_info import EcuInfo
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
# Base class for DocXXXXX and BotXXXXXInfo Documents as 
# Cartaporte, Manifiesto, Declaracion
#----------------------------------------------------------
class ManifiestoInfo (EcuInfo):
	def __init__ (self, runningDir, empresa, pais, ecudocFields=None):
		super().__init__ ("MANIFIESTO", runningDir, empresa, pais, ecudocFields)

	#-- Get data and value from document main fields
	def extractEcuapassFields (self, docFieldsPath, analysisType="BOT"):
		#print ("\n>>>>>> Identificacion del Transportista Autorizado <<<")
		transportista                         = self.getTransportistaInfo ()
		self.ecudoc ["01_TipoProcedimiento"]  = transportista ["procedimiento"]
		self.ecudoc ["02_Sector"]             = transportista ["sector"]
		self.ecudoc ["03_Fecha_Emision"]      = transportista ["fechaEmision"]
		self.ecudoc ["04_Distrito"]           = transportista ["distrito"]
		self.ecudoc ["05_MCI"]                = transportista ["MCI"]
		self.ecudoc ["06_Empresa"]            = transportista ["empresa"]

		#print ("\n>>> Identificación Permisos")
		permisos                              = self.getPermisosInfo ()
		self.ecudoc ["07_TipoPermiso_CI"]     = permisos ["tipoPermisoCI"]
		self.ecudoc ["08_TipoPermiso_PEOTP"]  = permisos ["tipoPermisoPEOTP"]
		self.ecudoc ["09_TipoPermiso_PO"]     = permisos ["tipoPermisoPO"]
		self.ecudoc ["10_PermisoOriginario"]  = permisos ["permisoOriginario"]
		self.ecudoc ["11_PermisoServicios1"]  = permisos ["permisoServicios1"]
		self.ecudoc ["12_PermisoServicios2"]  = None
		self.ecudoc ["13_PermisoServicios3"]  = None
		self.ecudoc ["14_PermisoServicios4"]  = None

		# Empresa
		self.ecudoc ["15_NombreTransportista"] = self.getNombreEmpresa ()
		self.ecudoc ["16_DirTransportista"]    = self.getDireccionEmpresa ()

		#print ("\n>>>>>> Identificacion de la Unidad de Carga (Remolque) <<<")
		remolque                             = self.extractVehiculoInfo ("REMOLQUE")
		self.ecudoc ["24_Marca_remolque"]    = remolque ["marca"]
		self.ecudoc ["25_Ano_Fabricacion"]   = remolque ["anho"]
		self.ecudoc ["26_Placa_remolque"]    = remolque ["placa"]
		self.ecudoc ["27_Pais_remolque"]     = remolque ["pais"]
		self.ecudoc ["28_Nro_Certificado"]   = remolque ["certificado"]
		self.ecudoc ["29_Otra_Unidad"]       = remolque ["chasis"]

		#print ("\n>>>>>> Identificacion del Vehículo Habilitado <<<")
		vehiculo                             = self.extractVehiculoInfo ("VEHICULO", remolque)
		self.ecudoc ["17_Marca_Vehiculo"]    = vehiculo ["marca"]
		self.ecudoc ["18_Ano_Fabricacion"]   = vehiculo ["anho"]
		self.ecudoc ["19_Pais_Vehiculo"]     = vehiculo ["pais"]
		self.ecudoc ["20_Placa_Vehiculo"]    = vehiculo ["placa"]
		self.ecudoc ["21_Nro_Chasis"]        = vehiculo ["chasis"]
		self.ecudoc ["22_Nro_Certificado"]   = vehiculo ["certificado"]
		self.ecudoc ["23_Tipo_Vehiculo"]     = vehiculo ["tipo"]

		#print ("\n>>>>>> Identificacion de la Tripulacion <<<")
		conductor                             = self.extractConductorInfo ()
		self.ecudoc ["30_Pais_Conductor"]     = conductor ["pais"]
		self.ecudoc ["31_TipoId_Conductor"]   = conductor ["tipoDoc"]
		self.ecudoc ["32_Id_Conductor"]       = conductor ["documento"]
		self.ecudoc ["33_Sexo_Conductor"]     = conductor ["sexo"]
		self.ecudoc ["34_Fecha_Conductor"]    = conductor ["fecha_nacimiento"]
		self.ecudoc ["35_Nombre_Conductor"]   = conductor ["nombre"]
		self.ecudoc ["36_Licencia_Conductor"] = conductor ["licencia"]
		self.ecudoc ["37_Libreta_Conductor"]  = None

		# Auxiliar
		self.ecudoc ["38_Pais_Auxiliar"]     = None
		self.ecudoc ["39_TipoId_Auxiliar"]   = None
		self.ecudoc ["40_Id_Auxiliar"]       = None
		self.ecudoc ["41_Sexo_Auxiliar"]     = None
		self.ecudoc ["42_Fecha_Auxiliar"]    = None
		self.ecudoc ["43_Nombre_Auxiliar"]   = None
		self.ecudoc ["44_Apellido_Auxiliar"] = None
		self.ecudoc ["45_Licencia_Auxiliar"] = None
		self.ecudoc ["46_Libreta_Auxiliar"]  = None

		print ("\n>>>>>> Datos sobre la carga <<<")
		text                                 = self.fields ["23_Carga_CiudadPais"]
		ciudad, pais                         = Extractor.getCiudadPais (text, self.resourcesPath)
		self.ecudoc ["47_Pais_Carga"]        = Utils.checkLow (pais)
		self.ecudoc ["48_Ciudad_Carga"]      = Utils.checkLow (ciudad)

		text                                 = self.fields ["24_Descarga_CiudadPais"]
		ciudad, pais                         = Extractor.getCiudadPais (text, self.resourcesPath)
		self.ecudoc ["49_Pais_Descarga"]     = Utils.checkLow (pais)
		self.ecudoc ["50_Ciudad_Descarga"]   = Utils.checkLow (ciudad)

		#self.updateDistrito ("04_Distrito", descarga ["pais"]) # LOGITRANS: Update after knowing destination country

		cargaInfo                            = self.getCargaInfo ()
		self.ecudoc ["51_Tipo_Carga"]        = cargaInfo ["tipo"]
		self.ecudoc ["52_Descripcion_Carga"] = cargaInfo ["descripcion"]

		#print ("\n>>>>>> Datos de las aduanas <<<")
		aduana                                = self.getAduanaInfo ()
		self.ecudoc ["58_AduanaDest_Pais"]    = aduana ["paisDestino"]
		self.ecudoc ["59_AduanaDest_Ciudad"]  = aduana ["ciudadDestino"]

		#print ("\n>>>>>> Datos sobre las unidades) <<<")
		unidades = self.getUnidadesMedidaInfo ()
		self.ecudoc ["60_Peso_NetoTotal"]     = unidades ["pesoNetoTotal"]
		self.ecudoc ["61_Peso_BrutoTotal"]    = unidades ["pesoBrutoTotal"]
		self.ecudoc ["62_Volumen"]            = None
		self.ecudoc ["63_OtraUnidad"]         = unidades ["otraUnidadTotal"]

		## Aduana Cruce
		self.ecudoc ["64_AduanaCruce_Pais"]   = aduana ["paisCruce"]
		self.ecudoc ["65_AduanaCruce_Ciudad"] = aduana ["ciudadCruce"]

		#print ("\n>>>>>> Datos sobre la mercancia (Incoterm) <<<")
		text                                 = self.fields ["34_Precio_Incoterm_Moneda"]
		incoterm                             = super().getIncotermInfo (text)
		self.ecudoc ["53_Precio_Mercancias"] = incoterm ["precio"]
		self.ecudoc ["54_Incoterm"]          = incoterm ["incoterm"]
		self.ecudoc ["55_Moneda"]            = incoterm ["moneda"]
		self.ecudoc ["56_Pais"]              = incoterm ["pais"]
		self.ecudoc ["57_Ciudad"]            = incoterm ["ciudad"]

		#print ("\n>>>>>> Detalles finales <<<")
		self.ecudoc ["66_Secuencia"]         = Utils.addLow (self.getSecuencia ())
		self.ecudoc ["67_MRN"]               = self.getMRN ()
		self.ecudoc ["68_MSN"]               = self.getMSN ()

		bultos                         = self.getBultosInfoManifiesto ()
		self.ecudoc ["69_CPIC"]        = Utils.checkLow (bultos ["cartaporte"])
		self.ecudoc ["70_TotalBultos"] = Utils.checkLow (bultos ["cantidad"])
		self.ecudoc ["71_Embalaje"]	   = Utils.checkLow (bultos ["embalaje"])
		self.ecudoc ["72_Marcas"]      = Utils.checkLow (bultos ["marcas"])

		# Unidades
		self.ecudoc ["73_Peso_Neto"]        = unidades ["pesoNetoTotal"]
		self.ecudoc ["74_Peso_Bruto"]       = unidades ["pesoBrutoTotal"]
		self.ecudoc ["75_Volumen"]          = None
		self.ecudoc ["76_OtraUnidad"]       = unidades ["otraUnidadTotal"]

		#print ("\n>>>>>> Info de Unidad de Carga <<<")
		text                                = self.fields ["26_Carga_Contenedores"]
		unidadCarga                         = self.getUnidadCargaInfo (text)
		self.ecudoc ["77_Nro_UnidadCarga"]  = unidadCarga ["id"] 
		self.ecudoc ["78_Tipo_UnidadCarga"] = unidadCarga ["tipo"]
		self.ecudoc ["79_Cond_UnidadCarga"] = unidadCarga ["condicion"]
		self.ecudoc ["51_Tipo_Carga"]       = unidadCarga ["tipoCarga"]

		#print ("\n>>>>>> Datos finales <<<")
		self.ecudoc ["80_Tara"]             = None
		self.ecudoc ["81_Descripcion"]      = bultos ['descripcion']
		self.ecudoc ["82_Precinto"]         = Utils.getValue (self.fields, "27_Carga_Precintos")

		# Update fields depending of other fields (or depending of # "empresa")
		self.updateExtractedEcuapassFields ()

		return (self.ecudoc)

	#------------------------------------------------------------------
	# Transportista information 
	#------------------------------------------------------------------
	def getTransportistaInfo (self):
		transportista = Utils.createEmptyDic (["procedimiento", "sector", "fechaEmision", "distrito", "MCI", "empresa"])
		try:	
			transportista ["procedimiento"]     = self.getTipoProcedimiento ()
			transportista ["sector"]            = "NORMAL||LOW"

			text                                = Utils.getValue (self.fields, "40_Fecha_Emision")
			transportista ["fechaEmision"]      = Extractor.getDate (text, self.resourcesPath)
			transportista ["distrito"]          = self.getDistrito ()
			transportista ["MCI"]               = self.getNumeroDocumento ()
			transportista ["empresa"]           = None    # Bot select the first option in BoxField
		except:
			Utils.printException ("Obteniendo información del transportista")
		return (transportista)

	#------------------------------------------------------------------
	# Permisos info: Overwritten in subclasses
	#-- Just "Originario"
	#------------------------------------------------------------------
	def getPermisosInfo (self):
		permisosInfo = Utils.createEmptyDic (["tipoPermisoCI","tipoPermisoPEOTP","tipoPermisoPO","permisoOriginario","permisoServicios1"])
		try:
			empresaInfo                        = EcuData.getEmpresaInfo (self.empresa)
			permisosInfo ["tipoPermisoPO"]     = "1"
			permisosInfo ["permisoOriginario"] = empresaInfo ["permisos"]["originario"]
		except:
			Utils.printException ("Obteniendo información de permisos")
		return permisosInfo

#	def getPermisosInfo (self):
#		permisos = Utils.createEmptyDic (["tipoPermisoCI", "tipoPermisoPEOTP", 
#									      "tipoPermisoPO", "permisoOriginario", "permisoServicios"])
#		try:
#			permisos ["permisoOriginario"] = self.getPermiso_PerEmpresa ("ORIGINARIO") 
#			permisos ["permisoServicios"]  = self.getPermiso_PerEmpresa ("SERVICIOS")
#			#permisos ["permisoOriginario"] = self.getPermiso ("02_Permiso_Originario")
#			#permisos ["permisoServicios"]  = self.getPermiso ("03_Permiso_Servicios").replace ("-","")
#
#			tipoPermiso = permisos ["permisoOriginario"].split ("-")[0]
#			tipoPermiso = re.sub (r"[^A-Za-z0-9]+", "", tipoPermiso).upper()  # re for removing symbols
#			if (tipoPermiso == "CI"):
#				permisos ["tipoPermisoCI"]     = "1"
#			elif (tipoPermiso == "POETP"):
#				permisos ["tipoPermisoPOETP"]  = "1"
#			elif (tipoPermiso == "PO"):
#				permisos ["tipoPermisoPO"]     = "1"
#			else:
#				Utils.printException (f"Tipo permiso desconocido en el texto: '{text}'")
#		except:
#			Utils.printException ("Obteniendo información de permisos")
#
#		return (permisos)

	#------------------------------------------------------------------
	# 'Servicios" permission is None for BYZA
	#------------------------------------------------------------------
	def getPermiso_PerEmpresa (self, tipoPermiso):
		outPermiso = None
		#----------------------------------------------------------
		def getPermiso (key):
			"""May contain one or two numbers. First is returned"""
			permiso = self.fields [key]
			return permiso.split ("\n")[0]
		#----------------------------------------------------
		if tipoPermiso == "ORIGINARIO":
			outPermiso =  getPermiso ("02_Permiso_Originario")
		elif tipoPermiso == "SERVICIOS":
			if self.empresaInfo["id"] == "BYZA":
				outPermiso = None
			else:
				outPermiso = getPermiso ("03_Permiso_Servicios").replace ("-","")

		return outPermiso
		
	#------------------------------------------------------------------
	# Get Vehiculo/Remolque information 
	#------------------------------------------------------------------
	def extractVehiculoInfo (self, type="VEHICULO", remolque=None):
#		vehiculo = {key:None for key in ["marca","anho","pais","placa","chasis","certificado","tipo"]}
#		keys     = None
#		if type == "VEHICULO":
#			keys = {"marca":"04_Camion_Marca", "anho":"05_Camion_AnoFabricacion", "placaPais":"06_Camion_PlacaPais", 
#		   			"chasis":"07_Camion_Chasis", "certificado":"08_Certificado_Habilitacion"}
#		elif type == "REMOLQUE":
#			keys = {"marca":"09_Remolque_Marca", "anho":"10_Remolque_AnoFabricacion", "placaPais":"11_Remolque_PlacaPais", 
#					"chasis": "12_Remolque_Otro", "certificado": "08_Certificado_Habilitacion"}
#		else:
#			print (f"ERROR: Tipo de vehiculo desconocido: '{type}'")
#			return vehiculo

		#generalFields  = ["marca", "anho", "pais", "placa", "chasis", "certificado"]
		generalFields  = ["marca", "anho", "placaPais", "chasis", "certificado"]
		vehiculoFields = dict (zip (generalFields, ["04_Camion_Marca", "05_Camion_AnoFabricacion", 
						"06_Camion_PlacaPais", "07_Camion_Chasis", "08_Certificado_Habilitacion"]))
		remolqueFields = dict (zip (generalFields, ["09_Remolque_Marca", "10_Remolque_AnoFabricacion", 
						"11_Remolque_PlacaPais", "12_Remolque_Otro", "08_Certificado_Habilitacion"]))

		keys     = vehiculoFields if type == "VEHICULO" else remolqueFields
		vehiculo = {key:None for key in ["marca","anho","pais","placa","chasis","certificado","tipo"]}
		try:
			text = self.fields [keys ["placaPais"]]
			placaPaisText = Extractor.getValidValue (self.fields [keys ["placaPais"]])
			if placaPaisText:
				placaPais                = Extractor.getPlacaPais (placaPaisText, self.resourcesPath) 
				vehiculo ["placa"]       = Extractor.getValidValue (placaPais ["placa"])
				vehiculo ["pais"]        = Extractor.getValidValue (placaPais ["pais"])
				vehiculo ["marca"]       = Extractor.getValidValue (self.fields [keys ["marca"]])
				vehiculo ["anho"]        = Extractor.getValidValue (self.fields [keys ["anho"]])
				vehiculo ["chasis"]      = Extractor.getValidValue (self.fields [keys ["chasis"]])
				vehiculo ["certificado"] = Extractor.getValidValue (self.getCheckCertificado (type, keys ["certificado"]))
				vehiculo ["tipo"]        = self.getTipoVehiculo (type, remolque)
		except Exception as e:
			Utils.printException (f"Extrayendo información del vehículo", e)

		print (f"\n+++ Vehiculo: '{type}' : '{vehiculo}'")
		return vehiculo

	#-- Get ECUAPASS tipo vehículo for 'empresa'
	def getTipoVehiculo  (self, tipo, remolque=None):
		remolque.pop ('chasis') if remolque else None    # Maybe no chasis in remolque
		if tipo == "VEHICULO" and Extractor.getValidValue (remolque):
			return "TRACTOCAMION"
		elif tipo == "VEHICULO" and not Extractor.getValidValue (remolque): 
			return "CAMION"
		elif tipo == "REMOLQUE":
			return "TRACTOCAMION"

	#-- Return certificadoString if it is valid (e.g. CH-CO-XXXX-YY, RUC-CO-XXX-YY), else None
	def getCheckCertificado (self, vehicleType, key):
		try:
			textCertificado  = Utils.getValue (self.fields, key)
			if vehicleType == "VEHICULO":
				text    = Extractor.getFirstString (textCertificado)
				pattern = re.compile (r'^CH-(CO|EC)-\d{4,5}-\d{2}')
			elif vehicleType == "REMOLQUE":
				text    = Extractor.getLastString (textCertificado)
				pattern = re.compile (r'^(CRU|CR)-(CO|EC)-\d{4,5}-\d{2}')

			if (text == None): 
				return "||LOW" if vehicleType == "VEHICULO" else None

			certificadoString = self.formatCertificadoString (text, vehicleType)
			if bool (pattern.match (certificadoString)) == False:
				Utils.printx (f"Error validando certificado de <{vehicleType}> en texto: '{certificadoString}'")
				certificadoString = "||LOW"
		except:
			Utils.printException (f"Obteniendo/Verificando certificado '{certificadoString}' para '{vehicleType}'")

		return certificadoString;

	#-- Try to convert certificado text to valid certificado string
	#-- Overwriten in LOGITRANS (CR-->CRU)
	def formatCertificadoString (self, text, vehicleType):
		try:
			if (text in [None, ""]):
				return None

			text = text.replace ("-","") 
			text = text.replace (".", "") 
 
			first = None
			if vehicleType == "VEHICULO":
				first  = text [0:2]; text = text [2:]   # CH
			elif vehicleType == "REMOLQUE":
				if text [0:3] == "CRU":
					first  = "CRU"; text = text [3:]   # CRU
				elif text [0:2] == "CR":
					first  = "CRU"; text = text [2:]   # CR

			second = text [0:2]; text = text [2:]       # CO|EC
			last   = text [-2:]; text = text [:-2]      # 23|23|XX
			middle = text                               # XXXX|YYYYY

			certificadoString = f"{first}-{second}-{middle}-{last}"
		except:
			Utils.printException (f"Excepción formateando certificado para '{vehicleType}' desde el texto '{text}'")
			certificadoString = ""

		return certificadoString
		
	#------------------------------------------------------------------
	# Extract conductor/Auxiliar informacion
	#------------------------------------------------------------------
	def extractConductorInfo (self, type="CONDUCTOR"):
		keysAll = {
			"CONDUCTOR":{"nombreFecha":"13_Conductor_Nombre", "documento":"14_Conductor_Id", 
					   "pais":"15_Conductor_Nacionalidad", "licencia":"16_Conductor_Licencia"},
		  	"AUXILIAR" :{"nombreFecha":"18_Auxiliar_Nombre", "documento":"19_Auxiliar_Id",  
					   "pais":"20_Auxiliar_Nacionalidad", "licencia":"21_Auxiliar_Licencia"}
		}
		conductor = Utils.createEmptyDic (["pais", "tipoDoc", "documento", "sexo", "fecha_nacimiento", "nombre", "licencia"])
		keys      = keysAll [type]
		try:
			documento = Utils.getValue (self.fields, keys ["documento"])
			if Extractor.getValidValue (documento):
				conductor ["documento"]        = documento
				conductor ["pais"]             = Extractor.getPaisFromPrefix (Utils.getValue (self.fields, keys ["pais"]))  
				conductor ["tipoDoc"]          = "CEDULA DE IDENTIDAD"
				conductor ["sexo"]             = "Hombre"
				text                           = Utils.getValue (self.fields, keys ["nombreFecha"])
				fecha_nacimiento               = Extractor.getDate (text, self.resourcesPath)
				conductor ["fecha_nacimiento"] = fecha_nacimiento if fecha_nacimiento else "||LOW"
				conductor ["nombre"]           = Extractor.extractNames (text)
				conductor ["licencia"]         = Utils.getValue (self.fields, keys ["licencia"])
		except:
			Utils.printException ("Obteniendo informacion del conductor")
		print (f"\n+++ Conductor '{conductor}'")
		return conductor

	#------------------------------------------------------------------
	# Info carga: type and descripcion
	#------------------------------------------------------------------
	def getCargaInfo (self):
		info = {"tipo": None, "descripcion": "||LOW"}
		try:
			info ["tipo"]           = Utils.checkLow (self.getTipoCarga ())
			info ["descripcion"]    = self.getCargaDescripcion ()
		except:
			Utils.printException ("Obteniendo inforamcion de la carga en texto:")
		return info

	#-- Overwritten in companies (BYZA:None)
	def getCargaDescripcion (self):
		return self.fields ["25e_Carga_TipoDescripcion"]

	def getTipoCarga (self):
		return "CARGA SUELTA||LOW"

	#-- Get info from unidad de carga (Containers)
	def getUnidadCargaInfo (self, text):
		tipoCarga    = self.ecudoc ["51_Tipo_Carga"]
		unidadCarga  = {"id": None, "tipo": None, "condicion": None, "tipoCarga": tipoCarga}
		contenedores = {"20": "CONTAINER IC 20 FEET", "30": "CONTAINER IC 30 FEET", "40": "CONTAINER IC 40 FEET"}

		if not text:
			return unidadCarga

		try:
			id, tipo                  = Extractor.getContenedorIdTipo (text.strip())
			unidadCarga ["id"]        = id
			unidadCarga ["tipo"]      = contenedores [tipo] 
			unidadCarga ["condicion"] = "LLENO"

			if not tipoCarga or "LOW" in tipoCarga:
				unidadCarga ["tipoCarga"] = "CARGA CONTENERIZADA||LOW"
		except:
			Utils.printException (f"Llenando info unidad de carga en texto: '{text}'")
			unidadCarga = {"id": "||LOW", "tipo": "||LOW", "condicion": "||LOW", "tipoCarga": tipoCarga}

		print (f"+++ Info Unidad carga '{unidadCarga}'")
		return unidadCarga

	#--------------------------------------------------------------------
	#-- Search "pais" for "ciudad" in previous document boxes
	#--------------------------------------------------------------------
	def searchPaisPreviousBoxes (self, ciudad, pais):
		try:
			if ciudad != None and pais == None:
				if self.ecudoc ["48_Ciudad_Carga"] and ciudad in self.ecudoc ["48_Ciudad_Carga"]:
					pais	 = self.ecudoc ["47_Pais_Carga"]
				elif self.ecudoc ["50_Ciudad_Descarga"] and ciudad in self.ecudoc ["50_Ciudad_Descarga"]:
					pais	 = self.ecudoc ["49_Pais_Descarga"]

		except Exception as e:
			Utils.printException (f"Obteniendo informacion de 'mercancía' en texto: '{text}'", e)
		return ciudad, pais


#	#-----------------------------------------------------------
#	# Match ciudad previous boxes and get return ciudad-pais
#	#-----------------------------------------------------------
#	def matchCiudadPaisPreviousBoxes (self, text):
#		pais, ciudad = None, None
#		keysPaisesCiudades = [("47_Pais_Carga", "48_Ciudad_Carga"), ("49_Pais_Descarga", "50_Ciudad_Descarga"),
#			("58_AduanaDest_Pais", "59_AduanaDest_Ciudad"), ("64_AduanaCruce_Pais", "65_AduanaCruce_Ciudad")]
#
#		try:
#			for keys in keysPaisesCiudades:
#				pais   = Extractor.delLow (self.ecudoc [keys [0]])
#				ciudad = Extractor.delLow (self.ecudoc [keys [1]])
#				if ciudad in text:
#					return ciudad, pais
#		except:
#			Utils.printException (f"Buscando ciudades previas en texto: '{text}'")
#		return ciudadPais
#
	#-----------------------------------------------------------
	# Return ecudoc field keys containing ciudad,pais 
	#-----------------------------------------------------------
	def getCiudadPaisKeys (self):
		ciudadPaisKeys = [
			("48_Ciudad_Carga","47_Pais_Carga"), 
			("50_Ciudad_Descarga", "49_Pais_Descarga"),
			("59_AduanaDest_Ciudad", "58_AduanaDest_Pais"),
			("65_AduanaCruce_Ciudad", "64_AduanaCruce_Pais")]
		return ciudadPaisKeys

#	#-----------------------------------------------------------
#	# Get ciudad, pais either: normal search or multiple sources
#	#-----------------------------------------------------------
#	def getCiudadPaisMultipleSources (self, text):
#		pais, ciudad = None, None
#		try:
#			# Default: ciudad-pais
#			ciudad, pais   = Extractor.getCiudadPais (text, self.resourcesPath, ECUAPASS=True) 
#			print (f"+++ Previous boxes default. Ciudad: '{ciudad}'. Pais: '{pais}'")
#
#			if ciudad and pais:
#				return ciudad, pais
#			else: # Special: Using previous boxes 
#				keysPaisesCiudades = [("47_Pais_Carga", "48_Ciudad_Carga"), ("49_Pais_Descarga", "50_Ciudad_Descarga"),
#					("58_AduanaDest_Pais", "59_AduanaDest_Ciudad"), ("64_AduanaCruce_Pais", "65_AduanaCruce_Ciudad")]
#
#				for keys in keysPaisesCiudades:
#					print (f"+++ Previous boxes keys '{keys}'")
#					pais   = Extractor.delLow (self.ecudoc [keys [0]])
#					ciudad = Extractor.delLow (self.ecudoc [keys [1]])
#					print (f"+++ Previous boxes. Ciudad: '{ciudad}'. Pais: '{pais}'")
#					if ciudad in text:
#						return ciudad, pais
#		except:
#			Utils.printException (f"Buscando pais, ciudad con múltiples fuentes en texto: '{text}'")
#		return ciudad, pais

	#-----------------------------------------------------------
	# Get info from unidades de medida:"peso neto, volumente, otras
	#-----------------------------------------------------------
	def getUnidadesMedidaInfo (self):
		info = {"pesoNetoTotal":None, "pesoBrutoTotal":None, "otraUnidadTotal":None}
		try:
			info ["pesoBrutoTotal"]  = Utils.checkQuantity (Extractor.getNumber (self.fields ["32a_Peso_BrutoTotal"]))
			info ["pesoNetoTotal"]   = Utils.checkQuantity (Extractor.getNumber (self.fields ["32b_Peso_NetoTotal"]))
			info ["otraUnidadTotal"] = Utils.checkQuantity (Extractor.getNumber (self.fields ["33_Otra_MedidaTotal"]))
		except:
			Utils.printException ("'Unidades de Medida'")

		print (f"\n+++ Unidades medida '{info}'")

		return info

	#--------------------------------------------------------------------
	# Aduana info: extract ciudad and pais for "cruce" and "destino" aduanas
	#--------------------------------------------------------------------
	def getAduanaInfo (self):
		info = {"paisCruce":"||NEEDED", "ciudadCruce":"||NEEDED", "paisDestino":"||NEEDED", "ciudadDestino":"||NEEDED"}
		#info = Utils.createEmptyDic (["paisCruce", "ciudadCruce", "paisDestino", "ciudadDestino"])
		text = ""
		try:
			aduanas = {}
			aduanas ["37_Aduana_Cruce"]   = {"ciudad":"ciudadCruce", "pais": "paisCruce"}
			aduanas ["38_Aduana_Destino"] = {"ciudad":"ciudadDestino", "pais": "paisDestino"}

			for key in ["37_Aduana_Cruce", "38_Aduana_Destino"]:
				print (f"+++ AduanaInfo text: '{key}' :'{text}'")
				text = self.fields [key]
				ciudad, pais = Extractor.getCiudadPais (text, self.resourcesPath)
				info [aduanas [key]["ciudad"]] = ciudad if Utils.isValidText (ciudad) else "||NEEDED"
				info [aduanas [key]["pais"]]   = pais if Utils.isValidText (pais) else "||NEEDED"

			print (f"+++ AduanaInfo '{info}'")
		except Exception as e:
			Utils.printException (f"Extrayendo pais-ciudad desde aduanas en texto: '{text}'", e)
		return info


#	def getAduanaInfoWithREs (self):
#		info = {"paisCruce":"||NEEDED", "ciudadCruce":"||NEEDED", "paisDestino":"||NEEDED", "ciudadDestino":"||NEEDED"}
#		#info = Utils.createEmptyDic (["paisCruce", "ciudadCruce", "paisDestino", "ciudadDestino"])
#		text = ""
#		try:
#			#reWithSeparador = r'(\b\w+[\s\w]*\b)\s*?[-.,]?\s*(\w+)'
#			reWithSeparador = r"(?P<city>[A-Za-z\s]+)\s*[-,\.]\s*(?P<country>[A-Za-z\s]+)"
#			reWithParentesis = r'(\b\w+[\s\w]*\b)\s*?\s*[(](\w+)[)]'
#
#			aduanas = {}
#			aduanas ["37_Aduana_Cruce"]   = {"ciudad":"ciudadCruce", "pais": "paisCruce"}
#			aduanas ["38_Aduana_Destino"] = {"ciudad":"ciudadDestino", "pais": "paisDestino"}
#
#			for key in ["37_Aduana_Cruce", "38_Aduana_Destino"]:
#				text = Utils.getValue (self.fields, key)
#				results = [re.search (x, text) for x in [reWithSeparador, reWithParentesis]]
#				print ("+++ Aduana resultados:", results)
#
#				if results [0] or results [1]:
#					result = results [0] if results [0] else results [1]
#					ciudad = result.group (1).strip()
#					info [aduanas [key]["ciudad"]] = ciudad if Utils.isValidText (ciudad) else "||NEEDED"
#					pais = Extractor.getPaisFromPrefix (result.group (2)).strip()
#					info [aduanas [key]["pais"]]   = pais if Utils.isValidText (pais) else "||NEEDED"
#
#		except Exception as e:
#			Utils.printException (f"Extrayendo pais-ciudad desde aduanas en texto: '{text}'", e)
#		return info
	#------------------------------------------------------------------
	# Secuencia, MRN, MSN, NumeroCPIC for BOTERO-SOTO
	#------------------------------------------------------------------
	def getSecuencia (self):
		return "1"

	def getMSN (self):
		return "0001" + "||LOW"

	#-----------------------------------------------------------
	#-- Get bultos info: cantidad, embalaje, marcas
	#-- It uses base "getBultosInfo"
	#-----------------------------------------------------------
	def getBultosInfoManifiesto (self):
		ecuapassFields = {"cantidad": "30_Mercancia_Bultos", "marcas":
			   "31_Mercancia_Embalaje", "descripcion": "29_Mercancia_Descripcion"}

		bultosInfo = self.getBultosInfo (ecuapassFields)
		bultosInfo ["cartaporte"] = self.getNumeroCartaporte ()
		return bultosInfo

	#-----------------------------------------------------------
	#-----------------------------------------------------------
	# Basic functions
	#-----------------------------------------------------------
	#-----------------------------------------------------------
	def getPaisDestinoDocumento (self):
		try:
			paisDestino = self.ecudoc ["49_Pais_Descarga"]
			if not paisDestino:
				paisDestino = self.ecudoc ["58_AduanaDest_Pais"]
			return paisDestino
		except:
			return None

	#-- Extract numero cartaprote from doc fields
	def getNumeroCartaporte (self):
		docKey = "28_Mercancia_Cartaporte"
		text    = Utils.getValue (self.fields, docKey)
		numero  = Extractor.getNumeroDocumento (text.replace ("\n", ""))
		return numero
		
#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()

