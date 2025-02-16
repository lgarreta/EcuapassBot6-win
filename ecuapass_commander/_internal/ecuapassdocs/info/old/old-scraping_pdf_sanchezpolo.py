#!/usr/bin/env python3
import sys, json
import pdfplumber
import fitz  # PyMuPDF

#--------------------------------------------------------------------
# 1. Detect Horizontal and Vertical Lines
# Extract the lines using pdfplumber and classify them:
#--------------------------------------------------------------------
def main ():
	fullTest ()

def simpleTest ():
	args = sys.argv
	pdfFile = "CPI-SANCHEZPOLO-061984-24.pdf"
	getPdfCoordinates (pdfFile)

def fullTest():
	args = sys.argv
	pdfFile = "CPI-SANCHEZPOLO-061984-24.pdf"

	boxes = getRawBoxesFromPdf (pdfFile)
	outPdf = drawBoxesOnPdf (pdfFile, boxes, WIDTH=3, COLORBOX=(1,0,0), COLORTEXT=(1,1,0))

	textBoxes = getDocumentBoxesFromPdf (boxes)
	#pdfFileBoxes = "CPI-SANCHEZPOLO-061984-24-BOXES.pdf"
	drawBoxesOnPdf (outPdf, textBoxes, COLORBOX=(0,0,1), COLORTEXT=(0,0,1))

	# Save txt coordinates
	saveTxtCoords (textBoxes, pdfFile)

#--------------------------------------------------------------------
# Get from PDF coordinates where text is written (no labels)
#--------------------------------------------------------------------
def getPdfCoordinates (pdfFilepath):
	print ("--------------------------------------------------------")
	rawBoxes = getRawBoxesFromPdf (pdfFilepath)
	docBoxes = getDocumentBoxesFromPdf (rawBoxes)
	coords   = convertBoxesToCoords (docBoxes)

	jsonFilename = pdfFilepath.split (".")[0] + "-COORDS.json"
	json.dump (coords, open (jsonFilename, "w"), indent=4)

	return coords

#--------------------------------------------------------------------
# Get raw (all detected) boxes from PDF file
#--------------------------------------------------------------------
def getRawBoxesFromPdf (pdf_path):
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
# Get document boxes (containing document text) from PDF file
#--------------------------------------------------------------------
def getDocumentBoxesFromPdf (boxes):
	b = boxes
	textBoxes = {}
	textBoxes ["txt0b"]     = boxSimple (b[1])
	textBoxes ["txt0a"]     = boxSimple (b[1])
	textBoxes ["txt00"]     = boxSimple (b[1])
	textBoxes ["txt01"]     = boxLabel (b[2])
	textBoxes ["txt02"]     = boxLabel (b[4])
	textBoxes ["txt03"]     = boxLabel (b[7])
	textBoxes ["txt04"]     = boxLabel (b[10])
	textBoxes ["txt05"]     = boxLabel (b[3])
	textBoxes ["txt06"]     = boxLabel (b[5])
	textBoxes ["txt07"]     = boxLabel (b[6])
	textBoxes ["txt08"]     = boxLabel (b[8])
	textBoxes ["txt09"]     = boxLabel (b[9])
	textBoxes ["txt10"]     = boxMercancia (b[11], b[19])
	textBoxes ["txt11"]     = boxMercancia (b[12], b[19])
	textBoxes ["txt12"]     = boxMercancia (b[13], b[19])
	textBoxes ["txt13_1"]   = boxLabel (b[15])
	textBoxes ["txt13_2"]   = boxLabel (b[16])
	textBoxes ["txt14"]     = boxLabel (b[17], 2)
	textBoxes ["txt15"]     = boxLabel (b[18], 2)
	textBoxes ["txt16"]     = boxIncoterms (b[17], b[18], b[20])
	textBoxes ["txt17_11"]  = boxGastos (b[22], 0)
	textBoxes ["txt17_12"]  = boxGastos (b[22], 1)
	textBoxes ["txt17_13"]  = boxGastos (b[22], 2)
	textBoxes ["txt17_14"]  = boxGastos (b[22], 3)

	textBoxes ["txt17_21"]  = boxGastos (b[23], 0)
	textBoxes ["txt17_22"]  = boxGastos (b[23], 1)
	textBoxes ["txt17_23"]  = boxGastos (b[23], 2)
	textBoxes ["txt17_24"]  = boxGastos (b[23], 3)
	
	textBoxes ["txt17_31"]  = boxGastos (b[24], 0)
	textBoxes ["txt17_32"]  = boxGastos (b[24], 1)
	textBoxes ["txt17_33"]  = boxGastos (b[24], 2)
	textBoxes ["txt17_34"]  = boxGastos (b[24], 3)

	textBoxes ["txt17_41"]  = boxGastos (b[25], 0)
	textBoxes ["txt17_42"]  = boxGastos (b[25], 1)
	textBoxes ["txt17_43"]  = boxGastos (b[25], 2)
	textBoxes ["txt17_44"]  = boxGastos (b[25], 3)

	textBoxes ["txt18"]     = boxLabel (b[27])
	textBoxes ["txt19"]     = boxLabel (b[29])
	textBoxes ["txt20"]     = boxLabel (b[30])
	textBoxes ["txt21"]     = boxLabel (b[20])
	textBoxes ["txt22"]     = boxSimple (b[28])
	textBoxes ["txt23"]     = boxMRN (b[11], b[12], b[19])

	return textBoxes

