#!/usr/bin/env python3
import sys, json
import pdfplumber
import fitz  # PyMuPDF

#--------------------------------------------------------------------
# 1. Detect Horizontal and Vertical Lines
# Extract the lines using pdfplumber and classify them:
#--------------------------------------------------------------------
class AAA:
	pass

def main ():
	fullTest ()

def simpleTest ():
	args = sys.argv
	pdfFile = "CPI-SANCHEZPOLO-061984-24.pdf"
	getPdfCoordinates (pdfFile)

def fullTest():
	args = sys.argv
	#pdfFile = "CPI-SANCHEZPOLO-061984-24.pdf"
	pdfFile = "MCI-SANCHEZPOLO-093125.pdf"

	pdf    = ScrapingPdf_SANCHEZPOLO_Manifiesto ()

	boxes  = pdf.getRawBoxesFromPdf (pdfFile)
	outPdf = pdf.drawBoxesOnPdf (pdfFile, boxes, WIDTH=3, COLORBOX=(1,0,0), COLORTEXT=(1,0.5,0.5))

	textBoxes = pdf.getDocumentBoxesFromPdf (boxes)
	pdf.drawBoxesOnPdf (outPdf, textBoxes, COLORBOX=(0,0,1), COLORTEXT=(0,0,1))

#--------------------------------------------------------------------
# Class for extracting coordinates from a PDF file based on its boxes
#--------------------------------------------------------------------
class ScrapingPdf_SANCHEZPOLO:
	#--------------------------------------------------------------------
	# Get from PDF coordinates where text is written (no labels)
	#--------------------------------------------------------------------
	def getPdfCoordinates (self, pdfFilepath):
		rawBoxes = self.getRawBoxesFromPdf (pdfFilepath)
		docBoxes = self.getDocumentBoxesFromPdf (rawBoxes)
		coords   = self.convertBoxesToCoords (docBoxes)

		jsonFilename = pdfFilepath.split (".")[0] + "-COORDS.json"
		json.dump (coords, open (jsonFilename, "w"), indent=4)

		return coords

	#--------------------------------------------------------------------
	# Get raw (all detected) boxes from PDF file
	#--------------------------------------------------------------------
	def getRawBoxesFromPdf (self, pdf_path):
		doc = fitz.open(pdf_path)
		page = doc[0]

		# Retrieve all drawing commands
		shapes = page.get_drawings()

		boxes = []
		for k, shape in enumerate (shapes):
			for i, item in enumerate (shape["items"]):
				if item[0] == "re":	# Check if the item is a line
					boxes.append (item [1])
		return boxes

	#--------------------------------------------------------------------
	# Convert boxes (Rect type) to coords: x, y, width, height
	#--------------------------------------------------------------------
	def convertBoxesToCoords (self, boxes):
		coords = {}
		for k, v in boxes.items ():
			if not v:
				continue
			coords [k] = [int (x) for x in [v[0],v[1],v[2]-v[0]+1,v[3]-v[1]+1]]
		return coords

	#--------------------------------------------------------------------
	# Get box region containing the specific type of document text
	#--------------------------------------------------------------------

	def boxSimple (self, box):
		return (box)

	def boxLabel (self, box, nLines=1):
		box [1] += 9*nLines
		return (box)

	def boxMercancia (self, boxTop, boxBottom):
		box = (boxTop [0], boxTop [3], boxTop [2], boxBottom [1]-30)
		return (box)

	def boxIncoterms (self, boxTop1, boxTop2, boxBottom):
		box = (boxTop1 [0], boxTop1 [3] + 18, boxTop2 [2], boxBottom [1])
		return (box)

	def boxGastos (self, boxTop, rowNumber):
		rowSize = 24 if rowNumber !=3 else 14
		rowPos  = boxTop[3] + rowNumber * 24
		box = (boxTop [0], rowPos , boxTop [2], rowPos + rowSize)
		return (box)

	def boxMRN (self, left, right, bottom):
		box = (left [0], bottom [1]-30, right [2], bottom [1]) 
		return box

	def boxTipoCarga (self, top, bottom):
		offset = (top [2]-top[0]) / 4
		box = top [2]-offset, top [3], top [2], bottom [1]
		return box

	def boxEmpty (self, box):
		box [1] += 9
		return (box)

	#--------------------------------------------------------------------
	#--------------------------------------------------------------------
	def saveTxtCoords (self, textBoxes, filename):
		outFilename = f"{filename.split('.')[0]}-coordinates.txt"
		outFile = open (outFilename, "w")
		for k,v in textBoxes.items ():
			v = [int (x) for x in v]
			name = k.replace ("txt", "")
			outFile.write (f"{name}:{v[0]},{v[1]},{v[2]},{v[3]}\n")
		outFile.close ()
	#--------------------------------------------------------------------
	#--------------------------------------------------------------------
	def printBoxes (self, boxes):
		for i, box in enumerate (boxes):
			print (f"Box {i} : {box}")
			print ("")

	#--------------------------------------------------------------------
	# Draw the box rectangle from box Rect x1,y1,x2,y2
	#--------------------------------------------------------------------
	def drawBoxesOnPdf (self, pdfFilename, boxes, WIDTH=1, COLORBOX=(0,0,1), COLORTEXT=(1,0,1)):
		if type (boxes) is list:
			boxes = {str (i):x for i,x in enumerate (boxes)}

		# Open the PDF
		output_pdf  = pdfFilename.split (".")[0] + "-BOXES.pdf"

		pdf_document = fitz.open(pdfFilename)

		# Draw a rectangle on the first page
		page = pdf_document[0]
		for k, box in boxes.items():
			if not box:
				continue
			text = str (k).zfill(2)
			rect = fitz.Rect (box)  # (x0, y0, x1, y1)
			print (f"+++ rect '{rect}'")
			page.draw_rect (rect, color=COLORBOX, width=WIDTH)  # Red border
			centerX = box [0] + (box[2]-box[0])/2
			centerY = 5 + box [1] + (box[3]-box[1])/2
			page.insert_text ((centerX, centerY), text, fontsize=16, color=COLORTEXT)  # Blue text
			#page.insert_text ((box[2]-55, box[3]-5), text, fontsize=16, color=COLORTEXT)  # Blue text

		# Save the modified PDF
		pdf_document.save(output_pdf)
		pdf_document.close()
		return output_pdf

