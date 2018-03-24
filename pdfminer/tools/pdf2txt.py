#!/usr/bin/env python
import sys
import re
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter

# main
def translate(output, args):
    # debug option
    debug = 0
    # input option
    password = ''
    pagenos = set()
    maxpages = 0
    # output option
    outfile = None
    outtype = None
    imagewriter = None
    rotation = 0
    stripcontrol = False
    layoutmode = 'normal'
    codec = 'utf-8'
    pageno = 1
    scale = 1
    caching = True
    showpageno = True
    laparams = LAParams()
    outfile = output
    #
    PDFDocument.debug = debug
    PDFParser.debug = debug
    CMapDB.debug = debug
    PDFPageInterpreter.debug = debug
    #
    rsrcmgr = PDFResourceManager(caching=caching)
    if not outtype:
        outtype = 'text'
        if outfile:
            if outfile.endswith('.htm') or outfile.endswith('.html'):
                outtype = 'html'
            elif outfile.endswith('.xml'):
                outtype = 'xml'
            elif outfile.endswith('.tag'):
                outtype = 'tag'
    if outfile:
        outfp = file(outfile, 'w')
    else:
        outfp = sys.stdout
    if outtype == 'text':
        device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                               imagewriter=imagewriter)
    elif outtype == 'xml':
        device = XMLConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                              imagewriter=imagewriter,
                              stripcontrol=stripcontrol)
    elif outtype == 'html':
        device = HTMLConverter(rsrcmgr, outfp, codec=codec, scale=scale,
                               layoutmode=layoutmode, laparams=laparams,
                               imagewriter=imagewriter, debug=debug)
    elif outtype == 'tag':
        device = TagExtractor(rsrcmgr, outfp, codec=codec)
    else:
        return usage()
    fp = file(args, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos,
                                  maxpages=maxpages, password=password,
                                  caching=caching, check_extractable=True):
        page.rotate = (page.rotate+rotation) % 360
        interpreter.process_page(page)
    fp.close()
    device.close()
    outfp.close()
    return

if __name__ == '__main__':
    translate('captain.txt', 'pdfminer/tools/samples/1-Demo.pdf')
    f = open('captain.txt', 'r')
    contents = f.readlines()
    f.close()
    new = ''
    i = 0
    for line in contents:
        blank = False
        if (i < len(contents)-1):
            lastchar=" "
            for num in range(len(line)-1, -1, -1):
                lastchar=line[num]
                if lastchar != "\n" and lastchar != " ":
                    break
                    
            if (contents[i+1].strip("\n") == "" and lastchar != "." and lastchar != "!"):
                blank = True
                
        if (not blank):
            if (lastchar == "."  or lastchar == "!"):
                new += line
            elif (len(line) > 10):
                new += line                    
        i+=1
    new = new.replace('\n', ' ')
    new = new[:-1];
    new = [e+'.' for e in re.split("!\s|\.\s", new) if e]
    contents = ''
    for n in new:
        if (n[-2] != "?"):
            n = n.strip(" ")
            contents += n + '\n'
    t = open('captain-out.txt', 'w')
    t.write(contents)
    t.close()
