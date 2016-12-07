#!/usr/bin/env python3
import re
from ftplib import FTP

# Supported:
# - EZ, LF

try:
    while True:
        url = input()
        m = re.search(r"ftp://(promis.ikd.kiev.ua)/(Potential/DECODED/([0-9_]*)/pdata\3/([a-z]*)/([a-z]*)/([0-9]*)/)", url)
        if m != None:
            fname = m.group(3) + "-" + m.group(4) + "-" + m.group(5) + "-" + m.group(6) + ".json"
            print("Create dataset: " + fname)
            ftp = FTP(m.group(1))
            ftp.login()
            ftp.cwd(m.group(2))
            basename = None
            for x in ftp.nlst():
                # expect something like 00000108.lfz
                mm = re.search(r"[0-9]{4}([0-9]{4}).lfz", x)
                if mm != None:
                    basename = mm.group(1)
                    break
            if basename == None:
                print("Can't figure out the base name")
            else:
                print(m.group(5)+basename+".csv")
            ftp.quit()

except EOFError:
    print("Enjoy your files.")