#--------------------------------------------------------------------
# Scraping class for Manifiesto
#--------------------------------------------------------------------
class ScrapingPdf_SANCHEZPOLO_Manifiesto (ScrapingPdf_SANCHEZPOLO):
	#--------------------------------------------------------------------
	# Get document boxes (containing document text) from PDF file
	#--------------------------------------------------------------------
	def getDocumentBoxesFromPdf (self, boxes):
		b = boxes
		textBoxes = {}
		textBoxes ["txt0b"]     = self.boxLabel (b[5])
		textBoxes ["txt0a"]     = self.boxLabel (b[33])
		textBoxes ["txt00"]     = self.boxSimple (b[1])
		textBoxes ["txt01"]     = self.boxLabel (b[4])
		textBoxes ["txt02"]     = self.boxLabel (b[5])
		textBoxes ["txt03"]     = self.boxLabel (b[6])

		# Camion o Tracto Camion:
		textBoxes ["txt04"]     = self.boxLabel (b[9])
		textBoxes ["txt05"]     = self.boxLabel (b[10])
		textBoxes ["txt06"]     = self.boxLabel (b[11])
		textBoxes ["txt07"]     = self.boxLabel (b[12])
		textBoxes ["txt08"]     = self.boxLabel (b[13])

		# Unidad Carga:
		textBoxes ["txt09"]     = self.boxLabel (b[16])
		textBoxes ["txt10"]     = self.boxLabel (b[17])
		textBoxes ["txt11"]     = self.boxLabel (b[18])
		textBoxes ["txt12"]     = self.boxLabel (b[19])
		textBoxes ["txt13"]     = self.boxLabel (b[22])

		textBoxes ["txt14"]     = self.boxLabel (b[24])
		textBoxes ["txt15"]     = self.boxLabel (b[25])
		textBoxes ["txt16"]     = self.boxLabel (b[28])
		textBoxes ["txt17"]     = self.boxLabel (b[29])
		textBoxes ["txt18"]     = self.boxLabel (b[23])
		textBoxes ["txt19"]     = self.boxLabel (b[26])
		textBoxes ["txt20"]     = self.boxLabel (b[27])
		textBoxes ["txt21"]     = self.boxLabel (b[30])
		textBoxes ["txt22"]     = self.boxLabel (b[31])
		textBoxes ["txt23"]     = self.boxLabel (b[33])
		textBoxes ["txt24"]     = self.boxLabel (b[34])
		textBoxes ["txt25_0"]   = self.boxEmpty (b[38])
		textBoxes ["txt25_1"]   = self.boxSimple (b[56])
		textBoxes ["txt25_2"]   = self.boxSimple (b[58])
		textBoxes ["txt25_3"]   = self.boxSimple (b[60])
		textBoxes ["txt25_4"]   = self.boxSimple (b[62])
		textBoxes ["txt25_5"]   = self.boxTipoCarga (b[34],b[37])
		textBoxes ["txt26"]     = self.boxLabel (b[36])
		textBoxes ["txt27"]     = self.boxLabel (b[37])
		textBoxes ["txt28"]     = self.boxMercancia (b[38],b[46])
		textBoxes ["txt29"]     = self.boxMercancia (b[39],b[46])
		textBoxes ["txt30"]     = self.boxMercancia (b[40],b[46])
		textBoxes ["txt31"]     = self.boxMercancia (b[41],b[47])
		textBoxes ["txt32_1"]   = self.boxMercancia (b[44],b[48])
		textBoxes ["txt32_2"]   = self.boxSimple (b[48])
		textBoxes ["txt32_3"]   = self.boxMercancia (b[45],b[49])
		textBoxes ["txt32_4"]   = self.boxSimple (b[49])
		textBoxes ["txt33_1"]   = self.boxMercancia (b[43],b[50])
		textBoxes ["txt33_2"]   = self.boxSimple (b[50])

		# Incoterm
		textBoxes ["txt34"]     = self.boxLabel (b[46], nLines=0)

		textBoxes ["txt35"]     = self.boxLabel (b[51])
		textBoxes ["txt36"]     = self.boxLabel (b[54])
		textBoxes ["txt37"]     = self.boxLabel (b[52])
		textBoxes ["txt38"]     = self.boxLabel (b[53])
		textBoxes ["txt39"]     = self.boxEmpty (b[38])
		textBoxes ["txt40"]     = self.boxLabel (b[55])

		# Special fields
		textBoxes ["appMRN"]    = self.boxMRN (b[46], b[40], b[46])
		return textBoxes

