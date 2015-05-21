'''
Turn all.csv into a tab deliminted file (for easy processing in javascript)
'''

import csv
import os

try:
    os.remove("all.tsv")
except OSError:
    pass

with open('all.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        with open('all.tsv', 'a') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter='\t', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(row)
