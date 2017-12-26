#!/usr/bin/env python
import os
import optparse
import sys
try:
    from common_methods import *
except ImportError:
    sys.exit("Could not find common_methods.py... download the full toolkit from https://github.com/MonroCoury/Forensic_Tools")


def get_name_from_threadKey(threadKey, core_db):
    command = "SELECT thread_name FROM threads WHERE thread_key = \"%s\";" % threadKey
    return str(pull_from_db(core_db, command)[0][0])

def get_uid_from_name(name, core_db):
    try:
        command = "select contact_user_id from contact where name = \"%s\";" % name
        return str(pull_from_db(core_db, command)[0][0])
    except IndexError:
        raise ValueError("specified user not found!")

def get_db_owner(accounts_db):
    command = "SELECT display_name FROM accounts;"
    return str(pull_from_db(accounts_db, command, facebook_name=True)[0][0])

def read_fb_contacts(core_db="core.db"):
    command = "SELECT name, contact_user_id, profile_picture_url, is_blocked, " \
            + "last_seen_timestamp, last_seen_update_timestamp, is_friend " \
            + "from contact;"

    res = pull_from_db(core_db, command)
    data = init_data("facebook_messenger Contacts", len(res)) + init_table_header("./templates/init_fb_msngr_contacts_html.html")

    for row in res:
        name = str(row[0])
        account_url = "<a href=\"https://facebook.com/profile.php?id=%s\" target=\"_blank\">Link</a>" % str(row[1])
        profile_pic = '<a href="%s" target="_blank"><img src="%s" alt="%s\'s Avatar"></a>' % (str(row[2]), str(row[2]), str(row[0]))
        blocked = "Yes" if row[3] == "1" else "No"
        last_seen = parse_timestamp(row[4])
        last_seen_update = parse_timestamp(row[5])
        friend = "Yes" if str(row[6]) == "1" else "No"

        line = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (name, account_url, profile_pic, blocked) \
             + "<td>%s</td><td>%s</td><td>%s</td></tr>" % (last_seen, last_seen_update, friend)
        data += line

    data += close_table_html()

    saveResult("facebook_scanner_contacts.html", data)

def read_fb_messages(core_db, partner=None, tm_min=0, tm_max=10000000000000):
    db_owner = get_db_owner(os.path.split(core_db)[0] + "/cross_account.db")

    command = "SELECT sender, thread_key, timestamp, snippet, is_unsent, attachment_filename, attachment_filesize, " \
            + "attachment_mime_type, media_playable_url, voice_call_duration_s, voice_call_start_time, " \
            + "is_voice_call_answered, is_voice_call_incoming, user_id from messages " \
            + "WHERE (timestamp > %s AND timestamp < %s);" % (tm_min, tm_max)

    if partner:
        user_id = get_uid_from_name(partner, core_db)
        command = command[:-1] + " AND (sender = \"{}\" OR thread_key LIKE \"%{}\");".format(partner, user_id)

    res = pull_from_db(core_db, command)

    data = init_data("facebook_messenger Messages", len(res)) + init_table_header("./templates/init_fb_msngr_msgs_html.html")

    for row in res:
        sender = str(row[0]) if row[0] else "Database owner: " + db_owner
        threadKey = str(row[1])
        time = parse_timestamp(row[2])
        contents = str(row[3])
        sent = "No" if str(row[4]) == "1" else "Yes"
        attachment_name = str(row[5])
        attachment_size = parse_value(str(row[6]), integer=True, div=1024)
        attachment_type = parse_value(str(row[7]))
        media_url = "<a href='%s' target='_blank'>Link</a>" % parse_value(str(row[8])) if row[8] else "Not Applicable"
        voice_call_dur = parse_value(str(row[9]), integer=True, div= 60)
        voice_call_start = parse_timestamp(row[10])
        call_answered = "Yes" if str(row[11]) == 1 else "No/ Not Applicable"
        call_direction = "incoming" if str(row[12]) == "1" else "outgoing" if str(row[12]) == "0" else "Not Applicable"

        recipient = "Database owner: %s" % db_owner if (threadKey.split(":")[1] == str(row[13])) or "GROUP:" in threadKey else get_name_from_threadKey(threadKey, core_db)

        line = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (sender, recipient, time, contents, sent) \
             + "<td>%s</td><td>%s</td><td>%s</td>" % (attachment_name, attachment_size, attachment_type) \
             + "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" %(media_url, voice_call_start, call_answered, call_direction) \
             + "<td>%s</td></tr>" % voice_call_dur
        data += line

    data += close_table_html()

    saveResult("facebook_scanner_msgs.html", data)


