#!/usr/bin/env python
import sys, os, optparse
from PIL import Image
from PIL.ExifTags import TAGS
from common_tools import *


def getExif(image_file, save=True, verbose=True):
    '''Get image file EXIF metadata'''
    if not os.path.isfile(image_file):
        sys.exit("%s is not a valid image file!")
    data = "Time: %d/%d/%d %d : %d : %d. Found the following Exif data for the image %s:\n\n" % (now.year, now.month,
                                                                                                 now.day, now.hour, now.minute,
                                                                                                 now.second, name)
    img = Image.open(image_file)
    info = img._getexif()
    exif_data = {}
    if info:
        for (tag, value) in info.items():
            decoded = TAGS.get(tag, tag)
            if type(value) is bytes:
                try:
                    exif_data[decoded] = value.decode("utf-8")
                except:
                    pass
            else:
                exif_data[decoded] = value
    else:
        sys.exit("No EXIF data found!")

    for key in exif_data:
        data += "{}    :   {}\n".format(key, exif_data[key])

    if save:
        name = getFileName(image_file)
        tgt = name + ".txt"
        saveResult(tgt, data)

    if verbose:
        print("Found the following exif data:\n", data)

if __name__ == "__main__":
    print('\n\n    ##########A simple Python script to extract exif metadata #########')
    print('    #                      Coded by monrocoury                        #')
    print('    #                most images contain Exif Metadata                #')
    print('    #               for more info refer to Google/wiki                #')
    print('    ###################################################################\n\n')
    parser = optparse.OptionParser("Usage: python exif_extractor.py -i <image path> -s <True or False> -v <True or False>")
    parser.add_option("-i", dest="image_path", type="string", help="provide the full path to the image file. eg: E:\images\img_1.jpg")
    parser.add_option("-s", dest="save", type="string", help="(optional) save the exif data as a text file? default True")
    parser.add_option("-v", dest="verbose", type="string", help="(optional) if False results won't be displayed in the console. default True")

    (options, args) = parser.parse_args()

    path = options.image_path
    if not path:
        print("please provide the path to the image file!")
        sys.exit(parser.usage)

    save = options.save
    if not save:
        save = True
    else:
        save = eval(save.title())

    verbose = options.verbose
    if not verbose:
        verbose = False
    else:
        verbose = eval(verbose.title())

    getExif(path, save, verbose)
