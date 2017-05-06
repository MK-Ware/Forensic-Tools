#!/usr/bin/env python
import sqlite3, os, sys, optparse
from datetime import datetime as dt
from time import mktime, strptime
try:
    from common_methods import *
except ImportError:
    sys.exit("Could not find common_methods.py... download the full toolkit from https://github.com/MonroCoury/Forensic_Tools")


def read_accounts(db):
    command = "SELECT fullname, skypename, city, country, datetime(profile_timestamp, 'unixepoch') FROM Accounts;"
    res = pull_from_db(db, command)
    now = dt.now()
    data = init_data("skype_scanner Account", len(res)) + "<thead>\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<th scope=\"col\">Full Name</th>\n\t\t\t\t\t\t" \
        + "<th scope=\"col\">Skype Username</th>\n\t\t\t\t\t\t<th scope=\"col\">Location</th>\n\t\t\t\t\t\t" \
        + "<th scope=\"col\">Profile Date</th>\n\t\t\t\t\t</tr>\n\t\t\t\t</thead>\n\t\t\t\t<tbody>"
    for row in res:
        if not row[2]:
            loc = str(row[3]) + ", unspecified city/town"
        else:
            loc = str(row[3]) + ', ' + str(row[2])
        line = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (row[0], row[1],
                                                                          loc, row[4])
        data += line

    data += "</tbody></tablte></center></body></html>"
    tgt = "skype_scanner_accounts.html"
    saveResult(tgt, data)

def read_contacts(db):
    command = "SELECT displayname, skypename, city, country, phone_mobile, birthday FROM Contacts;"
    res = pull_from_db(db, command)
    now = dt.now()
    data = init_data("skype_scanner Contacts", len(res)) + "<thead>\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<th scope=\"col\">Display Name</th>\n\t\t\t\t\t\t" \
        + "<th scope=\"col\">Skype Name</th>\n\t\t\t\t\t\t<th scope=\"col\">Location</th>\n\t\t\t\t\t\t<th scope=\"col\">Phone NO.</th>\n\t\t\t\t\t\t" \
        + "<th scope=\"col\">DOB</th>\n\t\t\t\t\t</tr>\n\t\t\t\t</thead>\n\t\t\t\t<tbody>"
    for row in res:
        if not row[2]:
            loc = str(row[3]) + ", unspecified city/town"
        else:
            loc = str(row[3]) + ', ' + str(row[2])
        line = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (row[0], row[1],
                                                                                    loc, row[4], row[5])
        data += line

    data += "</tbody></tablte></center></body></html>"
    tgt = "skype_scanner_contacts.html"
    saveResult(tgt, data)

def read_call_log(db, partner=None, tm_min=0, tm_max=10000000000000):
    command = "SELECT datetime(begin_timestamp, 'unixepoch'), identity, duration, is_incoming FROM calls, conversations WHERE " \
              + "(calls.conv_dbid = conversations.id) AND (begin_timestamp > %s AND begin_timestamp < %s);" % (tm_min, tm_max)
    if partner:
        command = command[:-1] + " AND (chatname LIKE %s);" % ("'%" + partner + "%'")

    res = pull_from_db(db, command)
    data = init_data("skype_scanner Call Log", len(res)) + "<thead>\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<th scope=\"col\">Start Time</th>\n\t\t\t\t\t\t" \
        + "<th scope=\"col\">Partner</th>\n\t\t\t\t\t\t<th scope=\"col\">Duration</th>\n\t\t\t\t\t\t<th scope=\"col\">Direction</th>\n\t\t\t\t\t\t" \
        + "</tr>\n\t\t\t\t</thead>\n\t\t\t\t<tbody>"
    for row in res:
        dir_dict = {"0" : "outgoing", "1" : "incoming"}
        line = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (row[0], row[1], row[2], dir_dict[str(row[3])])
        data += line

    data += "</tbody></tablte></center></body></html>"
    tgt = "skype_scanner_calls.html"
    saveResult(tgt, data)

