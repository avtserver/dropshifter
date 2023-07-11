# Copyright (c) 2023, MD Faiyaz Ansari and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class DSStock(Document):
# 	pass
# frappe framework

import frappe

from frappe.model.document import Document

# class DSStock(Document):
#     def validate(self):
#         self.update_stock()

#     def update_stock(self):
#         if self.available_stock is None:
#             self.available_stock = 0

#         if self.add_stock:
#             self.available_stock += self.add_stock
#             self.add_stock = 0  # Reset the field for the next transaction

#         if self.sold_stock:
#             self.available_stock -= self.sold_stock
#             self.sold_stock = 0  # Reset the field for the next transaction

class DSStock(Document):
    def validate(self):
        self.update_stock()

    def update_stock(self):
        if self.available_stock is None:
            self.available_stock = 0

        # Check if add_stock attribute exists
        if hasattr(self, 'add_stock') and self.add_stock:
            self.available_stock += self.add_stock
            self.add_stock = 0  # Reset the field for the next transaction

        # Check if sold_stock attribute exists
        if hasattr(self, 'sold_stock') and self.sold_stock:
            self.available_stock -= self.sold_stock
            self.sold_stock = 0  # Reset the field for the next transaction




# Inside ds_stock.py
def create_ds_stock_from_item(doc, method):
    # Check if maintain_ds_stock is checked
    if doc.maintain_ds_stock:
        # Check if ds_initial_stock is provided
        if doc.ds_initial_stock is None:
            frappe.throw("Please provide the Initial DS Stock.")

        if doc.is_stock_item:
            doc.is_stock_item = 0  # Uncheck the 'Maintain Stock'
            doc.save()  # Save the change back to the Item doc
            frappe.msgprint("The 'Maintain Stock' was automatically unchecked because 'Maintain DS Stock' is checked.")
        
        # Create new DS Stock document
        ds_stock = frappe.get_doc({
            "doctype": "DS Stock",
            "item_code": doc.item_code,
            "item_name": doc.item_name,
            "available_stock": doc.ds_initial_stock,  # Set available_stock to Item's ds_initial_stock
        })
        ds_stock.insert(ignore_permissions=True)

        # //also create a DS Stock Transaction for further reference

        ds_stock_transaction = frappe.get_doc({
            "doctype": "DS Stock Transaction",
            "item_code": ds_stock.name,  # Use the name of the newly created DS Stock doc
            "item_name": doc.item_name,
            "date_of_transaction": frappe.utils.now_datetime(),  # Use the current date and time
            "type_of_entry": "Add Stock",
            "transaction_type": "Initial Stock",  # Specify the transaction type
            "add_stock": 0,  # Record the initial stock
            "entry_by": "System flow",
            "remarks": f"Initial stock of {doc.ds_initial_stock} was added upon item creation.",  # Add a note about the initial stock
        })
        ds_stock_transaction.insert(ignore_permissions=True)
        frappe.msgprint(f"DS Stock for item {doc.item_code} was created successfully with {doc.ds_initial_stock} Initial Stock!")

# unpublished website item script

# from frappe.website.doctype.website_item.website_item import WebsiteItem

def check_uncheck_published(doc, method):
    website_item = frappe.get_list("Website Item", filters={"item_code": doc.item_code}, fields=["name", "published"])

    for item in website_item:
        if doc.available_stock > 0:
            # If the stock is greater than 0 and the item is unpublished, publish it
            if not item.published:
                frappe.db.set_value("Website Item", item.name, "published", 1)
        else:
            # If the stock is 0 and the item is published, unpublish it
            if item.published:
                frappe.db.set_value("Website Item", item.name, "published", 0)
