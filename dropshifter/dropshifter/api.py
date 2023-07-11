import frappe

@frappe.whitelist()
def approve_retailer(user):
    customer = frappe.get_all('Customer', filters={'user_id': user}, fields=['name'])
    if customer:
        frappe.db.set_value('Customer', customer[0].name, 'customer_group', 'Retailer')
        frappe.db.commit()
