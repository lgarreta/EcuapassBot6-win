
import os, json, re, datetime, importlib

from .resourceloader import ResourceLoader 
from .ecuapass_data import EcuData
from .ecuapass_extractor import Extractor
from .ecuapass_utils import Utils
from .ecuapass_exceptions import EcudocExtractionException

# Base class for all info document clases: CartaporteInfo (CPI), ManifiestoInfo (MCI), EcuDCL (DTAI)
class EcuInfo:

	def __init__ (self, docType, runningDir, empresa, pais, ecudocFields=None):
		# When called from predictions: ecudocFields, else docFieldsPath
		self.fields               = ecudocFields   # Called when predicting values
		self.docType              = docType
		self.runningDir           = runningDir
		self.empresa              = empresa
		self.pais                 = pais
		self.distrito             = None

		self.inputsParametersFile = Utils.getInputsParametersFile (docType)
		self.empresaInfo          = EcuData.getEmpresaInfo (self.empresa)   # Overwritten per 'empresa'
		self.ecudoc               = {}                       # Ecuapass doc fields (CPI, MCI, DTI)
		self.resourcesPath        = os.path.join (runningDir, "resources", "data_ecuapass") 
#		self.numero               = self.getNumeroDocumento () # From docFields

	#-- Get data and value from document main fields"""
	def extractFields (self, docFieldsPath, analysisType="BOT"):
		logFile, stdoutOrg = Utils.redirectOutput (f"log-extraction-{self.docType}.log")
		try:
			self.fields  = json.load (open (docFieldsPath))
			self.numero  = self.getNumeroDocumento () # From docFields
			ecuFields    = self.extractEcuapassFields (docFieldsPath, analysisType)
			return ecuFields
		except:
			Utils.redirectOutput ("log-extraction-cartaporte.log", logFile, stdoutOrg)
			Utils.printException ()
			raise EcudocExtractionException ("Extrayendo información del documento '{docFieldsPath}'")
		finally:
			Utils.redirectOutput ("log-extraction-cartaporte.log", logFile, stdoutOrg)

	#------------------------------------------------------------------
	#-- Create "ecuapass_info_XXXX" class from empresa and docType
	#-- Eg. "Cartaporte_BYZA" from "ecuapass_info_BYZA"
	#------------------------------------------------------------------
	def createInfoClass (docType, empresa, pais, runningDir):
		empresaMatriz = Utils.getEmpresaMatriz (empresa)

		module = importlib.import_module (f"ecuapassdocs.info.ecuapass_info_{empresaMatriz}")

		DOCINFOCLASS = None
		if docType == "CARTAPORTE":
			DOCINFOCLASS = getattr (module, f"Cartaporte_{empresaMatriz}")
		elif docType == "MANIFIESTO":
			DOCINFOCLASS = getattr (module, f"Manifiesto_{empresaMatriz}")

		docInfo = DOCINFOCLASS (runningDir, empresa,  pais)
		return docInfo

	def createDocInfoInstance (docType, empresa, pais, runningDir):
		empresaMatriz = Utils.getEmpresaMatriz (empresa)
		package       = "ecuapassdocs.info"
		module        = f"ecuapass_info_{empresaMatriz}"
		infoClass     = f"{docType.capitalize ()}_{empresaMatriz}" 
		MyClass       = ResourceLoader.load_class_from_module (package, module, infoClass)
		instance      = MyClass (runningDir, empresa, pais)  # Create an instance of the dynamically loaded class
		#instance.some_method()  # Call a method on the instance
		return instance


	#------------------------------------------------------------------
	# Set distrito from scraping class
	#------------------------------------------------------------------
	def setDistrito (self, distrito):
		self.distrito = distrito

	def getDistrito (self):
		if not self.distrito:
			self.distrito = "TULCAN" + "||LOW"
		
		return self.distrito

