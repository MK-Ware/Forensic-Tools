from zipfile import BadZipFile, ZipFile
import os, sys, optparse
import lxml.etree as tree
from datetime import datetime as dt
from common_methods import *
try:    
    from PyPDF2 import PdfFileReader
except ImportError:
    sys.exit("PyPDF2 module not found... to install it use the command: pip install PyPDF2")


def compMetaData(file_path, save=True):
    '''Get common document metadata, takes 2 arguments, file_path and save (boolean, default is True)'''
    metadata = "Time: %d/%d/%d %d : %d : %d. Found the following metadata for the file %s:\n\n" % (now.year, now.month,
                                                                                                   now.day, now.hour, now.minute,
                                                                                                   now.second, file_name[:-4])
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
        last_modifier = "Could not get last modifier... File format not supported!"
        creation_time = "Could not get creation time... File format not supported!"
        xml_mod_time = "Could not get xml modification time... File format not supported!"

    stats = os.stat(file_path)
    c_time = dt.fromtimestamp(stats.st_ctime)
    last_access_time = dt.fromtimestamp(stats.st_atime)
    last_mod_time = dt.fromtimestamp(stats.st_mtime)
    owner_user_id = stats.st_uid

    metadata += """Creator: %s\nLast Modified By: %s\nOwner User ID: %s\nLast metadata mod Time: %s\nCreation Time: %s
Last Modification Time: %s\nXML Modification Time: %s\nLast Access Time: %s""" % (creator, last_modifier, owner_user_id,
                                                                                  c_time, creation_time,
                                                                                  last_mod_time, xml_mod_time,
                                                                                  last_access_time)

    print(metadata)

    if save:
        file_name = getFileName(file_path)
        tgt = file_name + ".txt"

        saveResult(tgt, metadata)

def pretifyPyPDF2Time(key, val):
    '''Make PyPDF2 time code more readable'''
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
    '''Get PDF document metadata, takes 2 arguments, file_path and save (boolean, default is True)'''
    pdf_doc = PdfFileReader(open(file_path, "rb"))

    if pdf_doc.isEncrypted:
        if pdf_doc.decrypt("") != 1:
            sys.exit("target pdf document is encrypted... exiting...")

    doc_info = pdf_doc.getDocumentInfo()
    stats = os.stat(file_path)
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
