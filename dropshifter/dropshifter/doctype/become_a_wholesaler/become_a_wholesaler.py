# Copyright (c) 2023, MD Faiyaz Ansari and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class BecomeaWholesaler(Document):
# 	pass

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class BecomeaWholesaler(Document):
    def on_update(self):
        if self.status == 'Approved':
            # Get the linked contact from the user
            contact = frappe.get_all('Contact', filters={'user': self.user}, fields=['name'])
            if contact:
                contact = contact[0].name
                # Get the linked customer from the contact
                customer_link = frappe.get_all('Dynamic Link', filters={'parenttype': 'Contact', 'link_doctype': 'Customer', 'parent': contact}, fields=['link_name'])
                if customer_link:
                    customer_name = customer_link[0].link_name
                    customer = frappe.get_doc('Customer', customer_name)
                    customer.customer_group = 'Wholesaler'
                    customer.gst_category = self.gst_category  # Assuming 'gst_category' is the field name in your DocType
                    customer.gstin = self.gstin  # Assuming 'gstin' is the field name in your DocType
                    customer.pan = self.pan  # Assuming 'pan' is the field name in your DocType
                    customer.customer_type = self.customer_type  # Assuming 'customer_type' is the field name in your DocType
                    customer.save()
