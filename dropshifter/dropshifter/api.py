# import frappe

# @frappe.whitelist()
# def approve_retailer(user):
#     customer = frappe.get_all('Customer', filters={'user_id': user}, fields=['name'])
#     if customer:
#         frappe.db.set_value('Customer', customer[0].name, 'customer_group', 'Retailer')
#         frappe.db.commit()


import frappe

@frappe.whitelist()
def change_customer_group(user):
    contact_name = frappe.get_value('Contact', {'user': user}, 'name')
    if frappe.db.exists('Contact', contact_name):
        customer_link = frappe.get_value('Dynamic Link', {'parenttype': 'Contact', 'link_doctype': 'Customer', 'parent': contact_name}, 'link_name')
        if frappe.db.exists('Customer', customer_link):
            customer = frappe.get_doc('Customer', customer_link)
            customer.customer_group = 'Retailer'
            customer.save()
