# Class for checking proper values in ecuapass fields

class EcuChecing:
	#---------------------------------------------------------------- 
	# Create docFields from ecuFields
	#---------------------------------------------------------------- 
	def getCartaporteDocFieldsFromEcuFields (ecuFields):
		docFields = {}
		ef, df = ecuFields, docFields

		df ["id"] = ""
		df ["00_Numero"] = ef ["02_NumeroCPIC"]
		df ["00a_Pais"] = ""
		df ["01_Transportista"] = ""

		df ["02_Remitente"] = ef ["14_NombreRemitente"] + "\n" + 
		                      ef ["15_DireccionRemitente"] + "\n" +
							  ef ["10_PaisRemitente"] + "\n" +
							  ef ["11_TipoIdRemitente"] + ":" + ef ["12_NroIdRemitente"]

		df ["03_Destinatario"] = ef ["19_NombreDestinatario"] + "\n" + 
		                         ef ["20_DireccionDestinatario"] + "\n" +
							     ef ["16_PaisDestinatario"] + "\n" +
							     ef ["17_TipoIdDestinatario"] + ":" + ef ["12_NroIdDestinatario"]

		df ["04_Consignatario"] = ef ["24_NombreConsignatario"] + "\n" + 
		                          ef ["25_DireccionConsignatario"] + "\n" +
							      ef ["21_PaisConsignatario"] + "\n" +
							      ef ["22_TipoIdConsignatario"] + ":" + ef ["12_NroIdConsignatario"]


		df ["05_Notificado"] = ef ["26_NombreNotificado"] + "\n" + 
		                       ef ["27_DireccionNotificado"] + "\n" +
							   ef ["28_PaisNotificado"] + "\n" 

		df ["06_Recepcion"] = f'{ef ["30_CiudadRecepcion"]}-{3f["29_PaisRecepcion"]}. {ef ["31_FechaRecepcion"]}'
		df ["07_Embarque"]  = f'{ef ["33_CiudadEmbarque"]}-{3f["32_PaisEmbarque"]}. {ef ["34_FechaEmbarque"]}'
		df ["08_Entrega"]   = f'{ef ["36_CiudadEntrega"]}-{3f["35_PaisEntrega"]}. {ef ["37_FechaEntrega"]}'

		df ["09_Condiciones"] = ef ["38_CondicionesTransporte"] + "." + ef ["39_CondicionesPago"]

		df ["10_CantidadClase_Bultos"] = ef ["42_TotalBultos"] + "." + ef ["68_Embalaje"]

		df ["11_MarcasNumeros_Bultos"] = ef ["69_Marcas"]
		df ["12_Descripcion_Bultos"]   = ef ["79_DescripcionCarga"]
		df ["13a_Peso_Neto"]  = ef ["40_PesoNeto"]
		df ["13b_Peso_Bruto"] = ef ["41_PesoBruto"]
		df ["14_Volumen"]     = ef ["43_Volumen"]
		df ["15_Otras_Unidades"] = ef ["44_OtraUnidad"]
		df ["16_Incoterms"] = "%s. %s %s. %s-%s" % (
		    ef ["46_INCOTERM"], 
			ef ["45_PrecioMercancias"],
			ef ["47_TipoMoneda"],
			ef ["49_CiudadMercancia"]
			ef ["48_PaisMercancia"]
		)
		# Gastos Remitente
		df ["17_Gastos:ValorFlete,MontoRemitente"]      = ef ["50_GastosRemitente"]         
		df ["17_Gastos:Seguro,MontoRemitente"]          = ""
		df ["17_Gastos:OtrosGastos,MontoRemitente"]     = ef ["54_OtrosGastosRemitente"]   
		df ["17_Gastos:Total,MontoRemitente"]           = ef ["58_TotalRemitente"]        
		df ["17_Gastos:ValorFlete,MonedaRemitente"]     = "USD"
		df ["17_Gastos:Seguro,MonedaRemitente"]         = "USD"
		df ["17_Gastos:OtrosGastos,MonedaRemitente"]    = "USD"
		df ["17_Gastos:Total,MonedaRemitente"]          = "USD"

		# Gastos Destinatario
		df ["17_Gastos:ValorFlete,MontoDestinatario"]   = ef ["52_GastosDestinatario"]   
		df ["17_Gastos:Seguro,MontoDestinatario"]       = ""
		df ["17_Gastos:OtrosGastos,MontoDestinatario"]  = ef ["56_OtrosGastosDestinatario"] 
		df ["17_Gastos:Total,MontoDestinatario"]        = ef ["59_TotalDestinatario"] 
		df ["17_Gastos:ValorFlete,MonedaDestinatario"]  = "USD"
		df ["17_Gastos:Seguro,MonedaDestinatario"]      = "USD"
		df ["17_Gastos:OtrosGastos,MonedaDestinatario"] = "USD"
		df ["17_Gastos:Total,MonedaDestinatario"]       = "USD"

		# Valores finales
		df ["18_Documentos"] = ef ["60_DocsRemitente"]
		df ["19_Emision"] = "%s-%s. %s" % (
			ef ["61_FechaEmision"],
			ef ["62_PaisEmision"],
			ef ["63_CiudadEmision"]
		)
		df ["21_Instrucciones"] = ef ["64_Instrucciones"]
		df ["22_Observaciones"] = ef ["65_Observaciones"]
		df ["24_OriginalCopia"] = 

