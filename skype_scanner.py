#!/usr/bin/env python
import sqlite3, os, sys, optparse
from datetime import datetime as dt
from common_methods import *


def read_accounts(db, verbose=False, save=True):
    command = "SELECT fullname, skypename, city, country, datetime(profile_timestamp, 'unixepoch') FROM Accounts;"
    res = pull_from_db(db, command)
    now = dt.now()
    data = "Time: %d/%d/%d %d : %d : %d. Found %s account(s):\n" % (now.year, now.month,
                                                                    now.day, now.hour, now.minute,
                                                                    now.second, len(res))
    for row in res:
        if not row[2]:
            loc = str(row[3]) + ", unspecified city/town"
        else:
            loc = str(row[3]) + ', ' + str(row[2])
        line = "Full Name: %s\nSkype username: %s\nLocation: %s\nProfile Date: %s\n\n" % (row[0], row[1],
                                                                                          loc, row[4])
        data += line

    if verbose:
        print(data)
    if save:
        tgt = "skype_scanner_accounts.txt"
        saveResult(tgt, data)


def read_contacts(db, verbose=False, save=True):
    command = "SELECT displayname, skypename, city, country, phone_mobile, birthday FROM Contacts;"
    res = pull_from_db(db, command)
    now = dt.now()
    data = "Time: %d/%d/%d %d : %d : %d. Found %s contacts(s):\n" % (now.year, now.month,
                                                                    now.day, now.hour, now.minute,
                                                                    now.second, len(res))
    for row in res:
        if not row[2]:
            loc = str(row[3]) + ", unspecified city/town"
        else:
            loc = str(row[3]) + ', ' + str(row[2])
        line = "Display Name: %s\nSkype Name: %s\nLocation: %s\nPhone Number: %s\nDOB: %s\n\n" % (row[0], row[1],
                                                                                              loc, row[4], row[5])
        data += line
    if verbose:
        try:
            print(data)
        except UnicodeEncodeError:
            os.system("chcp 65001")
            print(data)
    if save:
        tgt = "skype_scanner_contacts.txt"
        saveResult(tgt, data)

def read_call_log(db, verbose=False, save=True):
    command = "SELECT datetime(begin_timestamp, 'unixepoch'), identity FROM calls, conversations WHERE " \
              + "calls.conv_dbid = conversations.id;"
    res = pull_from_db(db, command)
    now = dt.now()
    data = "Time: %d/%d/%d %d : %d : %d. Found %s call(s):\n" % (now.year, now.month,
                                                                 now.day, now.hour, now.minute,
                                                                 now.second, len(res))
    for row in res:
        line = "Start time: %s\nPartner: %s\n\n" % (row[0], row[1])
        data += line

    if verbose:
        try:
            print(data)
        except UnicodeEncodeError:
            os.system("chcp 65001")
            print(data)
    if save:
        tgt = "skype_scanner_contacts.txt"
        saveResult(tgt, data)

def read_msgs(db, verbose=False, save=True):
    command = "SELECT datetime(timestamp, 'unixepoch'), dialog_partner, author, body_xml FROM Messages;"
    res = pull_from_db(db, command)
    now = dt.now()
    data = "Time: %d/%d/%d %d : %d : %d. Found %s call(s):\n" % (now.year, now.month,
                                                                 now.day, now.hour, now.minute,
                                                                 now.second, len(res))
    for row in res:
        try:
            if 'partlist' not in str(row[3]):
                if row[1]:
                    msg_direction = "To " + str(row[1]) + ": "
                else:
                    msg_direction = "From " + str(row[2]) + ": "
                line = "Time: %s\n%s %s\n\n" % (row[0], msg_direction, row[3])
                data += line
        except:
            pass

    if verbose:
        try:
            print(data)
        except UnicodeEncodeError:
            os.system("chcp 65001")
            print(data)
    if save:
        tgt = "skype_scanner_msgs.txt"
        saveResult(tgt, data)
        
if __name__ == "__main__":
    print('\n\n    ##############A Python script to read skype profile data ################')
    print('    #                      Coded by monrocoury                              #')
    print('    #              can read accounts data, messages, call log               #')
    print('    #                   and contacts to name a few                          #')
    print('    #########################################################################\n\n')

    parser = optparse.OptionParser("Usage: python skype_scanner.py -t <target> -b <database location>" \
                                   + " -v <verbose, True or False> -s <save, True or False> or python skype_scanner.py -h for help")
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
    parser.add_option("-v", dest="verbose", type="string", help="show the result in the console screen")
    parser.add_option("-s", dest="save", type="string", help="save the result to a text file")
    (options, args) = parser.parse_args()

    if None in (options.target, options.db):
        sys.exit("please enter a target:\n\n%s" % parser.usage)
    if options.target not in ("accounts", "msgs", "clog", "contacts"):
        sys.exit("Unrecognized target function!")

    db = options.db
    if not os.path.isfile(db):
        db = os.path.join(db, "main.db")
    try:
        verbose = eval(options.verbose.title())
    except:
        verbose = False

    try:
        save = eval(options.save.title())
    except:
        save = True

    if options.target.lower() == "accounts":
        read_accounts(db, verbose, save)
    elif options.target.lower() == "msgs":
        read_msgs(db, verbose, save)
    elif options.target.lower() == "clog":
        read_call_log(db, verbose, save)
    elif options.target.lower() == "contacts":
        read_contacts(db, verbose, save)
