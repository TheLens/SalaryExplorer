'''
Turn gss.csv into a tab deliminted file (for easy processing in javascript)
'''

import csv
import os

try:
    os.remove("gss_tabs.csv")
except OSError:
    pass

with open('gss.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        with open('gss_tabs.csv', 'a') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter='\t', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(row)
