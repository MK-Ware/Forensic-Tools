#!/usr/bin/env python
import sqlite3, os, sys, re, optparse
from datetime import datetime as dt
from common_methods import *


def read_moz_cookies(cookies_db, verbose=False, save=True):
    command = "SELECT host, name, value FROM moz_cookies"
    res = pull_from_db(cookies_db, command)
    now = dt.now()
    data = "Time: %d/%d/%d %d : %d : %d. Found %s cookies:\n" % (now.year, now.month,
                                                                 now.day, now.hour, now.minute,
                                                                 now.second, len(res))
    
    for row in res:
        host = str(row[0])
        name = str(row[1])
        value = str(row[2])
        line = "Host: %s\nCookie: %s\nValue: %s\n\n" % (host, name, value)
        data += line
    if verbose:
        try:
            print(data)
        except UnicodeEncodeError:
            os.system("chcp 65001")
            print(data)
    if save:
        file_name = getFileName(cookies_db)
        tgt = file_name + ".txt"
        saveResult(tgt, data)

def read_moz_history(history_db, verbose=False, save=True, google=False):
    command = "SELECT url, datetime(visit_date/1000000, 'unixepoch') FROM moz_places, moz_historyvisits " \
              + "WHERE visit_count > 0 and moz_places.id == moz_historyvisits.place_id;"
    res = pull_from_db(history_db, command)
    now = dt.now()
    data = "Time: %d/%d/%d %d : %d : %d. Found %s history activities:\n" % (now.year, now.month,
                                                                            now.day, now.hour, now.minute,
                                                                            now.second, len(res))

    for row in res:
        url = str(row[0])
        date = str(row[1])
        if google:
            if "google" in url.lower():
                r = re.findall(r'q=.*\&', url)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('q=', '').replace('+', ' ')
                    if not search == "":
                        line = "Date: %s\nSearched for: %s\n\n" % (date, search)
                        data += line
        else:
            line = "Date: %s\nVisited: %s\n\n" % (date, url)
            data += line
    if verbose:
        try:
            print(data)
        except UnicodeEncodeError:
            os.system("chcp 65001")
            print(data)
    if save:
        file_name = getFileName(history_db)
        tgt = file_name + ".txt"
        saveResult(tgt, data)

def read_moz_forms(forms_db, verbose=False, save=True):
    command = "SELECT fieldname, value, timesUsed, datetime(firstUsed/1000000, 'unixepoch'), " \
              + "datetime(lastUsed/1000000, 'unixepoch') from moz_formhistory;"
    res = pull_from_db(forms_db, command)
    now = dt.now()
    data = "Time: %d/%d/%d %d : %d : %d. Found %s forms:\n" % (now.year, now.month,
                                                               now.day, now.hour, now.minute,
                                                               now.second, len(res))
    for row in res:
        
        line = "Field Name: %s\nValue: %s\nTimes Used: %s\nFirst Used: %s\nLast Used: %s\n\n" % (str(row[0]), str(row[1]),
                                                                                                 str(row[2]), str(row[3]),
                                                                                                 str(row[4]))
        data += line
    if verbose:
        try:
            print(data)
        except UnicodeEncodeError:
            os.system("chcp 65001")
            print(data)
    if save:
        file_name = getFileName(forms_db)
        tgt = file_name + ".txt"
        saveResult(tgt, data)

def read_moz_downloads(downloads_db, verbose=False, save=True):
    command = "SELECT name, source, datetime(endTime/1000000, 'unixepoch') FROM moz_downloads;"
    res = pull_from_db(downloads_db, command)
    now = dt.now()
    data = "Time: %d/%d/%d %d : %d : %d. Found %s downloads:\n" % (now.year, now.month,
                                                                   now.day, now.hour, now.minute,
                                                                   now.second, len(res))

    for row in res:
        line = "File: %s - Source: %s - at: %s\n\n" % (row[0], row[1], row[2])
        data += line
    
    if verbose:
        try:
            print(data)
        except UnicodeEncodeError:
            os.system("chcp 65001")
            print(data)
    if save:
        file_name = getFileName(downloads_db)
        tgt = file_name + ".txt"
        saveResult(tgt, data)

if __name__ == "__main__":
    print('\n\n    ##############A Python script to read firefox browser data ############')
    print('    #                      Coded by monrocoury                            #')
    print('    #              can read forms data, cookies, Google searches          #')
    print('    #                   and history to name a few                         #')
    print('    #######################################################################\n\n')

    parser = optparse.OptionParser("Usage: python firefox_scanner.py -t <target> -b <database location>" \
                                   + " -v <verbose, True or False> -s <save, True or False> or python firefox_scanner.py -h for help")
    target_help = "can take one of 5 values: cookies, history, google_searches, forms_history, or downloads"
    parser.add_option("-t", dest="target", type="string", help=target_help)
    db_help = "The location of the database to parse. By default, if you're on linux go to" \
              + " /home/<username>/.mozilla/firefox/ choose the directory that ends with '.default'. once inside the folder" \
              + " copy the full path from the address bar and paste it as the -b argument. enclose the path in quotes if " \
              + "it contains spaces"
    parser.add_option("-b", dest="db", type="string", help=db_help)
    parser.add_option("-v", dest="verbose", type="string", help="show the result in the console screen")
    parser.add_option("-s", dest="save", type="string", help="save the result to a text file")
    (options, args) = parser.parse_args()
    if not options.target:
        sys.exit("please enter a target:\n\n%s" % parser.usage)

    if options.target not in ("cookies", "history", "google_searches", "forms_history", "downloads"):
        sys.exit("Unrecognized target function!")

    try:
        verbose = eval(options.verbose.title())
    except:
        verbose = False

    try:
        save = eval(options.save.title())
    except:
        save = True
    if options.target.lower() == "cookies":
        read_moz_cookies(os.path.join(options.db, "cookies.sqlite"), verbose, save)
    elif options.target.lower() == "history":
        read_moz_history(os.path.join(options.db, "places.sqlite"), verbose, save)
    elif options.target.lower() == "google_searches":
        read_moz_history(os.path.join(options.db, "places.sqlite"), verbose, save, google=True)
    elif options.target.lower() == "forms_history":
        read_moz_forms(os.path.join(options.db, "formhistory.sqlite"), verbose, save)
    elif options.target.lower() == "downloads":
        read_moz_downloads(os.path.join(options.db, "downloads.sqlite"), verbose, save)
