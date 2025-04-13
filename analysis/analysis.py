#!/usr/bin/env python
import sys
import os
from typing import TypedDict, Dict
import json

class ReceiptItem(TypedDict):
    name: str
    quantity: int
    price: float

def create_receipt_item(itemDict: Dict):
    name: str = itemDict['name']
    quantityStr: str = itemDict['quantity']
    priceStr: str = itemDict['price']
    quantity = int(quantityStr.split()[-1])
    price = float(priceStr[1:])
    return ReceiptItem(name, quantity, price)

def create_receipt(jsonFilename: str):
    with open(jsonFilename, 'r') as f:
        list_json = json.load(f)
    print(list_json)

if __name__ == '__main__':
    create_receipt('receipts/item-details-01-10-2025.json')