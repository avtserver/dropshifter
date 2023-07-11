# Copyright (c) 2023, MD Faiyaz Ansari and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DeliveryBoyStatus(Document):
	pass


# def update_po_status_on_submit(doc, method):
#     # Check if Purchase Order exists
#     if doc.purchase_order:
#         # Update status of the Purchase Order
#         frappe.db.set_value("Purchase Order", doc.purchase_order, "status", "Delivered")


def update_po_status_on_submit(doc, method):
    # Check if Purchase Order exists
    if doc.purchase_order:
        # Update status of the Purchase Order
        frappe.db.set_value("Purchase Order", doc.purchase_order, "status", "Delivered")
        
        # Get the Purchase Order doc
        purchase_order_doc = frappe.get_doc("Purchase Order", doc.purchase_order)

        # For each item in the Purchase Order, fetch related Sales Order and update status
        for item in purchase_order_doc.items:
            if item.sales_order:
                # Update status of the Sales Order to 'Completed'
                frappe.db.set_value("Sales Order", item.sales_order, "status", "Completed")
                # sales_order = frappe.get_doc("Sales Order", item.sales_order)
                # # Call method to update linked documents
                # update_status("Completed", sales_order.name)