def convertBoxesToCoords (boxes):
	coords = {}
	for k, v in boxes.items ():
		coords [k] = [int (x) for x in [v[0],v[1],v[2]-v[0]+1,v[3]-v[1]+1]]
	return coords

#--------------------------------------------------------------------
#--------------------------------------------------------------------
def boxToCoords (box):
	return int (box [0]), int (box [1]), int (box [2]-box[0] + 1), int (box [3] - box [1] + 1)

def boxSimple (box):
	return (box)

def boxLabel (box, labelLines=1):
	box [1] += 9*labelLines
	return (box)

def boxMercancia (boxTop, boxBottom):
	box = (boxTop [0], boxTop [3], boxTop [2], boxBottom [1]-30)
	return (box)

def boxIncoterms (boxTop1, boxTop2, boxBottom):
	box = (boxTop1 [0], boxTop1 [3] + 18, boxTop2 [2], boxBottom [1])
	return (box)

def boxGastos (boxTop, rowNumber):
	rowSize = 24 if rowNumber !=3 else 14
	rowPos  = boxTop[3] + rowNumber * 24
	box = (boxTop [0], rowPos , boxTop [2], rowPos + rowSize)
	return (box)

def boxMRN (left, right, bottom):
	box = (left [0], bottom [1]-30, right [2], bottom [1]) 
	return box

#--------------------------------------------------------------------
#--------------------------------------------------------------------
def saveTxtCoords (textBoxes, filename):
	outFilename = f"{filename.split('.')[0]}-coordinates.txt"
	outFile = open (outFilename, "w")
	for k,v in textBoxes.items ():
		v = [int (x) for x in v]
		name = k.replace ("txt", "")
		outFile.write (f"{name}:{v[0]},{v[1]},{v[2]},{v[3]}\n")
	outFile.close ()
#--------------------------------------------------------------------
#--------------------------------------------------------------------
def printBoxes (boxes):
	for i, box in enumerate (boxes):
		print (f"Box {i} : {box}")
		print ("")

#--------------------------------------------------------------------
#--------------------------------------------------------------------
def drawBoxesOnPdf (pdfFilename, boxes, WIDTH=1, COLORBOX=(0,0,1), COLORTEXT=(1,0,1)):
	if type (boxes) is list:
		boxes = {str (i):x for i,x in enumerate (boxes)}

	# Open the PDF
	output_pdf  = pdfFilename.split (".")[0] + "-BOXES.pdf"

	pdf_document = fitz.open(pdfFilename)

	# Draw a rectangle on the first page
	page = pdf_document[0]
	for k, box in boxes.items():
		text = str (k).zfill(2)
		rect = fitz.Rect (box)  # (x0, y0, x1, y1)
		print (f"+++ rect '{rect}'")
		page.draw_rect (rect, color=COLORBOX, width=WIDTH)  # Red border
		page.insert_text ((box[0]+5, box[1]+15), text, fontsize=16, color=COLORTEXT)  # Blue text

	# Save the modified PDF
	pdf_document.save(output_pdf)
	pdf_document.close()
	return output_pdf

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == "__main__":
	main()
