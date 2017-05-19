from zipfile import BadZipFile, ZipFile
from olefile import OleFileIO
import os, sys, optparse
import lxml.etree as tree
from datetime import datetime as dt
from common_methods import *
try:
    from PyPDF2 import PdfFileReader
except ImportError:
    sys.exit("PyPDF2 module not found... to install it use the command: pip install PyPDF2")


def compMetaData(file_path, save=True):
    now = dt.now()
    file_name = getFileName(file_path)
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
    try:
        print(metadata)
    except UnicodeEncodeError:
        print("Console encoding can't decode the result. Enter chcp 65001 in the console and rerun the script.")

    if save:
        file_name = getFileName(file_path)
        tgt = file_name + ".txt"

        saveResult(tgt, metadata)

def oleMetaData(file_path, save=True):
    now = dt.now()
    file_name = getFileName(file_path)
    metadata = "Time: %d/%d/%d %d : %d : %d. Found the following metadata for file %s:\n\n" % (now.year, now.month,
                                                                                               now.day, now.hour, now.minute,
                                                                                               now.second, file_name[:-4])
    try:
        ole = OleFileIO(file_path)
        meta = ole.get_metadata()
        ole.close()
        author = meta.author.decode("latin-1")
        creation_time = meta.create_time.ctime()
        last_author = meta.last_saved_by.decode("latin-1")
        last_edit_time = meta.last_saved_time.ctime()
        last_printed = meta.last_printed.ctime()
        revisions = meta.revision_number.decode("latin-1")
        company = meta.company.decode("latin-1")
        creating_app = meta.creating_application.decode("latin-1")

        metadata += "Original Author: %s\nCreation Time: %s\nLast Author: %s\n" % (author, creation_time, last_author) \
                    + "Last Modification Time: %s\nLast Printed at: %s\Total Revisions: %s\n" % (last_edit_time, last_printed, revisions) \
                    + "Created with: %s\nCompany: %s" % (creating_app, company)

        try:
            print(metadata)
        except UnicodeEncodeError:
            print("Console encoding can't decode the result. Enter chcp 65001 in the console and rerun the script.")

        if save:
            file_name = getFileName(file_path)
            tgt = file_name + ".txt"

            saveResult(tgt, metadata)
            
    except OSError as e1:
        print("File not supported: %s" % e1)
    except FileNotFoundError:
        print("Specified file could not be found")

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
        try:
            if pdf_doc.decrypt("") != 1:
                sys.exit("target pdf document is encrypted... exiting...")
        except:
            sys.exit("target pdf document is encrypted with an unsupported algorithm... exiting...")

    doc_info = pdf_doc.getDocumentInfo()
    stats = os.stat(file_path)
    now = dt.now()
    file_name = getFileName(file_path)
    metadata = "Time: %d/%d/%d %d : %d : %d. Found the following metadata for file %s:\n\n" % (now.year, now.month,
                                                                                               now.day, now.hour, now.minute,
                                                                                               now.second, file_name[:-4])
    try:
        for md in doc_info:
            metadata += str(md[1:]) + " : " + pretifyPyPDF2Time(str(md[1:]) ,str(doc_info[md])) + "\n"
    except TypeError:
        sys.exit("Couldn't read document info! Make sure target is a valid pdf document...")

    metadata += "Last metadata mod Date: %s\nLast Mod Date: %s\nLast Access Date: %s\nOwner User ID: %s" %(dt.fromtimestamp(stats.st_ctime),
                                                                                                           dt.fromtimestamp(stats.st_mtime),
                                                                                                           dt.fromtimestamp(stats.st_atime),
                                                                                                           stats.st_uid)
    try:
        print(metadata)
    except UnicodeEncodeError:
        print("Console encoding can't decode the result. Enter chcp 65001 in the console and rerun the script.")

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
    parser = optparse.OptionParser("Usage: python %prog -p <file path> -s <True or False>")
    parser.add_option("-p", dest="file_path", type="string", help="provide the full path to the document. eg: E:\test.doc")
    parser.add_option("-s", dest="save", type="string", help="(optional) save the metadata as a text file? default True")

    (options, args) = parser.parse_args()

    path = options.file_path
    if not path:
        print("please provide the path to the document!")
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
    elif any(path.endswith(ext) for ext in (".doc", ".ppt", ".xls", ".pps")):
        oleMetaData(path, save)
    else:
        print("File extension not supported/recognized... Make sure the file has the correct extension...")
