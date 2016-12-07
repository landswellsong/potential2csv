#!/usr/bin/env python3
from re import search, findall
from ftplib import FTP
from io import BytesIO
from json import dumps

# Supported:
# - EZ, LF

try:
    while True:
        url = input()
        m = search(r"ftp://(promis.ikd.kiev.ua)/(Potential/DECODED/([0-9_]*)/pdata\3/([a-z]*)/([a-z]*)/[0-9]*/)", url)
        if m != None:
            data = { "id": m.group(3), "parm": m.group(4), "freq": m.group(5) }
            fname = data["id"] + "-" + data["parm"] + "-" + data["freq"] + ".json"
            print("Creating dataset: " + fname)
            ftp = FTP(m.group(1))
            ftp.login()
            ftp.cwd(m.group(2))
            basename = None
            for x in ftp.nlst():
                # expect something like 00000108.lfz
                mm = search(r"[0-9]{4}([0-9]{4}).lfz", x)
                if mm != None:
                    basename = mm.group(1)
                    break
            if basename == None:
                print("Can't figure out the base name")
            else:
                # .set
                setfile = BytesIO()
                ftp.retrbinary("RETR " + m.group(5)+basename+"mv.set", setfile.write)
                mm = search(r"utc=([1-2][09][8901][0-9]-[0-9]{2}-[0-9]{2} [012][0-9]:[0-5][0-9]:[0-5][0-9])", str(setfile.getvalue()[:]))
                # assume data is correct
                data["utc"] = mm.group(1)

                # .csv
                csvfile = BytesIO()
                ftp.retrbinary("RETR " + m.group(5)+basename+"mv.csv", csvfile.write)
                # TODO: do we have any ocurrence of non-integer input?
                mm = findall(r"([-0-9]*),[0],", str(csvfile.getvalue()[:]))
                data["mv"] = []
                for x in mm:
                    data["mv"].append(int(x))
            # TODO: except file open error
            fp = open(fname, "w")
            fp.write(dumps(data))
            fp.close()
            ftp.quit()

except EOFError:
    print("Enjoy your files.")
