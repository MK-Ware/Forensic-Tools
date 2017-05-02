#!/usr/bin/env python
import sys, os, optparse
from datetime import datetime as dt
from PIL import Image
from PIL.ExifTags import TAGS

def getImgName(full_path):
    x = 0
    for i in range(len(full_path)):
        if full_path[i] in ("\\", "/"):
            x = i

    if any(char in full_path for char in ("\\", "/")):
        x += 1
    return full_path[x:]

def getExif(image_file, save=True, verbose=True):
    if not os.path.isfile(image_file):
        sys.exit("%s is not a valid image file!")
    now = dt.now()
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


    if save:
        name = getImgName(image_file)
        tgt = name + ".txt"

        if os.path.isfile(tgt):
            sys.exit("%s already exists! Rename or move that file to avoid losing your data!" % tgt)
        print("saving results to %s\n" % tgt)
        with open(name + ".txt", "w") as tf:
            print("Time: %d/%d/%d %d : %d : %d. Found the following Exif data for the image %s:\n" % (now.year, now.month,
                                                                                                     now.day, now.hour, now.minute,
                                                                                                     now.second, name), file=tf)
            for key in exif_data:
                print("{}    :   {}".format(key, exif_data[key]), file=tf)
    print("done! Results saved to %s...\n" % tgt)
    if verbose:
        print("Found the following exif data:\n")
        for key in exif_data:
            print("%s   :   %s" % (key, exif_data[key]))

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
