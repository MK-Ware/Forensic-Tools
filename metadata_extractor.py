#!/usr/bin/env python
from zipfile import BadZipFile, ZipFile
import os, sys, optparse
import lxml.etree as tree
from datetime import datetime as dt
try:    
    from PyPDF2 import PdfFileReader
except ImportError as e:
    sys.exit("PyPDF2 module not found... to install it use the command: pip install PyPDF2 %s" % e)



def getFileName(full_path):
    x = 0
    for i in range(len(full_path)):
        if full_path[i] in ("\\", "/"):
            x = i

    if any(char in full_path for char in ("\\", "/")):
        x += 1
    return full_path[x:]

def saveResult(file_name, metadata):
    if os.path.isfile(file_name):
            sys.exit("%s already exists! Rename or move that file to avoid losing your data!" % file_name)

    print("saving results to %s\n" % file_name)
    now = dt.now()

    with open(file_name, "w") as rf:
        print("Time: %d/%d/%d %d : %d : %d. Found the following metadata for the file %s:\n" % (now.year, now.month,
                                                                                             now.day, now.hour, now.minute,
                                                                                             now.second, file_name[:-4]), file=rf)
        print(metadata, file=rf)
    print("done! Results saved to %s...\n" % file_name)

def compMetaData(file_path, save=True):
    try:
        f = ZipFile(file_path)
        doc = tree.fromstring(f.read("docProps/core.xml"))

        ns = {'dc': 'http://purl.org/dc/elements/1.1/'}
        ns2 = {'dcterms': 'http://purl.org/dc/terms/'}
        ns3 = {'cp' : 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties'}
        
        creator = doc.xpath('//dc:creator', namespaces=ns)[0].text
        last_modifier = doc.xpath('//cp:lastModifiedBy', namespaces=ns3)[0].text
        creation_time = doc.xpath('//dcterms:created', namespaces=ns2)[0].text
        xml_mod_time = doc.xpath('//dcterms:modified', namespaces=ns2)[0].text

    except BadZipFile:
        creator = "Could not get creator... File format not supported!"

    stats = os.stat(file_path)
    c_time = dt.fromtimestamp(stats.st_ctime)
    last_access_time = dt.fromtimestamp(stats.st_atime)
    last_mod_time = dt.fromtimestamp(stats.st_mtime)
    owner_user_id = stats.st_uid

    metadata = """Creator: %s\nLast Modified By: %s\nOwner User ID: %s\nLast metadata mod Time: %s\nCreation Time: %s
Last Modification Time: %s\nXML Modification Time: %s\nLast Access Time: %s""" % (creator, last_modifier, owner_user_id,
                                                                                  c_time, creation_time,
                                                                                  last_mod_time, xml_mod_time,
                                                                                  last_access_time)

    print("Found the following metadata:\n\n" + metadata)

    if save:
        file_name = getFileName(file_path)
        tgt = file_name + ".txt"

        saveResult(tgt, metadata)

def pretifyPyPDF2Time(key, val):
    if "D:" in val and "Date" in key:
        temp = list(val)
        temp.insert(6, "-")
        temp.insert(9, "-")
        temp.insert(12, "  ")
        temp.insert(15, ":")
        temp.insert(18, ":")
        return "".join(temp)
    else:
        return val

def pdfMetaData(file_path, save=True):
    pdf_doc = PdfFileReader(open(file_path, "rb"))

    if pdf_doc.isEncrypted:
        sys.exit("target pdf document is encrypted... exiting...")

    doc_info = pf.getDocumentInfo()
    metadata = ""
    for md in doc_info:
        metadata += str(md[1:]) + " : " + pretifyPyPDF2Time(str(md[1:]) ,str(doc_info[md])) + "\n"

    metadata += "Last metadata mod Date: %s\nLast Mod Date: %s\nLast Access Date: %s\nOwner User ID: %s" %(dt.fromtimestamp(stats.st_ctime),
                                                                                                           dt.fromtimestamp(stats.st_mtime),
                                                                                                           dt.fromtimestamp(stats.st_atime),
                                                                                                           stats.st_uid)
    print(metadata)

    if save:
        file_name = getFileName(file_path)
        tgt = file_name + ".txt"

        saveResult(tgt, metadata)

if __name__ == "__main__":
    print('\n\n    ##########A simple Python script to extract document metadata #########')
    print('    #                      Coded by monrocoury                            #')
    print('    #                most documents contain Metadata                      #')
    print('    #               for more info refer to Google/wiki                    #')
    print('    #######################################################################\n\n')
    parser = optparse.OptionParser("Usage: python metadata_extractor.py -p <file path> -s <True or False>")
    parser.add_option("-p", dest="file_path", type="string", help="provide the full path to the image file. eg: E:\images\img_1.jpg")
    parser.add_option("-s", dest="save", type="string", help="(optional) save the exif data as a text file? default True")

    (options, args) = parser.parse_args()

    path = options.file_path
    if not path:
        print("please provide the path to the image file!")
        sys.exit(parser.usage)

    save = options.save
    if not save:
        save = True
    else:
        save = eval(save.title())

    if any(path.endswith(ext) for ext in (".docx", ".pptx", ".xlsx", ".vsdx", "thmx", "xltx", ".potx", ".vtx", ".ppsx", ".pub", ".zip")):
        compMetaData(path, save)
    elif path.endswith(".pdf"):
        pdfMetaData(path, save)
    else:
        print("File extension not supported/recognized... Make sure the file has the correct extension...")