def read_fb_call_log(core_db, partner=None, tm_min=0, tm_max=10000000000000):
    command = "SELECT thread_name, updated_timestamp, is_incoming, " \
            + "is_answered, attempt_count FROM aggregated_calls " \
            + "WHERE (updated_timestamp > %s AND updated_timestamp < %s);" % (tm_min, tm_max)

    if partner:
        command = command[:-1] + " AND thread_name = \"%s\";" % partner

    res = pull_from_db(core_db, command)
    data = init_data("facebook_messenger Call Log", len(res)) + init_table_header("./templates/init_fb_msngr_calls_html.html")

    for row in res:
        call_partner = str(row[0])
        call_time = parse_timestamp(row[1])
        direction = "incoming" if str(row[2]) == "1" else "outgoing"
        answered = "Yes" if str(row[3]) == "1" else "No"

        line = "<tr><td>%s</td><td>%s</td><td>%s</td>" % (call_partner, call_time, direction)\
             + "<td>%s</td><td>%s</td></tr>" % (answered, row[4])
        data += line

    data += close_table_html()

    saveResult("facebook_scanner_calls.html", data)

def read_fb_accounts(cross_account_db):
    command = "SELECT user_id, display_name, profile_pic, nonce FROM accounts;"

    res = pull_from_db(cross_account_db, command)
    data = init_data("facebook_messenger Accounts", len(res)) + init_table_header("./templates/init_fb_msngr_accounts_html.html")

    for row in res:
        name = str(row[1])
        account_url = "<a href=\"https://facebook.com/profile.php?id=%s\" target=\"_blank\">Link</a>" % str(row[0])
        profile_pic = '<a href="%s" target="_blank"><img src="%s" alt="%s\'s Avatar"></a>' % (str(row[2]), str(row[2]), str(row[1]))
        nonce = parse_value(row[3])

        line = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (name, profile_pic, account_url, nonce)
        data += line

    data += close_table_html()

    saveResult("facebook_scanner_accounts.html", data)

if __name__ == "__main__":
    print('\n\n    ##############A Python script that reads facebook app data #####################')
    print('    #                      Coded by monrocoury                                     #')
    print('    ################################################################################\n\n')

    parser = optparse.OptionParser("Usage: python %prog -t <target> --db <core.db database location>" \
                                   + " --accountDB <cross_account database location> --partner <(optional) partner name>" \
                                   + " --min_time <(optional)> --max_time <(optional)>" \
                                   + " or python skype_scanner.py -h for help")

    target_help = "target function: msgs, calls, contacts or accounts"
    parser.add_option("-t", dest="target", type="string", help=target_help)

    db_help = "full path to the core.db file, it contains most of the information you want to extract " \
            + "location if you're on android /data/data/com.facebook.mlite/databases/"
    parser.add_option("--db", dest="db", default="core.db", type="string", help=db_help)

    accountDB_help = "full path to the core.db file, it contains information about the accounts " \
                   + "used to log into the app"
    parser.add_option("--accountDB", dest="account_db", default="cross_account.db", type="string", help=accountDB_help)

    partner_help = "name of chat partner"
    parser.add_option("--partner", dest="chat_partner", type="string", help=partner_help)

    min_time_help = "read messages/calls after a given date and time, " \
                  + "must be a string separated by _ like YYYY_MM_DD_HH_MM_SS"
    parser.add_option("--min_time", dest="min_time", default=0, type="string", help=min_time_help)

    max_time_help = "read messages/calls before a given date and time, " \
                  + "must be a string separated by _ like YYYY_MM_DD_HH_MM_SS"
    parser.add_option("--max_time", dest="max_time", default=10000000000000, type="string", help=max_time_help)

    (options, args) = parser.parse_args()

    if not options.target:
        sys.exit("please enter a target!\n\n%s" % parser.usage)

    if options.target.lower() not in ("msgs", "calls", "contacts", "accounts"):
        sys.exit("Unrecognized target function!")

    db = options.db
    if not os.path.isfile(db):
        db = os.path.join(db, "core.db")

    min_time = time_to_epoch(options.min_time) if options.min_time > 0 else 0
    max_time = time_to_epoch(options.max_time) if options.max_time < 10000000000000 else 10000000000000

    if options.target.lower() == "msgs":
        read_fb_messages(core_db=db, partner=options.chat_partner, tm_min=min_time, tm_max=max_time)
    elif options.target.lower() == "contacts":
        read_fb_contacts(core_db=db)
    elif options.target.lower() == "accounts":
        read_fb_accounts(options.account_db)
    else:
        read_fb_call_log(core_db=db, partner=options.chat_partner, tm_min=min_time, tm_max=max_time)