#--------------------------------------------------------------------
# Scraping class for Cartaporte
#--------------------------------------------------------------------
class ScrapingPdf_SANCHEZPOLO_Cartaporte (ScrapingPdf_SANCHEZPOLO):
	#--------------------------------------------------------------------
	# Get document boxes (containing document text) from PDF file
	#--------------------------------------------------------------------
	def getDocumentBoxesFromPdf (self, boxes):
		b = boxes
		textBoxes = {}
		textBoxes ["txt0b"]     = self.boxSimple (b[1])
		textBoxes ["txt0a"]     = self.boxSimple (b[1])
		textBoxes ["txt00"]     = self.boxSimple (b[1])
		textBoxes ["txt01"]     = self.boxLabel (b[2])
		textBoxes ["txt02"]     = self.boxLabel (b[4])
		textBoxes ["txt03"]     = self.boxLabel (b[7])
		textBoxes ["txt04"]     = self.boxLabel (b[10])
		textBoxes ["txt05"]     = self.boxLabel (b[3])
		textBoxes ["txt06"]     = self.boxLabel (b[5])
		textBoxes ["txt07"]     = self.boxLabel (b[6])
		textBoxes ["txt08"]     = self.boxLabel (b[8])
		textBoxes ["txt09"]     = self.boxLabel (b[9])
		textBoxes ["txt10"]     = self.boxMercancia (b[11], b[19])
		textBoxes ["txt11"]     = self.boxMercancia (b[12], b[19])
		textBoxes ["txt12"]     = self.boxMercancia (b[13], b[19])
		textBoxes ["txt13_1"]   = self.boxLabel (b[15])
		textBoxes ["txt13_2"]   = self.boxLabel (b[16])
		textBoxes ["txt14"]     = self.boxLabel (b[17], 2)
		textBoxes ["txt15"]     = self.boxLabel (b[18], 2)
		textBoxes ["txt16"]     = self.boxIncoterms (b[17], b[18], b[20])
		textBoxes ["txt17_11"]  = self.boxGastos (b[22], 0)
		textBoxes ["txt17_12"]  = self.boxGastos (b[22], 1)
		textBoxes ["txt17_13"]  = self.boxGastos (b[22], 2)
		textBoxes ["txt17_14"]  = self.boxGastos (b[22], 3)

		textBoxes ["txt17_21"]  = self.boxGastos (b[23], 0)
		textBoxes ["txt17_22"]  = self.boxGastos (b[23], 1)
		textBoxes ["txt17_23"]  = self.boxGastos (b[23], 2)
		textBoxes ["txt17_24"]  = self.boxGastos (b[23], 3)
		
		textBoxes ["txt17_31"]  = self.boxGastos (b[24], 0)
		textBoxes ["txt17_32"]  = self.boxGastos (b[24], 1)
		textBoxes ["txt17_33"]  = self.boxGastos (b[24], 2)
		textBoxes ["txt17_34"]  = self.boxGastos (b[24], 3)

		textBoxes ["txt17_41"]  = self.boxGastos (b[25], 0)
		textBoxes ["txt17_42"]  = self.boxGastos (b[25], 1)
		textBoxes ["txt17_43"]  = self.boxGastos (b[25], 2)
		textBoxes ["txt17_44"]  = self.boxGastos (b[25], 3)

		textBoxes ["txt18"]     = self.boxLabel (b[27])
		textBoxes ["txt19"]     = self.boxLabel (b[29])
		textBoxes ["txt20"]     = self.boxLabel (b[30])
		textBoxes ["txt21"]     = self.boxLabel (b[20])
		textBoxes ["txt22"]     = self.boxSimple (b[28])
		textBoxes ["appMRN"]    = self.boxMRN (b[11], b[12], b[19])

		return textBoxes


#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == "__main__":
	main()
