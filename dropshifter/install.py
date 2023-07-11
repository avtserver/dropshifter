# # install.py
# import frappe

# def after_install():
#     create_customer_groups()
#     create_price_lists()

# def create_customer_groups():
#     default_customer_groups = [
#         {"customer_group_name": "Retailer", "parent_customer_group": "All Customer Groups"},
#         {"customer_group_name": "Wholesaler", "parent_customer_group": "All Customer Groups"},
#     ]
#     for customer_group in default_customer_groups:
#         if not frappe.db.exists('Customer Group', customer_group["customer_group_name"]):
#             new_customer_group = frappe.get_doc({
#                 "doctype": "Customer Group",
#                 "customer_group_name": customer_group["customer_group_name"],
#                 "parent_customer_group": customer_group["parent_customer_group"],
#                 "is_group": "No"
#             })
#             new_customer_group.insert()

# def create_price_lists():
#     default_price_lists = [
#         {"price_list_name": "Retailer Selling Price", "currency": "INR", "buying_or_selling": "Selling"},
#         {"price_list_name": "Wholesaler Selling Price", "currency": "INR", "buying_or_selling": "Selling"},
#     ]
#     for price_list in default_price_lists:
#         if not frappe.db.exists('Price List', price_list["price_list_name"]):
#             new_price_list = frappe.get_doc({
#                 "doctype": "Price List",
#                 "price_list_name": price_list["price_list_name"],
#                 "currency": price_list["currency"],
#                 "buying_or_selling": price_list["buying_or_selling"],
#                 "enabled": 1
#             })
#             new_price_list.insert()
