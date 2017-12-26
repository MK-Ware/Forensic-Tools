#!/usr/bin/env python
import os
import optparse
try:
    from common_methods import *
except ImportError:
    sys.exit("Could not find common_methods.py... download the full toolkit from https://github.com/MonroCoury/Forensic_Tools")


def parse_col(col_val):
    if not col_val:
        return "Not Applicable"
    else:
        return str(col_val)

def get_name_from_phone(wa_db, phone):
    command = "SELECT sort_name FROM wa_contacts WHERE jid like '%{}%';".format(phone)
    res = pull_from_db(wa_db, command)
    names = [str(row[0]) for row in res if len(row) > 0]
    return "--".join(names)

def read_wa_msgs(msgstore_db, wa_db=None, partner=None, tm_min=0, tm_max=10000000000000, get_partner_name=None):
    '''Read Messages from whatsapp msgstore database. Takes 6 arguments:
msgstore_db: msgstore database file full path
wa_db: wa database file full path, default value None
partner: chat partner, default value None
tm_min: minimum Message timestamp, default value 0
tm_max: maximum Message timestamp, default value 10000000000000
get_partner_name: pass True to display name instead of phone number in from/to fields'''
    command = "SELECT key_from_me, status, data, timestamp, receipt_server_timestamp, receipt_device_timestamp," \
              + " read_device_timestamp, played_device_timestamp, media_url, media_caption, media_duration, latitude," \
              + " longitude, media_wa_type, needs_push, recipient_count, key_remote_jid from messages" \
              + " WHERE (timestamp > %s AND timestamp < %s);" % (tm_min, tm_max)
    if partner:
        command = "SELECT key_from_me, status, data, timestamp, receipt_server_timestamp, receipt_device_timestamp," \
                  + " read_device_timestamp, played_device_timestamp, media_url, media_caption, media_duration, latitude," \
                  + " longitude, media_wa_type, needs_push, recipient_count, key_remote_jid FROM messages" \
                  + " WHERE (key_remote_jid LIKE '%{}%') AND (timestamp > {} AND timestamp < {});".format(partner, tm_min, tm_max)
    res = pull_from_db(msgstore_db, command)
    status_dict = {0 : "RECEIVED", 1 : "UPLOADING", 2 : "UPLOADED", 3 : "SENT BY CLIENT",
                   4 : "RECEIVED BY SERVER", 5 : "RECEIVED BY DESTINATION", 6 : "CONTROL MESSAGE"}
    media_wa_dict = {0 : "text", 1 : "image", 2 : "audio", 3 : "video", 4 : "contact card", 5 : "geo position", 8 : "call"}
    broad_dict = {2 : "Yes", 0 : "No"}
    if not wa_db:
        wa_db = os.path.join(os.path.dirname(msgstore_db), "wa.db")
    data = init_data("whatsapp_scanner Messages", len(res)) + init_table_header("./templates/init_whatsapp_msgs_html.html")

    for row in res:
        if str(row[0]) == "1":
            frm = "db owner"
            to = str(row[16])[0:str(row[16]).index('@')]
            if get_partner_name:
                to = get_name_from_phone(wa_db, to)
        else:
            frm = str(row[16])[0:str(row[16]).index('@')]
            if get_partner_name:
                frm = get_name_from_phone(wa_db, frm)
            to = "db owner"

        try:
            status = status_dict[int(row[1])]
        except KeyError:
            status = "Unknown"
        msg_body = str(row[2])
        insert_time = parse_timestamp(row[3])
        server_time = parse_timestamp(row[4])
        receipt_time = parse_timestamp(row[5])
        read_time = parse_timestamp(row[6])
        media_play_time = parse_timestamp(row[7])
        media_url = parse_col(row[8])
        media_cap = parse_col(row[9])
        media_dur = parse_col(row[10])
        coordinates = "long: %s, lat: %s" % (row[12], row[11])
        try:
            msg_type = media_wa_dict[int(row[13])]
        except KeyError:
            msg_type = "Unknown"
        broadcast = broad_dict[int(row[14])]
        receivers = int(row[15])

        line = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (insert_time, server_time, receipt_time, media_play_time, read_time) \
               + "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (frm, to, msg_type, msg_body, status, broadcast) \
               + "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (receivers, media_url, media_cap, media_dur, coordinates)
        data += line
    data += close_table_html()
    tgt = "whatsapp_scanner_msgs.html"
    saveResult(tgt, data)

