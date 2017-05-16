#!/usr/bin/env python
import sys, re, optparse
try:
    from common_methods import *
except ImportError:
    sys.exit("Could not find common_methods.py... download the full toolkit from https://github.com/MonroCoury/Forensic_Tools")


def read_moz_cookies(cookies_db):
    '''Read mozilla firefox cookies. Takes one argument: the full path of the cookies sqlite database file'''
    command = "SELECT host, name, value FROM moz_cookies"
    res = pull_from_db(cookies_db, command)
    data = init_data("firefox_scanner Cookies", len(res)) + init_table_header("./templates/init_cookies_html.html")

    for row in res:
        host = str(row[0])
        name = str(row[1])
        value = str(row[2])
        line = "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (host, name, value)
        data += line

    data += close_table_html()
    file_name = getFileName(cookies_db)
    tgt = file_name + ".html"
    saveResult(tgt, data)

def read_moz_history(history_db, tm_min=0, tm_max=10000000000000, google=False, android=False):
    '''Read mozilla firefox history. Takes 4 argument:
history_db: the full path of the places sqlite database file
tm_min: the minimum visit timestamp, default value is 0
tm_max: the maximum visit timestamp, default value is 10000000000000
google: Look for google searches only? default value is False'''
    command = "SELECT url, datetime(visit_date/1000000, 'unixepoch'), title FROM moz_places, moz_historyvisits " \
              + "WHERE (visit_count > 0) AND (moz_places.id == moz_historyvisits.place_id) AND (visit_date/1000000 > %s AND visit_date/1000000 < %s);" % (tm_min, tm_max)
    if android:
        command = "SELECT url, datetime(date/1000, 'unixepoch'), title FROM history WHERE (visits > 0)" \
                  + " AND (date/1000 > %s AND date/1000 < %s);" % (tm_min, tm_max)
        if google:
            command = "SELECT query, datetime(date/1000, 'unixepoch') FROM searchhistory WHERE (visits > 0)" \
                  + " AND (date/1000 > %s AND date/1000 < %s);" % (tm_min, tm_max)
    res = pull_from_db(history_db, command)
    data = init_data("firefox_scanner History", len(res)) + init_table_header("./templates/init_history_html.html")

    for row in res:
        if google:
            if android:
                search = str(row[0])
                date = str(row[1])
                title = "Search"
            else:
                url = str(row[0])
                date = str(row[1])
                title = str(row[2])
                if "google" in url.lower():
                    r = re.findall(r'q=.*\&', url)
                    if r:
                        search = r[0].split('&')[0]
                        search = search.replace('q=', '').replace('+', ' ')
            if not search == "":
                line = "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (date, title, search)
                data += line
        else:
            url = str(row[0])
            date = str(row[1])
            title = str(row[2])
            if len(title) == 0:
                title = url
            line = "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (date, title, url)
            data += line

    data += close_table_html()
    file_name = getFileName(history_db)
    tgt = file_name + ".html"
    saveResult(tgt, data)

def read_moz_forms(forms_db, tm_min=0, tm_max=10000000000000):
    '''Read mozilla firefox forms history. Takes 3 argument:
forms_db: the full path of the form_history sqlite database file
tm_min: the minimum form use timestamp, default value is 0
tm_max: the maximum form use timestamp, default value is 10000000000000'''
    command = "SELECT fieldname, value, timesUsed, datetime(firstUsed/1000000, 'unixepoch'), " \
              + "datetime(lastUsed/1000000, 'unixepoch') FROM moz_formhistory WHERE (firstUsed/1000000 > %s AND firstUsed/1000000 < %s);" % (tm_min, tm_max)
    res = pull_from_db(forms_db, command)
    data = init_data("firefox_scanner Forms History", len(res)) + init_table_header("./templates/init_formhistory_html.html")
    for row in res:

        line = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (str(row[0]), str(row[1]),
                                                                                     str(row[2]), str(row[3]),
                                                                                     str(row[4]))
        data += line

    data += close_table_html()
    file_name = getFileName(forms_db)
    tgt = file_name + ".html"
    saveResult(tgt, data)

def read_moz_downloads(downloads_db, tm_min=0, tm_max=10000000000000):
    '''Read mozilla firefox downloads. Takes 3 argument:
forms_db: the full path of the downloads sqlite database file
tm_min: the minimum download timestamp, default value is 0
tm_max: the maximum download timestamp, default value is 10000000000000'''
    command = "SELECT name, source, datetime(endTime/1000000, 'unixepoch') FROM moz_downloads WHERE (endtime/1000000 > %s AND endtime/1000000 < %s);" % (tm_min, tm_max)
    res = pull_from_db(downloads_db, command)
    data = init_data("firefox_scanner Downloads", len(res)) + init_table_header("./templates/init_downloads_html.html")

    for row in res:
        line = "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (row[0], row[1], row[2])
        data += line

    data += close_table_html()
    file_name = getFileName(downloads_db)
    tgt = file_name + ".html"
    saveResult(tgt, data)

if __name__ == "__main__":
    print('\n\n    ##############A Python script to read firefox browser data ############')
    print('    #                      Coded by monrocoury                            #')
    print('    #              can read forms data, cookies, Google searches          #')
    print('    #                   and history to name a few                         #')
    print('    #######################################################################\n\n')

    parser = optparse.OptionParser("Usage: python %prog -t <target> -b <(optional) database path> --min_time <(optional) minimum entry time>" \
                                   + " --max_time <(optional) maximum entry time> --android <(optional) Target is a firefox android database?>" \
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
    android_help = "True if target database is a firefox android database. default False"
    parser.add_option("--android", dest="droid", type="string", help=android_help)
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

    try:
        android = eval(options.droid)
    except Exception:
        android = False

    if options.target.lower() == "cookies":
        if not db:
            db = get_firefox_db("cookies.sqlite")
        read_moz_cookies(db)
    elif options.target.lower() == "history":
        if not db:
            db = get_firefox_db("places.sqlite")
        read_moz_history(db, min_time, max_time, android=android, google=False)
    elif options.target.lower() == "google_searches":
        if not db:
            db = get_firefox_db("places.sqlite")
        read_moz_history(db, min_time, max_time, android=android, google=True)
    elif options.target.lower() == "forms_history":
        if not db:
            db = get_firefox_db("formhistory.sqlite")
        read_moz_forms(db, min_time, max_time)
    elif options.target.lower() == "downloads":
        if not db:
            db = get_firefox_db("downloads.sqlite")
        read_moz_downloads(db, min_time, max_time)
