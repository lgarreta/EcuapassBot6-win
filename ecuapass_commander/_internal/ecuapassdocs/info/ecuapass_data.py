import os, re, importlib

from ecuapassdocs.info.ecuapass_utils import Utils
from ecuapassdocs.info.ecuapass_exceptions import IllegalEmpresaException

#from ecuapassdocs.info.ecuapass_info_BYZA import Cartaporte_BYZA, Manifiesto_BYZA

#-----------------------------------------------------------
#-- Class containing data for filling Ecuapass document
#-----------------------------------------------------------
class EcuData:
	temporalDir = None

	#-------------------------------------------------------------------
	# Create Doc Info Instance for "empresa" and "docType"
	#-------------------------------------------------------------------
	def createDocInfoInstance (docType, empresa, pais, runningDir):
		global Cartaporte_BYZA, Manifiesto_BYZA
		global Cartaporte_ALDIA, Manifiesto_ALDIA
		global Cartaporte_SANCHEZPOLO, Manifiesto_SANCHEZPOLO
		global Cartaporte_AGENCOMEXCARGO, Manifiesto_AGENCOMEXCARO
		global Cartaporte_LOGITRANS, Manifiesto_LOGITRANS
		global Cartaporte_RODFRONTE, Manifiesto_RODFRONTE
		global Cartaporte_ALCOMEXCARGO, Manifiesto_ALCOMEXCARGO

		empresaMatriz = Utils.getEmpresaMatriz (empresa)
		docType       = docType.capitalize () 
		#module        = importlib.import_module (f"ecuapassdocs.info.ecuapass_info_{empresaMatriz}")
		DOCINFOCLASS  = getattr (module, f"{docType}_{empresaMatriz}")
		return DOCINFOCLASS (docType, empresa, pais, runningDir)

	#-------------------------------------------------------------------
	#-------------------------------------------------------------------
	empresas = { 
		"AGENCOMEXCARGO" : { 
			"activa"     : True,
			'id'         : "AGENCOMEXCARGO",
			"nombre"     : "LOGISTICA Y TRANSPORTE AGENCOMEXCARGO S.A.",
			"direccion"  : "CDLA. ELOY ALFARO AV. MANABI No. 62018 Y AV. BRASIL",
			"idTipo"     : "RUC", 
			"idNumero"   : "0491516194001",
			"appType"    : "CODEBIN",
			"permisos"   : {"originario":"PO-EC-0037-21", "servicios1":"", "servicios2":""}
		},
		"RODFRONTE" : { 
			"activa"     : False,
			'id'         : "RODFRONTE",
			"nombre"     : "TRANSPORTE PESADO RODFRONTE S.A.",
			"direccion"  : "ARGENTINA Y JUAN LEON MERA - TULCAN",
			"idTipo"     : "RUC", 
			"idNumero"   : "1792600863001",
			"appType"    : "CODEBIN",
			"permisos"   : {"originario":"PO-EC-0108-24", "servicios1":None}
		},
		"SANCHEZPOLO": {
			"activa"   : True,
			'id'       : "SANCHEZPOLO",
			"nombre"   : "TRANSPORTES SANCHEZ POLO S.A",
			"direccion": "PAR LOGÍSTICO CALIFORNIA AV. CORDIALIDAD BG 30",
			"idTipo"   : "NIT", 
			"idNumero" : "890103161-1",
			"appType"  : "SANCHEZPOLO",
			"permisos" : {"originario":"PO-CO-0060-23", "servicios1":None}
		},
	
		"ALCOMEXCARGO" : { 
			"activa"     : False,
			'id'         : "ALCOMEXCARGO",
			"nombre"     : "TRANSPORTE DE CARGA NACIONAL E INTERNACIONAL ALCOMEXCARGO S.A.",
			"direccion"  : "CALLE AV. SAN FRANCISCO INT.: REMIGIO CRESPO TORAL REF.",
			"idTipo"     : "RUC", 
			"idNumero"   : "0491523638001",
			"appType"    : "CODEBIN",
			"permisos"   : {"originario":"PO-EC-0091-23", "servicios1":"", "servicios2":""}
		},
		"ALDIA": {
			"activa"   : True,
			'id'       : "ALDIA",
			"nombre"   : "ALDIA SAS",
			"direccion": "AV GALO PLAZA LASSO N 68-100 Y AVELLANEDAS",
			"idTipo"   : "RUC", 
			"idNumero" : "1791250060001",
			"appType"  : "ALDIA",
			"permisos" : {"originario":"PO-EC-0083-23", "servicios1":"P.P.S-CO-0196-09"}
		},
	
		"ALDIA::TRANSERCARGA": {
			"activa"   : True,
			'id'       : "ALDIA::TRANSERCARGA",
			"nombre"   : "TRANSERCARGA SAS",
			"direccion": "AV GALO PLAZA LASSO N 68-100 Y AVELLANEDAS",
			"idTipo"   : "RUC", 
			"idNumero" : "1791250060001",
			"appType"  : "ALDIA",
			"permisos" : {"originario":"PO-EC-0083-23", "servicios1":"P.P.S-CO-0196-09"}
		},
	
		"ALDIA::SERCARGA": {
			"activa"   : True,
			'id'       : "ALDIA::SERCARGA",
			"nombre"   : "SERCARGA SAS",
			"direccion": "AV GALO PLAZA LASSO N 68-100 Y AVELLANEDAS",
			"idTipo"   : "RUC", 
			"idNumero" : "1792006880001",
			"appType"  : "ALDIA",
			"permisos" : {"originario":"PO-CO-0018-21", "servicios1":"PO-CO-0018-21"}
		},

		"BYZA": {
			"activa"   : True,
			'id'       : "BYZA",
			"nombre"   : "Grupo BYZA S.A.S.",
			"direccion": "Av. Coral y los Alamos",
			"idTipo"   : "RUC", 
			"idNumero" : "0400201414001",
			"appType"  : "CODEBIN",
			"permisos" : {"originario":"PO-CO-0033-22", "servicios1": "PO-CO-0033-22"}
		},
		"LOGITRANS" : { 
			"activa"   : True,
			'id'       : "LOGITRANS",
			"nombre"   : "TRANSPORTES LOGITRANS-ACROS S.A.",
			"direccion": "CALDERON NRO. 63-052 Y URUGUAY",
			"idTipo"   : "RUC", 
			"idNumero" : "0491507748001",
			"appType"  : "CODEBIN",
			"permisos" : {"originario":"PO-EC-0005-20", "servicios1": "PO-EC-0005-20"}
		},
		"NTA" : { 
			"activa"   : False,
			'id'         : "NTA",
			"nombre"     : "NUEVO TRANSPORTE DE AMERICA COMPAÑIA LIMITADA", 
			"direccion"  : "ARGENTINA Y JUAN LEON MERA - TULCAN",
			"idTipo"     : "RUC", 
			"idNumero"   : "1791834461001",
			"appType"  : "CODEBIN",
			"permisos" : {"originario":"C.I.-E.C.-0060-04",
				          "servicios1":"P.P.S.CO015905", "servicios2":"P.P.S.PE000210"}
		}
	}

	configuracion = {
		"dias_cartaportes_recientes" : 4,
		"numero_documento_inicio" : 2000000,
		"num_zeros" : 5
	}

	procedureTypes = {"COLOMBIA":"IMPORTACION", "ECUADOR":"EXPORTACION", "PERU":"IMPORTACION"}

	def getEmpresaInfo (empresa):
		return EcuData.empresas [empresa]

	def getEmpresaId (empresa):
		return EcuData.empresas [empresa]["numeroId"]

	#----------------------------------------------------------------
	# Check if is a valid 'empresa' by validating 'permiso'
	#----------------------------------------------------------------
	def checkEmpresaPermisos (empresa, permisoText):
		try:
			empresaInfo   = EcuData.getEmpresaInfo (empresa)
			permiso       = empresaInfo ["permisos"]["originario"]
			if not permiso or permiso not in permisoText:
				raise IllegalEmpresaException (f"SCRAPERROR::Permiso empresa '{permiso}' desconocido!")

			if not empresaInfo ["activa"]:
				raise IllegalEmpresaException (f"SCRAPERROR::Empresa '{empresa} no está activa!")
		except Exception as ex:
			Utils.printException ()
			raise IllegalEmpresaException (f"SCRAPERROR::Problemas validando empresa: '{empresa}'!") from ex
#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	mainInfo ()