def read_wa_contacts(wa_db):
    '''Read contacts from whatsapp wa database. Takes one argument: the full path of the wa.db database file'''
    command = "SELECT jid, is_whatsapp_user, status, status_timestamp, display_name, unseen_msg_count, sort_name from wa_contacts;"
    res = pull_from_db(wa_db, command)
    wa_user_dict = {0 : "No", 1 : "Yes"}
    data = init_data("whatsapp_scanner Contacts", len(res)) + init_table_header("./templates/init_whatsapp_contacts_html.html")

    for row in res:
        phone = str(row[0])[0:str(row[0]).index('@')]
        wa_user = wa_user_dict[row[1]]
        last_status_update = parse_timestamp(row[3])
        line = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (row[4], row[6], wa_user,
                                                                                                           phone, row[2], last_status_update,
                                                                                                           row[5])
        data += line
    data += close_table_html()
    tgt = "whatsapp_scanner_contacts.html"
    saveResult(tgt, data)

if __name__ == "__main__":
    print('\n\n    ##############A Python script that reads whatsapp data #####################')
    print('    #                      Coded by monrocoury                                 #')
    print('    ############################################################################\n\n')

    parser = optparse.OptionParser("Usage: python %prog -t <target> --msgstore <msgstore database location>" \
                                   + " --wa <wa database location> --partner <(optional) partner name> --min_time <(optional)> --max_time <(optional)>" \
                                   + " --partner_name <(optional)> or python skype_scanner.py -h for help")
    target_help = "either msgs or contacts"
    parser.add_option("-t", dest="target", type="string", help=target_help)
    msgstore_help = "The full path of the msgstore.db database. It contains exchanged messages with details. Location on android: " \
                    + "/data/data/com.whatsapp/databases/"
    parser.add_option("--msgstore", dest="msgstore_db", type="string", help=msgstore_help)
    wa_help = "The full path of the wa.db database. It contains phone contacts with details, required for reading contacts data, and " \
              + "if get_partner_name is True. It's optional if target function is 'msgs', in which case the script will try to access 'wa.db" \
              + " in the same directory containing msgstore.db"
    parser.add_option("--wa", dest="wa_db", type="string", help=wa_help)
    parser.add_option("--partner", dest="partner", type="string", help="enter only if target is 'msgs' to read messages/calls from/to the given number")
    p_name_help = "True to display partner name instead of number in from/to column, default False"
    parser.add_option("--partner_name", dest="get_partner_name", type="string", help=p_name_help)
    min_help = "enter only if target is 'msgs' to read messages/calls after a given date and time, must be a string separated by _ YYYY_MM_DD_HH_MM_SS"
    parser.add_option("--min_time", dest="min", type="string", help=min_help)
    max_help = "enter only if target is 'msgs' to read messages/calls before a given date and time, must be a string separated by _ YYYY_MM_DD_HH_MM_SS"
    parser.add_option("--max_time", dest="max", type="string", help=max_help)
    (options, args) = parser.parse_args()

    if not options.target:
        sys.exit("please enter a target:\n\n%s" % parser.usage)
    if options.target not in ("msgs", "contacts"):
        sys.exit("Unrecognized target function!")

    msgstore_db = options.msgstore_db
    if not os.path.isfile(msgstore_db):
        msgstore_db = os.path.join(msgstore_db, "msgstore.db")

    wa_db = options.wa_db

    if options.min:
        min_time = time_to_epoch(options.min)
    else:
        min_time = 0
    if options.max:
        max_time = time_to_epoch(options.min)
    else:
        max_time = 10000000000000

    get_partner_name = bool(options.get_partner_name)

    print("Working...")
    if options.target.lower() == "msgs":
        read_wa_msgs(msgstore_db, wa_db=wa_db, partner=options.partner, tm_min=min_time, tm_max=max_time, get_partner_name=get_partner_name)
    elif options.target.lower() == "contacts":
        read_wa_contacts(wa_db)

