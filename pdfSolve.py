#-*-coding=utf-8*-*
from reportlab.lib.pagesizes import portrait
from reportlab.pdfgen import canvas
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
import os


def printf(str):
    print('*' * 50)
    print(str)
    print('*' * 50)
 
def imgtopdf(input_paths, outputpath):
    (maxw, maxh) = Image.open(input_paths).size
    c = canvas.Canvas(outputpath, pagesize=portrait((maxw, maxh)))
    c.drawImage(input_paths, 0, 0, maxw, maxh)
    c.showPage()
    c.save()

def dirtopdf(input_paths):
    folder = os.path.exists(input_paths)
    if folder:
        files = os.listdir(input_paths)
        for file in files:
            imgtopdf(input_paths +'/' + file, input_paths + '/' + file.replace('.jpg', '.pdf'))

def merge_pdf(infileList, outfile):
    pdf_output = PdfFileWriter()
    for infile in infileList:
        #print infileList[infile]
        pdf_input = PdfFileReader(open(infileList[infile], 'rb'))
        page_count = pdf_input.getNumPages()
        for i in range(page_count):
            pdf_output.addPage(pdf_input.getPage(i))
    pdf_output.write(open(outfile, 'wb'))

def dir_merge_pdf(dir):
    pdfList = {}
    folder = os.path.exists(dir)
    if folder:
        files = os.listdir(dir)
        for file in files:
            if('.pdf' in file):
                pdfList[int(file.replace('.pdf',''))] = (dir + '/' + file)
        merge_pdf(pdfList, 'pdf/' + dir + '.pdf')
    printf('转换合成pdf完成')

if __name__ == '__main__':
    #dirtopdf('天黑请睁眼  所谓艺术的灵魂')
    dir_merge_pdf('天黑请睁眼  所谓艺术的灵魂')
