# Copyright (c) 2023, MD Faiyaz Ansari and contributors
# For license information, please see license.txt

# import frappe


def execute(filters=None):
	columns, data = [], []
	return columns, data

# import frappe
# from frappe import _

# def execute(filters=None):
#     if filters is None:
#         filters = {}

#     columns = get_columns()
#     data = get_data(filters)

#     return columns, data

# def get_columns():
#     return [
#         _("Date") + ":Date:80",
#         _("Delivery Boy") + ":Link/User:120",
#         _("Status") + "::120",
#         _("Number of Orders") + ":Int:100"
#     ]

# def get_data(filters):
#     conditions = ""

#     if filters.get("purchase_order"):
#         conditions += " AND delivery_boy_status.purchase_order = %(purchase_order)s"

#     data = frappe.db.sql("""
#         SELECT
#             ds_db_status_update.update_on,
#             delivery_boy_status.update_by,
#             ds_db_status_update.status,
#             COUNT(*)
#         FROM
#             `tabDelivery Boy Status` AS delivery_boy_status
#         INNER JOIN
#             `tabDS DB Status Update` AS ds_db_status_update
#         ON
#             delivery_boy_status.name = ds_db_status_update.parent
#         WHERE
#             DATE(ds_db_status_update.update_on) = CURDATE() 
#             {conditions}
#         GROUP BY
#             ds_db_status_update.update_on, 
#             delivery_boy_status.update_by, 
#             ds_db_status_update.status
#         ORDER BY
#             ds_db_status_update.update_on ASC, 
#             delivery_boy_status.update_by ASC, 
#             ds_db_status_update.status ASC
#     """.format(conditions=conditions), filters, as_list=True)

#     return data
