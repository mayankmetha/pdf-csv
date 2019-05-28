import PyPDF2
from pdf2image import convert_from_path
import os
import re
from PIL import Image
import sys
import pyocr
import pyocr.builders

images = []
texts1 = []
texts2 = []

# plain text pdf text extraction
def simplePDFTextExtract(filename,fout):
    pdf_file = open(filename, "rb")
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    f = open(fout, "wb")
    for page in range(number_of_pages):
        f.write(read_pdf.getPage(page).extractText().encode('utf-8'))
    f.close()
    pdf_file.close()

# pdf ocr text extraction
def PDFOCR(filename):
    for _ in os.listdir('tmp/ppm'):
        os.remove(os.path.join('tmp/ppm', _))
    for _ in os.listdir('tmp/jpg'):
        os.remove(os.path.join('tmp/jpg', _))
    for _ in os.listdir('tmp/txt1'):
        os.remove(os.path.join('tmp/txt1', _))
    for _ in os.listdir('tmp/txt2'):
        os.remove(os.path.join('tmp/txt2', _))
    pages = convert_from_path(filename,dpi=500,output_folder='tmp/ppm',thread_count=4)
    i = 0
    for p in pages:
        out = 'tmp/jpg/page'+str(i)+'.jpg'
        p.save(out,'JPEG')
        images.append(out)
        i += 1

# image to ocr
def imgOCR(imageFile):
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    tool = tools[0]
    txt = tool.image_to_string(
        Image.open(imageFile),
        lang='eng',
        builder=pyocr.builders.TextBuilder()
    )
    return (txt.strip())

# extract images from pdf
def extractImage(f):
    pdfFile = PyPDF2.PdfFileReader(open(f, "rb"))
    pages = PyPDF2.PdfFileReader(pdfFile)
    for p in range(pages):
        page0 = pdfFile.getPage(p)
        if '/XObject' in page0['/Resources']:
            xObject = page0['/Resources']['/XObject'].getObject()
            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                    data = xObject[obj].getData()
                    if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                        mode = "RGB"
                    else:
                        mode = "P"
                    if '/Filter' in xObject[obj]:
                        if xObject[obj]['/Filter'] == '/FlateDecode':
                            img = Image.frombytes(mode, size, data)
                            img.save("images/"+obj[1:] + ".png")
                        elif xObject[obj]['/Filter'] == '/DCTDecode':
                            img = open("images/"+obj[1:] + ".jpg", "wb")
                            img.write(data)
                            img.close()
                        elif xObject[obj]['/Filter'] == '/JPXDecode':
                            img = open("images/"+obj[1:] + ".jp2", "wb")
                            img.write(data)
                            img.close()
                        elif xObject[obj]['/Filter'] == '/CCITTFaxDecode':
                            img = open("images/"+obj[1:] + ".tiff", "wb")
                            img.write(data)
                            img.close()
                    else:
                        img = Image.frombytes(mode, size, data)
                        img.save("images/"+obj[1:] + ".png")
        else:
            print("No image found.")

f = sys.argv[1]
PDFOCR(f)
fileOut = sys.argv[2]
# convert txt to csv
pg = 0
for i in images:
    txt = imgOCR(i)
    f = 'tmp/txt1/'+str(pg)+'.txt'
    texts1.append(f)
    fout = open(f,'w')
    for _ in txt:
        fout.write(_)
    pg += 1
    fout.close()

pg = 0
for i in texts1:
    f = 'tmp/txt2/'+str(pg)+'.txt'
    texts2.append(f)
    fout = open(f,'w')
    fin = open(texts1[pg],'r')
    for _ in fin.readlines():
        if re.findall('^[ \t\n]+$',_):
            pass
        else:
            fout.write(_)
    pg += 1
    fin.close()
    fout.write("\n")
    fout.close() 

fout = open(fileOut,'w')
fout.write("page,line,content\n")
i = 1
for _ in texts2:
    lineNo = 1
    fin = open(_,'r')
    for lines in fin.readlines():
        fout.write(str(i)+","+str(lineNo)+","+lines)
        lineNo += 1
    fin.close()
    i += 1
fout.close()
#extractImage(f)