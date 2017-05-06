#!/usr/bin/env python
import sqlite3, os, sys
from datetime import datetime as dt


def time_to_epoch(time_string):
    tm = [int(item) for item in time_string.split("_")]
    return dt(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5]).timestamp()

def getFileName(full_path):
    x = 0
    for i in range(len(full_path)):
        if full_path[i] in ("\\", "/"):
            x = i

    if any(char in full_path for char in ("\\", "/")):
        x += 1
    return full_path[x:]

def saveResult(file_name, data):
    if os.path.isfile(file_name):
            sys.exit("%s already exists! Rename or move that file to avoid losing your data!" % file_name)

    print("saving results to %s\n" % file_name)

    with open(file_name, "w", encoding='utf-8') as rf:
        rf.write(data)
    print("done! Results saved to %s...\n" % file_name)

def pull_from_db(db, command):
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(command)
        return c.fetchall()
    except Exception as e:
        sys.exit("Error reading the database: %s" % e)

def init_data(title, size):
    now = dt.now()
    data = "<html>\n\t<title>%s</title>\n\t<head>" % title \
        + "<meta http-equiv=\"Content-Type\" content=\"text/html;charset=UTF-8\">\n\t" \
        + "<style type=\"text/css\">\n\t\ttable{\n\t\t\tborder-collapse: collapse;\n" \
        + "\t\t\tborder-spacing: 0;\n\t\t}\n\t\tth,\n\t\ttd{\n\t\t\tpadding: 10px 15px;\n\t\t}\n\t\tthead{\n\t\t\tbackground: #395870;\n\t\t\t" \
        + "color: #fff;\n\t\t}\n\t\ttbody tr:nth-child(even){\n\t\t\tbackground: #f0f0f2\n\t\t}\n\t\ttd{\n\t\t\tborder-bottom: 1px solid #cecfd5;" \
        + "\n\t\t\tborder-right: 1px solid #cecfd5;\n\t\t}\n\t\ttd:first-child{\n\t\t\tborder-left: 1px solid #cecfd5;\n\t\t}\n\t</style>\n\t</head>" \
        + "\n\t<body>\n\t\t<center>\n\t\t\t<table>\n\t\t\t\t<caption style=\"color:brown\" style=\"font-family:georgia\"><i>" \
        + "<B> %d-%d-%d %d: %d: %d Found "% (now.year, now.month, now.day, now.hour, now.minute, now.second) \
        + "%d result(s)</B></i></caption>\n\t\t\t\t" % size
    return data
