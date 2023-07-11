# import frappe

# @frappe.whitelist()
# def approve_retailer(user):
#     customer = frappe.get_all('Customer', filters={'user_id': user}, fields=['name'])
#     if customer:
#         frappe.db.set_value('Customer', customer[0].name, 'customer_group', 'Retailer')
#         frappe.db.commit()
# dropshifter/dropshifter/api.py
# for retauler

import frappe

def approve_retailer(doc, method):
    if doc.status == 'Approved':
        # Get the linked contact from the user
        contact = frappe.get_all('Contact', filters={'user': doc.user}, fields=['name'])
        if contact:
            contact = contact[0].name
            # Get the linked customer from the contact
            customer_link = frappe.get_all('Dynamic Link', filters={'parenttype': 'Contact', 'link_doctype': 'Customer', 'parent': contact}, fields=['link_name'])
            if customer_link:
                customer_name = customer_link[0].link_name
                customer = frappe.get_doc('Customer', customer_name)
                customer.customer_group = 'Retailer'
                customer.gst_category = doc.gst_category
                customer.gstin = doc.gstin
                customer.pan = doc.pan
                customer.customer_type = doc.customer_type
                customer.save()
