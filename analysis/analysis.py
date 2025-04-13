#!/usr/bin/env python
import sys
import os
from typing import TypedDict, Dict, List
import json
import re

class ReceiptItem(TypedDict):
    name: str
    quantity: float
    price: float

def create_receipt_item(itemDict: Dict):
    name: str = itemDict['name']
    quantityMatch = re.search(r'\d+\.?\d{,2}', itemDict['quantity'])
    if quantityMatch is None:
        print(itemDict['quantity'])
        raise ValueError("Could not find quantity!")
    quantityStr = quantityMatch.group()
    priceStr: str = itemDict['price']
    quantity = float(quantityStr)
    price = float(priceStr[1:])
    return ReceiptItem(name=name, quantity=quantity, price=price)

def create_receipt(jsonFilename: str):
    with open(jsonFilename, 'r') as f:
        list_json = json.load(f)
    receipt = [create_receipt_item(it) for it in list_json]
    return receipt

def find_date(date_string: str, sep: str):
    date_pattern = r'\d{2}'+sep+r'\d{2}'+sep+r'\d{4}'
    date_match = re.search(date_pattern, date_string)
    return date_match.group() if date_match else None

def get_all_receipts(dir: str = 'receipts', file_prefix: str='item-details', sep: str='-'):
    receipt_files = [f for f in os.listdir(dir) if f.startswith(file_prefix)]
    receipts: Dict[str, List[ReceiptItem]] = {}
    for receipt_file in receipt_files:
        receipt_date = find_date(receipt_file, sep)
        if receipt_date is None:
            print("Could not find date for receipt ", receipt_file)
            continue
        receipt = create_receipt(os.path.join(dir,receipt_file))
        if receipt_date in receipts.keys():
            receipts[receipt_date].append(receipt)
        else:
            receipts[receipt_date] = receipt
    return receipts

if __name__ == '__main__':
    receipts = get_all_receipts()
    