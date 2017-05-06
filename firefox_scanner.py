#!/usr/bin/env python
import sqlite3, os, sys, re, optparse
from datetime import datetime as dt
try:
    from common_methods import *
except ImportError:
    sys.exit("Could not find common_methods.py... download the full toolkit from https://github.com/MonroCoury/Forensic_Tools")


def read_moz_cookies(cookies_db):
    command = "SELECT host, name, value FROM moz_cookies"
    res = pull_from_db(cookies_db, command)
    data = init_data("firefox_scanner Cookies", len(res)) + "<thead>\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<th scope=\"col\">Host</th>\n\t\t\t\t\t\t" \
        + "<th scope=\"col\">Cookie</th>\n\t\t\t\t\t\t<th scope=\"col\">Value</th>\n\t\t\t\t\t\t" \
        + "</tr>\n\t\t\t\t</thead>\n\t\t\t\t<tbody>"
    
    for row in res:
        host = str(row[0])
        name = str(row[1])
        value = str(row[2])
        line = "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (host, name, value)
        data += line

    data += "</tbody></tablte></center></body></html>"
    file_name = getFileName(cookies_db)
    tgt = file_name + ".html"
    saveResult(tgt, data)

def read_moz_history(history_db, tm_min=0, tm_max=10000000000000, google=False):
    command = "SELECT url, datetime(visit_date/1000000, 'unixepoch') FROM moz_places, moz_historyvisits " \
              + "WHERE (visit_count > 0) AND (moz_places.id == moz_historyvisits.place_id) AND (visit_date/1000000 > %s AND visit_date/1000000 < %s);" % (tm_min, tm_max)
    res = pull_from_db(history_db, command)
    data = init_data("firefox_scanner History", len(res)) + "<thead>\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<th scope=\"col\">Date</th>\n\t\t\t\t\t\t" \
        + "<th scope=\"col\">URL / Search Term</th>\n\t\t\t\t\t\t" \
        + "</tr>\n\t\t\t\t</thead>\n\t\t\t\t<tbody>"

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
                        line = "<tr><td>%s</td><td>%s</td></tr>" % (date, search)
                        data += line
        else:
            line = "<tr><td>%s</td><td>%s</td></tr>" % (date, url)
            data += line

    data += "</tbody></tablte></center></body></html>"
    file_name = getFileName(history_db)
    tgt = file_name + ".html"
    saveResult(tgt, data)

def read_moz_forms(forms_db, tm_min=0, tm_max=10000000000000):
    command = "SELECT fieldname, value, timesUsed, datetime(firstUsed/1000000, 'unixepoch'), " \
              + "datetime(lastUsed/1000000, 'unixepoch') FROM moz_formhistory WHERE (firstUsed/1000000 > %s AND firstUsed/1000000 < %s);" % (tm_min, tm_max)
    res = pull_from_db(forms_db, command)
    data = init_data("skype_scanner Forms History", len(res)) + "<thead>\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<th scope=\"col\">Field Name</th>\n\t\t\t\t\t\t" \
        + "<th scope=\"col\">Value</th>\n\t\t\t\t\t\t<th scope=\"col\">Times Used</th>\n\t\t\t\t\t\t<th scope=\"col\">First Used</th>\n\t\t\t\t\t\t" \
        + "<th scope=\"col\">Last Used</th>\n\t\t\t\t\t</tr>\n\t\t\t\t</thead>\n\t\t\t\t<tbody>"
    for row in res:
        
        line = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (str(row[0]), str(row[1]),
                                                                                     str(row[2]), str(row[3]),
                                                                                     str(row[4]))
        data += line

    data += "</tbody></tablte></center></body></html>"
    file_name = getFileName(forms_db)
    tgt = file_name + ".html"
    saveResult(tgt, data)

def read_moz_downloads(downloads_db, tm_min=0, tm_max=10000000000000):
    command = "SELECT name, source, datetime(endTime/1000000, 'unixepoch') FROM moz_downloads WHERE (endtime/1000000 > %s AND endtime/1000000 < %s);" % (tm_min, tm_max)
    res = pull_from_db(downloads_db, command)
    now = dt.now()
    data = init_data("skype_scanner Forms History", len(res)) + "<thead>\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<th scope=\"col\">File Name</th>\n\t\t\t\t\t\t" \
        + "<th scope=\"col\">Source</th>\n\t\t\t\t\t\t<th scope=\"col\">Time</th>\n\t\t\t\t\t</tr>\n\t\t\t\t</thead>\n\t\t\t\t<tbody>"

    for row in res:
        line = "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (row[0], row[1], row[2])
        data += line
    
    data += "</tbody></tablte></center></body></html>"
    file_name = getFileName(downloads_db)
    tgt = file_name + ".html"
    saveResult(tgt, data)

if __name__ == "__main__":
    print('\n\n    ##############A Python script to read firefox browser data ############')
    print('    #                      Coded by monrocoury                            #')
    print('    #              can read forms data, cookies, Google searches          #')
    print('    #                   and history to name a few                         #')
    print('    #######################################################################\n\n')

    parser = optparse.OptionParser("Usage: python %prog -t <target> -b <(optional) database path>" \
                                   + " or python firefox_scanner.py -h for help")
    target_help = "can take one of 5 values: cookies, history, google_searches, forms_history, or downloads"
    parser.add_option("-t", dest="target", type="string", help=target_help)
    db_help = "The full path of the database file to parse. By default, if you're on linux go to" \
              + " /home/<username>/.mozilla/firefox/ choose the directory that ends with '.default'. once inside the folder" \
              + " copy the full path from the address bar and paste it as the -b argument. enclose the path in quotes if " \
              + "it contains spaces. The script will attempt to find the default database for the target function specified and the active user"
    parser.add_option("-b", dest="db", type="string", help=db_help)
    min_help = "enter if target isn't 'cookies' to read items after a given date and time, must be a string separated by _ YYYY_MM_DD_HH_MM_SS"
    parser.add_option("--min_time", dest="min", type="string", help=min_help)
    max_help = "enter if target isn't 'cookies' to read items before a given date and time, must be a string separated by _ YYYY_MM_DD_HH_MM_SS"
    parser.add_option("--max_time", dest="max", type="string", help=max_help)
    (options, args) = parser.parse_args()
    if not options.target:
        sys.exit("please enter a target:\n\n%s" % parser.usage)

    if options.target not in ("cookies", "history", "google_searches", "forms_history", "downloads"):
        sys.exit("Unrecognized target function!")

    db = options.db
    
    if options.min:
        min_time = time_to_epoch(options.min)
    else:
        min_time = 0
    if options.max:
        max_time = time_to_epoch(options.min)
    else:
        max_time = 10000000000000

    if options.target.lower() == "cookies":
        if not db:
            db = get_firefox_db("cookies.sqlite")
        read_moz_cookies(db)
    elif options.target.lower() == "history":
        if not db:
            db = get_firefox_db("places.sqlite")
        read_moz_history(db, min_time, max_time)
    elif options.target.lower() == "google_searches":
        if not db:
            db = get_firefox_db("places.sqlite")
        read_moz_history(db, min_time, max_time, google=True)
    elif options.target.lower() == "forms_history":
        if not db:
            db = get_firefox_db("formhistory.sqlite")
        read_moz_forms(db, min_time, max_time)
    elif options.target.lower() == "downloads":
        if not db:
            db = get_firefox_db("downloads.sqlite")
        read_moz_downloads(db, min_time, max_time)
