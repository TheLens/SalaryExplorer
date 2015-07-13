# -*- coding: utf-8 -*-

'''docstring'''

# import csv
# from scripts.clean import Clean
from slugify import slugify


def make_headers(worksheet):
    '''Make headers'''

    headers = []
    cell_id = 0
    row_id = 0

    for cell_id in range(0, worksheet.ncols):
        cell_type = worksheet.cell_type(row_id, cell_id)
        cell_value = worksheet.cell_value(row_id, cell_id)
        cell_value = str(slugify(cell_value).replace('-', '_')).strip()

        if cell_type == 1:  # If unicode

            if cell_value == 'personnel_area_text':
                cell_value = 'department'
            elif cell_value == 'organizational_unit_text':
                cell_value = 'office'
            elif cell_value == 'work_parish':
                cell_value = 'parish'
            elif cell_value == 'employee_id_number':
                cell_value = 'employee_id'
            elif cell_value == 'employee_name':
                cell_value = 'full_name'
            elif cell_value == 'classified_unclassified':
                cell_value = 'classification'
            elif cell_value == 'full_time_part_time':
                cell_value = 'employee_status'
            elif cell_value == 'job_title':
                cell_value = 'job_title'
            elif cell_value == 'annual_pay_rate':
                cell_value = 'salary'
            elif cell_value == 'adjusted_service_date':
                cell_value = 'date_hired'

            headers.append(cell_value)

    headers.append('last_name')
    headers.append('first_name')
    headers.append('middle_name')

    print headers

    return headers


def split_name(filename):
    '''docstring'''

    headers = {}

    # with open('data/%s.csv' % (filename)) as f:
    #     reader = csv.reader(f)
    #     for i, row in enumerate(reader):
    #         headers[i] = row

    return headers


def clean_data(worksheet, writer, headers):
    # row_id = 1
    # TODO: ...nrows + 1?
    for row_id in range(1, worksheet.nrows):  # 1 because need to skip header
        # For each row...
        cell_id = 0
        row_dict = {}
        for cell_id in range(0, worksheet.ncols + 3):  # 3 new fields
            # For each column in this row...
            try:
                header = headers[cell_id]  # Not sure why try/except necessary
            except KeyError:
                # cell_id += 1
                continue

            condition = (
                header == 'first_name' or
                header == 'middle_name' or
                header == 'last_name'
            )

            if condition:
                cell_id = 4

            # Convert cells to correct data types
            try:
                # Strings
                cell_value = worksheet.cell_value(row_id, cell_id).strip()
                # print cell_value
                cell_value = str(cell_value)

                if header == 'last_name':
                    # Take everything before comma for last name
                    cell_value = cell_value.split(',')[0].strip()

                if header == 'first_name':
                    # Take after comma and before space for first name
                    # TODO: Fine tune separation of first name and middle init.
                    cell_value = cell_value.split(',')[1].strip()

                if header == 'middle_name':
                    cell_value = 'MIDDLE'

            except AttributeError:
                # Numbers, so take as is
                cell_value = worksheet.cell_value(row_id, cell_id)

            # Title case for names
            # if '_name' in header or header == 'position':
            if header != 'salary' and header != 'date_hired':
                cell_value = cell_value.title()

            # Correct things like Iii, Jr, Iv, etc.
            # cell_value = Clean(cell_value).cleaned_value  # TODO

            # Check if Excel was dumb and labeled strings as floats.
            # https://groups.google.com/forum/#!topic/python-excel/m6smKw5mweE
            # http://stackoverflow.com/questions/10169949/python-xlrd-reading-phone-nunmber-from-xls-becomes-float

            # if type(cell_value) == float:
            #     cell_value = str(int(cell_value))

            row_dict[header] = cell_value
            # cell_id += 1

        condition = (
            row_dict['employee_status'] == 'Wae' or
            row_dict['employee_status'] == 'Per Diem'
        )
        if condition:
            continue
        writer.writerow(row_dict)
        # row_id += 1
