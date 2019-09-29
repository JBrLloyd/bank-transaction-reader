#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv, datetime
from dateutil import relativedelta

class Transaction:
    def __init__(self, id, line_num, date, credit, debt, desc):
        self.id = id
        self.line_num = line_num
        self.date = date
        self.credit = credit
        self.debt = debt
        self.desc = desc

def data_import_nab(data):
    return {
        'date': datetime.datetime.strptime(data[0], "%d-%b-%y").date(),
        'credit': data[1] if data[1][0] != '-' else None,
        'debt': data[1] if data[1][0] == '-' else None,
        'desc': data[5]
    }

def data_import_ing(data):
    return {
        'date': datetime.datetime.strptime(data[0], "%d/%M/%y").date(),
        'credit': data[2],
        'debt': data[3],
        'desc': data[1]
    }

def data_import(bank, data):
    options = {
        'NAB': lambda : data_import_nab(data),
        'ING': lambda : data_import_ing(data)
    }
    return options.get(bank, lambda : "ERROR: Tank type not valid")()

def read_transaction_csv(start_num, bank, file_path):
    _data = []
    
    print('Finding file in:', file_path)
    with open(file_path) as csvFile:
        readCsv = csv.reader(csvFile, delimiter=',')
        for idx, row in enumerate(readCsv):
            try:
                data_output = data_import(bank, row)
                _data.append(Transaction(idx, idx, data_output['date'], data_output['credit'], data_output['debt'], data_output['desc']))
            except ValueError as ve:
                print('ValueError Raised:', ve)
    print('Rows of data ingested:', len(_data))
    return sorted(_data, key=lambda x: x.date)

def find_duplicate_data(processed_data):
    for idx, curr_data in enumerate(processed_data):
        if idx:
            prev_data = processed_data[idx - 1]
        else:
            prev_data = curr_data
            continue
        
        if curr_data.date.month == prev_data.date.month and curr_data.date.year == prev_data.date.year:
            print('Duplicate Month and Year on rows', curr_data.id, 'and', prev_data.id, '(', curr_data.date, ')')
            continue
        if curr_data.date.month != (prev_data.date + relativedelta.relativedelta(months=1)).month:
            print('Date incorrect for line:', curr_data.id, '-', curr_data.date.strftime("%b %Y"))


transaction_files = [{'bank': '', 'path': ''}]
start_num = 0
processed_data = {}

for file in transaction_files:
    processed_data = (read_transaction_csv(len(processed_data), file['bank'], file['path']))

find_duplicate_data(processed_data)
