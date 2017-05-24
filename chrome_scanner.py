#!/usr/bin/env python
import optparse
from datetime import datetime as dt
try:
    from common_methods import *
except ImportError:
    sys.exit("Could not find common_methods.py... download the full toolkit from https://github.com/MonroCoury/Forensic_Tools")


def read_chrome_history(history_db, tm_min=0, tm_max=10000000000000, google=False):
    command = "SELECT urls.url, title, visit_time, last_visit_time, visit_count FROM urls, visits WHERE (urls.id = visits.id)" \
              + " AND ((visit_time/10000000) > %s AND (visit_time/10000000) < %s);" % (tm_min, tm_max)

    if google:
        command = "SELECT urls.url, title, visit_time, last_visit_time, visit_count FROM urls, visits WHERE (urls.id = visits.id)" \
              + " AND ((visit_time/10000000) > %s AND (visit_time/10000000) < %s) " % (tm_min, tm_max) \
              + "AND (title like '%Google%');"

    res = pull_from_db(history_db, command)
    data = init_data("chrome_scanner History", len(res)) + init_table_header("./templates/init_chrome_history_html.html")

    for row in res:
        visit_time = dt.fromtimestamp(row[2]/10000000)
        last_visit_time = dt.fromtimestamp(row[3]/10000000)

        line = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (visit_time, last_visit_time, row[1], row[0], row[4])
        data += line

    data += close_table_html()
    saveResult("chrome_history.html", data)

def read_chrome_downloads(history_db, tm_min=0, tm_max=10000000000000):
    command = "SELECT url, current_path, start_time, end_time, received_bytes, total_bytes, opened, referrer, " \
              + "last_modified, mime_type FROM downloads, downloads_url_chains " \
              + "WHERE (downloads_url_chains.id = downloads.id) AND (start_time/10000000 > %s AND start_time/10000000 < %s);" % (tm_min, tm_max)

    res = pull_from_db(history_db, command)
    data = init_data("chrome_scanner Downloads", len(res)) + init_table_header("./templates/init_chrome_downloads_html.html")
    open_dict = {"0" : "No", "1" : "Yes"}

    for row in res:
        start_time = dt.fromtimestamp(row[2]/10000000)
        if row[3] > 0:
            end_time = dt.fromtimestamp(row[3]/10000000)
        else:
            end_time = "download interrupted"
        try:
            pct = str(round((100 * row[4]) / row[5], 4)) + " %"
        except ZeroDivisionError:
            pct = "Download size is zero"
        opened = open_dict[str(row[6])]

        line = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (start_time, end_time, row[0], row[9], row[7]) \
               + "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (row[1], row[5], pct, opened, row[8])
        data += line

    data += close_table_html()
    saveResult("chrome_downloads.html", data)

def read_chrome_cookies(cookies_db, tm_min=0, tm_max=10000000000000, host=None):
    command = "SELECT name, host_key, value, creation_utc, expires_utc, last_access_utc, has_expires from cookies " \
              + "WHERE (creation_utc/10000000 > %s AND creation_utc/10000000 < %s);" % (tm_min, tm_max)
    if host:
        command = command[:-1] + " AND (host_key LIKE '%s');" % host

    res = pull_from_db(cookies_db, command)
    data = init_data("chrome_scanner Cookies", len(res)) + init_table_header("./templates/init_chrome_cookies_html.html")
    exp_dict = {"0" : "No", "1" : "Yes"}

    for row in res:
        creation_date = dt.fromtimestamp(row[3]/10000000)
        exp_date = dt.fromtimestamp(row[4]/10000000)
        last_access_date = dt.fromtimestamp(row[5]/10000000)
        exp_stat = exp_dict[str(row[6])]

        line = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (row[1], row[0], row[2], creation_date) \
               + "<td>%s</td><td>%s</td><td>%s</td></tr>" % (exp_date, last_access_date, exp_stat)
        data += line

    data += close_table_html()
    saveResult("chrome_cookies.html", data)

def read_chrome_logins(logins_db, tm_min=0, tm_max=10000000000000, domain=None):
    command = "SELECT action_url, username_value, password_value, signon_realm, date_created, times_used, form_data FROM logins " \
              + "WHERE (date_created/10000000 > %s AND date_created/10000000 < %s);" % (tm_min, tm_max)
    if domain:
        command = command[:-1] + " AND (signon_realm LIKE '%s');" % domain

    res = pull_from_db(logins_db, command)
    data = init_data("chrome_scanner Logins", len(res)) + init_table_header("./templates/init_chrome_logins_html.html")

    for row in res:
        creation_date = dt.fromtimestamp(row[4]/10000000)
        form_data = row[6].decode("ISO-8859-1")

        line = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (creation_date, row[3], row[0], row[1]) \
               + "<td>%s</td><td>%s</td><td>%s</td></tr>" % (row[2].decode("ISO-8859-1"), row[5], form_data)
        data += line

    data += close_table_html()
    saveResult("chrome_logins.html", data)
    
if __name__ == "__main__":
    print('\n\n    ##############A Python script to read chrome  browser data ############')
    print('    #                      Coded by monrocoury                            #')
    print('    #              can read forms data, cookies, Google searches          #')
    print('    #                   and history to name a few                         #')
    print('    #######################################################################\n\n')

    parser = optparse.OptionParser("Usage: python %prog -t <target> -b <(optional) chrome database path> or python %prog -h for help")
    target_help = "can take one of 4 values: history, google_searches, cookies, logins, or downloads"
    parser.add_option("-t", dest="target", type="string", help=target_help)
    db_help = "The full path of the chrome database file to parse. By default, it's data/data/com.android.chrome/app_chrome/Default/" \
              + "On android. On win vista or later C:\Users\USERNAME\AppData\Local\Google\Chrome\User Data\Default\databases" \
              + ". On win xp: C:\Documents and Settings\USERNAME\Application Support\Google\Chrome\Default\databases" \
              + ". On Linux: ~/.config/google-chrome/Default/databases. On Mac: ~/Library/Application Support/Google/Chrome/Default/databases"
    parser.add_option("-b", dest="db", type="string", help=db_help)
    min_help = "enter if target isn't 'cookies' to read items after a given date and time, must be a string separated by _ YYYY_MM_DD_HH_MM_SS"
    parser.add_option("--min_time", dest="min", type="string", help=min_help)
    max_help = "enter if target isn't 'cookies' to read items before a given date and time, must be a string separated by _ YYYY_MM_DD_HH_MM_SS"
    parser.add_option("--max_time", dest="max", type="string", help=max_help)
    dom_help = "enter if target function is cookies or logins to look for results corresponding to a specific host/domain." \
               + " Default None"
    parser.add_option("--domain", dest="host_domain", type="string", help=dom_help)
    (options, args) = parser.parse_args()

    if not options.target:
        sys.exit("please enter a target:\n\n%s" % parser.usage)

    if options.target not in ("cookies", "history", "google_searches", "downloads", "logins"):
        sys.exit("Unrecognized target function!")

    db = options.db
    d