def read_msgs(db, partner=None, tm_min=0, tm_max=10000000000000):
    command = "SELECT timestamp, dialog_partner, author, body_xml, chatmsg_status, sending_status, chatname " \
              + "FROM Messages WHERE (timestamp > %s AND timestamp < %s);" % (tm_min, tm_max)
    if partner:
        command = command[:-1] + " AND (chatname LIKE %s);" % ("'%" + partner + "%'")

    res = pull_from_db(db, command)
    user = pull_from_db(db, "SELECT skypename from Accounts;")
    data = init_data("skype_scanner Messages", len(res)) + "<thead>\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<th scope=\"col\">Time</th>\n\t\t\t\t\t\t" \
        + "<th scope=\"col\">Chat</th>\n\t\t\t\t\t\t<th scope=\"col\">From</th>\n\t\t\t\t\t\t<th scope=\"col\">To</th>\n\t\t\t\t\t\t" \
        + "<th scope=\"col\">Message</th>\n\t\t\t\t\t<th scope=\"col\">Status</th></tr>\n\t\t\t\t</thead>\n\t\t\t\t<tbody>"
    
    for row in res:
        try:
            if 'partlist' not in str(row[3]):
                if row[1]:
                    From = str(row[2])
                    To = str(row[1])
                else:
                    From = str(row[2])
                    To = str(user[0][0])
                status_dict = {"1" : "pending", "2" : "delivered"}
                if str(row[5]) in ("1", "2"):
                    status = status_dict[str(row[4])]
                else:
                    status = "incoming"
                line = "\n\t\t\t\t\t<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (dt.fromtimestamp(float(row[0])),
                                                                                                                    row[6], From, To, row[3],
                                                                                                                    status)
                data += line
        except:
            pass
    data += "</tbody></tablte></center></body></html>"

    tgt = "skype_scanner_msgs.html"
    saveResult(tgt, data)
        
if __name__ == "__main__":
    print('\n\n    ##############A Python script to read skype profile data ################')
    print('    #                      Coded by monrocoury                              #')
    print('    #              can read accounts data, messages, call log               #')
    print('    #                   and contacts to name a few                          #')
    print('    #########################################################################\n\n')

    parser = optparse.OptionParser("Usage: python %prog -t <target> -b <database location>" \
                                   + " or python skype_scanner.py -h for help")
    target_help = "can take one of 4 values: accounts, msgs, clog, or contacts"
    parser.add_option("-t", dest="target", type="string", help=target_help)
    db_help = "The location of the database to parse, or the full path of the database file. " \
              + "ie: either c:\folder or c:\folder\db_file.db. If you enter a folder, the script will " \
              + "look for a main.db file which is the default name and extension of skype profile database." \
              + " On windows, the default location of the main.db file is: " \
              + r"C:\Users\(WindowsUserName)\AppData\Roaming\Skype\(SkypeUserName)\ on linux: " \
              + r"~/.Skype/(SkypeUserName)/ and on mac: ~/Library/Application Support/Skype/(SkypeUserName)/" \
              + r" if the location contains spaces, enclose it in quotes"
    parser.add_option("-b", dest="db", type="string", help=db_help)
    parser.add_option("--partner", dest="partner", type="string", help="enter only if target is 'msgs' or 'clog' to read messages/calls from the given sype username")
    min_help = "enter only if target is 'msgs' or 'clog' to read messages/calls after a given date and time, must be a string separated by _ YYYY_MM_DD_HH_MM_SS"
    parser.add_option("--min_time", dest="min", type="string", help=min_help)
    max_help = "enter only if target is 'msgs' or 'clog' to read messages/calls before a given date and time, must be a string separated by _ YYYY_MM_DD_HH_MM_SS"
    parser.add_option("--max_time", dest="max", type="string", help=max_help)
    (options, args) = parser.parse_args()

    if None in (options.target, options.db):
        sys.exit("please enter a target:\n\n%s" % parser.usage)
    if options.target not in ("accounts", "msgs", "clog", "contacts"):
        sys.exit("Unrecognized target function!")

    db = options.db
    if not os.path.isfile(db):
        db = os.path.join(db, "main.db")

    if options.target.lower() == "accounts":
        read_accounts(db)
    elif options.target.lower() == "msgs":
        if options.min:
            min_time = time_to_epoch(options.min)
        else:
            min_time = 0
        if options.max:
            max_time = time_to_epoch(options.min)
        else:
            max_time = 10000000000000
        read_msgs(db, options.partner, min_time, max_time)
    elif options.target.lower() == "clog":
        if options.min:
            min_time = time_to_epoch(options.min)
        else:
            min_time = 0
        if options.max:
            max_time = time_to_epoch(options.min)
        else:
            max_time = 10000000000000
        read_call_log(db, options.partner, min_time, max_time)
    elif options.target.lower() == "contacts":
        read_contacts(db)
