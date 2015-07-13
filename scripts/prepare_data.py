
'''Generates CSV files from Excel file. Cleans CSV files.'''

import csv
import xlrd
from util import make_headers, clean_data
from scripts import PROJECT_DIR


def main():
    '''docstring'''

    import_file = "%s/data/raw/La State Employee Listing " % PROJECT_DIR + \
        "- Data as of 5-15-2015.xlsx"

    workbook = xlrd.open_workbook(import_file)
    worksheets = workbook.sheet_names()

    headers = make_headers(workbook.sheet_by_name(worksheets[0]))

    file_path = "%s/data/intermediate/salaries.csv" % PROJECT_DIR

    with open(file_path, "w") as filename:
        writer = csv.DictWriter(filename, fieldnames=headers)
        writer.writeheader()
        sheet = workbook.sheet_by_name(worksheets[0])
        clean_data(sheet, writer, headers)

if __name__ == '__main__':
    main()
