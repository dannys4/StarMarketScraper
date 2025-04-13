#!/usr/bin/env python
import os
from typing import TypedDict, Dict, List
import json
import re
from datetime import datetime, date
import csv

class ReceiptItem(TypedDict):
    name: str
    quantity: float
    price: float
    date: date

def make_date(date_str: str):
    return datetime.strptime(date_str, '%m-%d-%Y').date()

def create_receipt_item(itemDict: Dict, date_str: str):
    date_obj = make_date(date_str)
    name: str = itemDict['name']
    quantityMatch = re.search(r'\d+\.?\d{,2}', itemDict['quantity'])
    if quantityMatch is None:
        print(itemDict['quantity'])
        raise ValueError("Could not find quantity!")
    quantityStr = quantityMatch.group()
    priceStr: str = itemDict['price']
    quantity = float(quantityStr)
    price = float(priceStr[1:])
    return ReceiptItem(name=name, quantity=quantity, price=price, date=date_obj)

def create_receipt(jsonFilename: str, date: str):
    with open(jsonFilename, 'r') as f:
        list_json = json.load(f)
    receipt = [create_receipt_item(it, date) for it in list_json]
    return receipt

def find_date(date_string: str, sep: str):
    date_pattern = r'\d{2}'+sep+r'\d{2}'+sep+r'\d{4}'
    date_match = re.search(date_pattern, date_string)
    return date_match.group() if date_match else None

def get_all_receipts(dir: str = 'receipts', file_prefix: str='item-details', sep: str='-'):
    receipt_files = [f for f in os.listdir(dir) if f.startswith(file_prefix)]
    receipt_items: List[ReceiptItem] = []
    for receipt_file in receipt_files:
        receipt_date = find_date(receipt_file, sep)
        if receipt_date is None:
            print("Could not find date for receipt ", receipt_file)
            continue
        receipt = create_receipt(os.path.join(dir,receipt_file), receipt_date)
        receipt_items.extend(receipt)
    return receipt_items

def create_receipt_item_alt(item: str, date: str):
    fields = item.split("\n")
    return create_receipt_item({'name': fields[0], 'price': fields[1], 'quantity': fields[-1]}, date)

def process_date_alt(item: str):
    date_pattern = r'(?i)\b(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s+(\d{1,2})\s+(\d{4})\b'
    date_match = re.search(date_pattern, item)
    if not date_match:
        return None
    month = date_match.group(1).upper()
    day = date_match.group(2).zfill(2)
    year = date_match.group(3)
    date_obj = datetime.strptime(f'{month} {day} {year}', '%b %d %Y')
    formatted_date = date_obj.strftime('%m-%d-%Y')
    return formatted_date

def get_all_receipts_alt(filename: str, dir: str = 'receipts', min_year: int = 2025):
    with open(os.path.join(dir,filename),'r') as f:
        receipts_str = f.read()
    receipt_items = re.split(r'\n{2,}', receipts_str)
    curr_date = ''
    items_list: List[ReceiptItem] = []
    for item in receipt_items:
        new_date = process_date_alt(item)
        if new_date is not None:
            curr_date = new_date
            continue
        if int(curr_date[-4:]) < min_year:
            print('alt receipts breaking on date ', curr_date)
            break
        item_formatted = create_receipt_item_alt(item, curr_date)
        items_list.append(item_formatted)
    return items_list

def make_csv(filename: str, receipts: List[ReceiptItem]):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = receipts[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for item in receipts:
            writer.writerow(item)

if __name__ == '__main__':
    receipts = get_all_receipts()
    alt_receipts_fname = input("Enter the name of the alternative receipts file (leave blank if none): ")
    if len(alt_receipts_fname) > 0:
        alt_receipts = get_all_receipts_alt(alt_receipts_fname)
        receipts.extend(alt_receipts)
    output_csv_fname = input("Enter name of output csv: ")
    make_csv(output_csv_fname, receipts)