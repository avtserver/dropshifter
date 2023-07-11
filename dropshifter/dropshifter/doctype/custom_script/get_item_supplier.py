# import frappe
# from frappe.model.document import Document

# # def create_ds_stock(doc, method):
# #     if doc.is_new():
# #         # Create new DS Stock document
# #         ds_stock = frappe.get_doc({
# #             "doctype": "DS Stock",
# #             "item_code": doc.item_code,
# #             "item_name": doc.item_name,
# #             "available_stock": doc.ds_initial_stock,  # Set available_stock to Item's ds_initial_stock
# #         })
# #         ds_stock.insert(ignore_permissions=True)
# # in your_custom_app/your_custom_app/api.py

# # in your_custom_app/your_custom_app/api.py

# @frappe.whitelist()
# def get_item_supplier(item_code):
#     item_supplier = frappe.get_list('Item Supplier', filters={'parent': item_code}, fields=['supplier'])
#     if item_supplier:
#         return item_supplier[0].supplier
#     return None