#	#-----------------------------------------------------------
#	# Get distrito according to 'empresa'
#	#-----------------------------------------------------------
#	def getDistrito (self):
#		distrito = None
#		try:
#			numero            = self.getNumeroDocumento ()
#			codigoPais        = Utils.getCodigoPais (numero)
#			idEmpresa         = self.getIdEmpresa ()
#			if idEmpresa == "NTA" and codigoPais == "PE":
#				distrito = "HUAQUILLAS"
#			else: # For NTA, BYZA, LOGITRANS
#				distrito = "TULCAN" + "||LOW"
#
#			return distrito
#		except:
#			Utils.printException ("No se pudo determinar el distrito (Importación/Exportación)")


	#------------------------------------------------------------------
	# Update fields that depends of other fields
	#------------------------------------------------------------------
	def updateExtractedEcuapassFields (self):
		#self.numero = self.getNumeroDocumento ()
		#self.pais   = Utils.getPaisFromDocNumber (self.numero)
		self.updateTipoProcedimientoFromFiels ()
		self.updateDistritoFromFields ()

	#-- Update tipo procedimiento (EXPO|INPO|TRANSITO) after knowing "Destino"
	#-- Update fecha entrega (when transito)
	def updateTipoProcedimientoFromFiels (self):
		tipoProcedimiento = self.getTipoProcedimiento ()

		procKeys = {
			"CARTAPORTE": "05_TipoProcedimiento", 
			"MANIFIESTO": "01_TipoProcedimiento", 
			"DECLARACION": "03_TipoProcedimiento"
		}
		self.ecudoc [procKeys [self.docType]] = tipoProcedimiento

	#-- Update distrito after knowing paisDestinatario
	def updateDistritoFromFields (self):
		try:
			distrito      = "TULCAN||LOW"
			paisDestino   = self.getPaisDestinoDocumento ()

			docKeys = {
				"CARTAPORTE":  "01_Distrito",
				"MANIFIESTO":  "04_Distrito",
				"DECLARACION": "01_Distrito"
			}
			ecuapassField = docKeys [self.docType]

			# Set distrito
			if self.pais == "PERU":
				self.ecudoc [ecuapassField] = "HUAQUILLAS"
			elif self.pais == "COLOMBIA":
				self.ecudoc [ecuapassField] = "TULCAN"
			elif "PERU" in paisDestino:
				self.ecudoc [ecuapassField] = "HUAQUILLAS"
			else:
				self.ecudoc [ecuapassField] = "TULCAN"
		except Exception as ex:
			Utils.printx ("EXCEPCION actualizando distrito: '{ex}'")
	
	#-- Get doc number from docFields (azrFields)
	def getNumeroDocumento (self, docKey="00_Numero"):
		text   = self.fields [docKey]
		numero = Extractor.getNumeroDocumento (text)
		return numero

	#-- Return the document "pais" from docFields
	def getPaisDocumento (self):
		return self.fields ["00a_Pais"]
		#numero = self.getNumeroDocumento ()
		#pais = Utils.getPaisFromDocNumber (numero)
		#return pais

	#-- Extract numero cartaprote from doc fields
	def getNumeroCartaporte (docFields, docType):
		keys    = {"CARTAPORTE":"00_Numero", "MANIFIESTO":"28_Mercancia_Cartaporte", "DECLARACION":"15_Cartaporte"}
		text    = Utils.getValue (docFields, keys [docType])
		text    = text.replace ("\n", "")
		numero  = Extractor.getNumeroDocumento (text)
		return numero

	#-- Extract 'fecha emision' from doc fields
	def getFechaEmision (docFields, docType, resourcesPath=None):
		fechaEmision = None
		text = None
		try:
			keys    = {"CARTAPORTE":"19_Emision", "MANIFIESTO":"40_Fecha_Emision", "DECLARACION":"23_Fecha_Emision"}
			text    = Utils.getValue (docFields, keys [docType])
			fecha   = Extractor.getDate (text, resourcesPath)
			#fecha   = fecha if fecha else datetime.datetime.today ()
			fechaEmision = Utils.formatDateStringToPGDate (fecha)
		except:
			print (f"EXCEPCION: No se pudo extraer fecha desde texto '{text}'")
			fechaEmision = None
			#fechaEmision = datetime.today ()
		return fechaEmision

	#-- Return updated PDF document fields
	def getDocFields (self):
		return self.fields

	#-- Get id (short name: NTA, BYZA, LOGITRANS)
	def getIdEmpresa (self):
		return self.empresaInfo ["id"]

	def getIdNumeroEmpresa (self):
		id = self.empresaInfo ["idNumero"]
		return id

	#-- Get full name (e.g. N.T.A Nuevo Transporte ....)
	def getNombreEmpresa (self): 
		return self.empresaInfo ["nombre"]

	#-- For NTA there are two directions: Tulcan and Huaquillas
	def getDireccionEmpresa (self):
		try:
			numero            = self.getNumeroDocumento ()
			codigoPais        = Utils.getCodigoPais (numero)
			idEmpresa         = self.getIdEmpresa ()

			if idEmpresa == "NTA" and codigoPais == "PE":
				return self.empresaInfo ["direccion02"]
			else:
				return self.empresaInfo ["direccion"]
		except:
			Utils.printException ("No se pudo determinar dirección empresa")
			return None

	#-----------------------------------------------------------
	#-- IMPORTACION or EXPORTACION or TRANSITO (after paisDestino)
	#-----------------------------------------------------------
	def getTipoProcedimiento (self):
		#originPais = self.getPaisOrigen ()
		print (f"+++ getTipoProcedimiento : País: '{self.pais}'")

		tipoProcedimiento = None
		paisDestino = self.getPaisDestinoDocumento ()
		try:
			if self.pais == "COLOMBIA" and paisDestino == "PERU":
				return "TRANSITO"
			else:
				return EcuData.procedureTypes [self.pais]
				#procedimientos    = {"COLOMBIA":"IMPORTACION", "ECUADOR":"EXPORTACION", "PERU":"IMPORTACION"}
				#numero            = self.getNumeroDocumento ()
				#codigoPais        = Utils.getCodigoPais (numero)
				#return procedimientos [codigoPais]

		except:
			Utils.printException ("No se pudo determinar procedimiento (IMPO/EXPO/TRANSITO)")

		return "IMPORTACION||LOW"


	#-----------------------------------------------------------
	# Get info from mercancia: INCONTERM, Ciudad, Precio, Tipo Moneda
	#-----------------------------------------------------------
	def getIncotermInfo (self, text):
		info = {"incoterm":None, "precio":None, "moneda":None, "pais":None, "ciudad":None}

		try:
			text = text.replace ("\n", " ")

			# Precio
			text, precio    = Extractor.getRemoveNumber (text)
			#info ["precio"] = Utils.checkLow (Utils.stringToAmericanFormat (precio))
			info ["precio"] = Utils.checkLow (Utils.checkQuantity (precio))
			text = text.replace (precio, "") if precio else text

			# Incoterm
			termsString = Extractor.getDataString ("tipos_incoterm.txt", 
			                                        self.resourcesPath, From="keys")
			reTerms = rf"\b({termsString})\b" # RE for incoterm
			incoterm = Utils.getValueRE (reTerms, text)
			info ["incoterm"] = Utils.checkLow (incoterm)
			text = text.replace (incoterm, "") if incoterm else text

			# Moneda
			info ["moneda"] = "USD"
			text = text.replace ("USD", "")
			text = text.replace ("$", "")
			#text = text.replace ("DOLARES", "")

			# Ciudad-Pais
			ciudad, pais   = self.getCiudadPaisMultipleSources (text)
			info ["pais"]   = Utils.checkLow (pais)
			info ["ciudad"] = Utils.checkLow (ciudad)

		except:
			Utils.printException ("Obteniendo informacion de 'mercancía'")

		print (f"\n+++ Incoterm text '{text}'")
		print (f"+++ Incoterm info '{info}'")
		return info

	#-----------------------------------------------------------
	# Get ciudad, pais either: normal search or multiple sources
	#-----------------------------------------------------------
	def getCiudadPaisMultipleSources (self, text):
		pais, ciudad = None, None
		try:
			# Default: ciudad-pais
			ciudad, pais   = Extractor.getCiudadPais (text, self.resourcesPath, ECUAPASS=True) 
			if "BOGOTA" in text:
				return "BOGOTA", "COLOMBIA"

			if ciudad and pais:
				return ciudad, pais

			# Special: Using previous boxes 
			ciudadPaisKeys = self.getCiudadPaisKeys ()
			for keys in ciudadPaisKeys:
				ciudad = Extractor.delLow (self.ecudoc [keys [0]])
				pais   = Extractor.delLow (self.ecudoc [keys [1]])
				if ciudad and pais and ciudad in text:
					return ciudad, pais
			return "",""

		except:
			Utils.printException (f"Buscando pais, ciudad con múltiples fuentes en texto: '{text}'")
		return ciudad, pais
	#-----------------------------------------------------------
	# Clean watermark: depending for each "company" class
	#-----------------------------------------------------------
	def cleanWaterMark (self, text):
		if self.empresaInfo ['id'] == "NTA":
			w1, w2, w3, w4 = r"N\.T\.A\.", r"CIA\.", r"LTDA.", r"N\.I\.A\."
			expression = rf'(?:{w1}\s+{w2}\s+{w3}|{w2}\s+{w3}\s+{w1}|{w3}\s+{w1}\s+{w2}|{w4}\s+{w2}\s+{w3}|{w2}\s+{w3}\s+{w4}|{w3}\s+{w4}\s+{w2}|{w1}\s+{w2}\s+{w3}|{w2}\s+{w3}\s+{w1}|{w3}\s+{w1}\s+{w2}|{w4}\s+{w2}\s+{w3}|{w2}\s+{w3}\s+{w4}|{w3}\s+{w4}\s+{w2})'

		elif self.empresaInfo ['id'] == 'BYZA':
			expression = r"(Byza)|(By\s*za\s*soluciones\s*(que\s*)*facilitan\s*tu\s*vida)"
		else:
			return text

		pattern = re.compile (expression)
		text = re.sub (pattern, '', text)

		return text.strip()

	#-----------------------------------------------------------
	#-- Extract only the needed info from text for each 'empresa'
	#-----------------------------------------------------------
	def getMercanciaDescripcion (self, descripcion):
		if self.empresaInfo ['id'] == "BYZA":
			if self.docType == "CARTAPORTE":   # Before "---" or CEC##### or "\n"
				pattern = r'((---+|CEC|\n\n).*)$'
				descripcion = re.sub (pattern, "", descripcion, flags=re.DOTALL)

			elif self.docType == "MANIFIESTO": # Before "---" or CPI: ###-###
				pattern = r'((---+|CPI:|CPIC:|\n\n).*)$'
				descripcion = re.sub (pattern, "", descripcion, flags=re.DOTALL)

		return descripcion.strip()

	#----------------------------------------------------------------
	#-- Create CODEBIN fields from document fields using input parameters
	#----------------------------------------------------------------
	def getCodebinFields (self):
		try:
			inputsParams = ResourceLoader.loadJson ("docs", self.inputsParametersFile)
			codebinFields = {}
			for key in inputsParams:
				ecudocsField  = inputsParams [key]["ecudocsField"]
				codebinField  = inputsParams [key]["codebinField"]
				#print ("-- key:", key, " dfield:", ecudocsField, "cfield: ", codebinField)
				if codebinField:
					value = self.getDocumentFieldValue (ecudocsField, "CODEBIN")
					codebinFields [codebinField] = value

			return codebinFields
		except Exception as e:
			Utils.printException ("Creando campos de CODEBIN")
			return None

	#----------------------------------------------------------------
	# Create ECUAPASSDOCS fields from document fields using input parameters
	#----------------------------------------------------------------
	def getEcuapassFormFields (self):
		try:
			inputsParams = ResourceLoader.loadJson ("docs", self.inputsParametersFile)
			formFields = {}
			for key in inputsParams:
				docField   = inputsParams [key]["ecudocsField"]
				if docField == "" or "OriginalCopia" in docField:
					continue
				else:
					value = self.getDocumentFieldValue (docField)
					formFields [key] = value

			return formFields
		except Exception as e:
			Utils.printException ("Creando campos de ECUAPASSDOCS")
			return None

	#-----------------------------------------------------------
	# Get value for document field 
	#-----------------------------------------------------------
	def getDocumentFieldValue (self, docField, appName=None):
		value = None
		# For ecudocs is "CO" but for codebin is "colombia"
		if "00_Pais" in docField:
			paises     = {"CO":"CO", "EC":"EC", "PE":"PE"}
			if appName == "CODEBIN":
				paises     = {"CO":"colombia", "EC":"ecuador", "PE":"peru"}

			codigoPais = self.fields [docField]["value"]
			value      =  paises [codigoPais]

		# In PDF docs, it is a check box marker with "X"
		elif "Carga_Tipo" in docField and not "Descripcion" in docField and self.docType == "MANIFIESTO":
			fieldValue = self.fields [docField]["value"]
			value = "X" if "X" in fieldValue.upper() else ""

		else:
			value = self.fields [docField]

		return value

	#------------------------------------------------------------------
	#-- get MRN according to empresa and docField
	#------------------------------------------------------------------
	def getMRN (self):
		print (f"+++ getMRN no implementado para '{self.empresa}'")
		return "||LOW"


	#------------------------------------------------------------------
	# Get bultos info for CPI and MCI with differnte ecuapass fields
	#------------------------------------------------------------------
	def getBultosInfo (self, ecuapassFields, analysisType="BOT"):
		bultosInfo = Utils.createEmptyDic (["cantidad", "embalaje", "marcas", "descripcion"])
		cantidadField    = ecuapassFields ["cantidad"]
		marcasField      = ecuapassFields ["marcas"]
		descripcionField = ecuapassFields ["descripcion"]
		try:
			# Cantidad
			text                    = self.fields [cantidadField]
			bultosInfo ["cantidad"] = Extractor.getNumber (text)
			bultosInfo ["embalaje"] = Extractor.getTipoEmbalaje (text, analysisType)

			# Marcas 
			bultosInfo ["marcas"] = self.getMarcasText (marcasField)

			# Descripcion
			descripcion = self.fields [descripcionField]
			descripcion = self.cleanWaterMark (descripcion)
			bultosInfo ["descripcion"] = self.getMercanciaDescripcion (descripcion)
		except:
			Utils.printException ("Obteniendo información de 'Bultos'", text)
		return bultosInfo


	#-- Get mercancia marcas from CPI field or MCI field
	#-- Overwritten in ALDIA subclass
	def getMarcasText (self, marcasField):
		text = self.fields [marcasField]
		return "SIN MARCAS" if text == "" else text

		
	#---------------------------------------------------------------- 
	# Return box coordinates from PDF document (CPI or MCI)
	# Coordinates file is defined in each subclass
	#---------------------------------------------------------------- 
	def getPdfCoordinates (self, pdfFilepath=None):
		coords_CPI_MCI = ResourceLoader.loadJson ("docs", self.coordinatesFile)
		coords   = coords_CPI_MCI [self.docType]
		return coords

