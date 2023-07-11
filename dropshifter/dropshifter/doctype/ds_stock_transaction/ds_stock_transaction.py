# Copyright (c) 2023, MD Faiyaz Ansari and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class DSStockTransaction(Document):
# 	pass
# from __future__ import unicode_literals
# import frappe
# from frappe.model.document import Document

# class DSStockTransaction(Document):
#     def validate(self):
#         # your validation logic here
#         self.update_stock_in_ds_stock()

#     def update_stock_in_ds_stock(self):
#         # Your logic to fetch DS Stock Document using self.item_code and then
#         # add or subtract the self.add_stock or self.sold_stock amount from it.
#         ds_stock_doc = frappe.get_doc("DS Stock", self.item_code)

#         if self.add_stock:
#             ds_stock_doc.available_stock += self.add_stock
#         if self.sold_stock:
#             ds_stock_doc.available_stock -= self.sold_stock

#         ds_stock_doc.save()

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import nowdate
from frappe import _


class DSStockTransaction(Document):
    def __init__(self, *args, **kwargs):
        super(DSStockTransaction, self).__init__(*args, **kwargs)

        # If the document is new and date_of_transaction is not set, set it to today's date
        if self.is_new() and not self.date_of_transaction:
            self.date_of_transaction = nowdate()

    def validate(self):
        # your validation logic here
        self.update_stock_in_ds_stock()

    def update_stock_in_ds_stock(self):
        # Your logic to fetch DS Stock Document using self.item_code and then
        # add or subtract the self.add_stock or self.sold_stock amount from it.
        ds_stock_doc = frappe.get_doc("DS Stock", self.item_code)

        if self.add_stock:
            ds_stock_doc.available_stock += self.add_stock
        if self.sold_stock:
            ds_stock_doc.available_stock -= self.sold_stock

        ds_stock_doc.save()

# add functio for hook.py

def create_from_sales_order(doc, method):
    for item in doc.items:  # Loop over the items in the Sales Order
        # Check if the item_code exists in the DS Stock doctype
        if frappe.db.exists('DS Stock', {'item_code': item.item_code}):
            create_stock_entry(item, doc)
        else:
            frappe.throw(_(f"Could not find Item_code: {item.item_code} in DS Stock"))

def create_stock_entry(item, doc):
    # Get the name of the DS Stock document with the item_code
    ds_stock_name = frappe.get_value('DS Stock', {'item_code': item.item_code}, 'name')

    stock_entry = frappe.get_doc({
        "doctype": "DS Stock Transaction",
        "item_code": ds_stock_name,  # use the name of DS Stock document here
        "item_name": item.item_name,
        "sales_order_ref": doc.name,
        "entry_by": "System flow",
        "type_of_entry": "Sold Stock",
        "transaction_type": "Submitted sales order",  # Specify the transaction type
        "date_of_transaction": doc.transaction_date,
        "sold_stock": item.qty,  # Update this to use the quantity from the Sales Order item
       "remarks": f"Create from Sales order - {doc.name} ",  # Add a note about the initial stock
        })
    
    # stock_entry.submit()
    stock_entry.save()
    frappe.msgprint(f"DS Stock Transaction also updated successfully for {item.item_code}")



# # //on canceled sale order status chang

def on_sales_order_cancelled(doc, method):
    for item in doc.items:  # Loop over the items in the Sales Order
        # Check if the item_code exists in the DS Stock doctype
        if frappe.db.exists('DS Stock', {'item_code': item.item_code}):
            create_cancelled_stock_entry(item, doc)
        else:
            frappe.throw(_(f"Could not find Item_code: {item.item_code} in DS Stock"))

def create_cancelled_stock_entry(item, doc):
    # Get the name of the DS Stock document with the item_code
    ds_stock_name = frappe.get_value('DS Stock', {'item_code': item.item_code}, 'name')

    cancellation_entry = frappe.get_doc({
        "doctype": "DS Stock Transaction",
        "item_code": ds_stock_name,  # use the name of DS Stock document here
        "item_name": item.item_name,
        "sales_order_ref": doc.name,
        "date_of_transaction": doc.transaction_date,
        "add_stock": item.qty,  # Add the cancelled quantity back to the available stock
        "transaction_type": "Cancelled"  # Specify the transaction type
    })
    cancellation_entry.insert()
    cancellation_entry.submit()


        # The new Item's initial stock should now be reflected in the DS Stock's available_stock.


# new code for hook.py

# class DSStockTransaction(Document):
#     def validate(self):
#         self.update_ds_stock()

#     def update_ds_stock(self):
#         ds_stock = frappe.get_doc('DS Stock', self.item_code)
#         ds_stock.append('transactions', {
#             'transaction_type': self.transaction_type,
#             'add_stock': self.add_stock,
#             'sold_stock': self.sold_stock
#         })
#         ds_stock.save()

# def create_from_sales_order(doc, method):
#     for item in doc.items:  
#         if frappe.db.exists('DS Stock', {'item_code': item.item_code}):
#             create_stock_entry(item, doc, 'Sold')
#         else:
#             frappe.throw(_(f"Could not find Item_code: {item.item_code} in DS Stock"))

# def create_cancelled_stock_entry(doc, method):
#     for item in doc.items:  
#         if frappe.db.exists('DS Stock', {'item_code': item.item_code}):
#             create_stock_entry(item, doc, 'Cancelled')
#         else:
#             frappe.throw(_(f"Could not find Item_code: {item.item_code} in DS Stock"))

# def create_stock_entry(item, doc, transaction_type):
#     ds_stock_name = frappe.get_value('DS Stock', {'item_code': item.item_code}, 'name')

#     stock_entry = frappe.get_doc({
#         "doctype": "DS Stock Transaction",
#         "item_code": ds_stock_name,  
#         "item_name": item.item_name,
#         "sales_order_ref": doc.name,
#         "date_of_transaction": doc.transaction_date,
#         "add_stock": item.qty if transaction_type != 'Sold' else 0,  
#         "sold_stock": item.qty if transaction_type == 'Sold' else 0,
#         "transaction_type": transaction_type,
#     })
#     stock_entry.insert()
#     stock_entry.submit()

