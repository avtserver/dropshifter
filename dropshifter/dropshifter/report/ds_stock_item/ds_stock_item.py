# Copyright (c) 2023, MD Faiyaz Ansari and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data
import frappe
from frappe import _

message = "DS Stock Item Report"

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters)
    return columns, data, message

def get_columns():
    return [
        _("Item Code") + ":Link/Item:100",
        _("Item Name") + "::150",
        _("Available Stock") + ":Float:100",
        _("Last Modified") + ":Datetime:150",
        _("Modified By") + "::150"
    ]

def get_data(filters):
    data = frappe.db.sql("""
        SELECT
            ds.item_code,
            ds.item_name,
            ds.available_stock,
            ds.modified,
            ds.modified_by
        FROM
            `tabDS Stock` as ds
        ORDER BY
            ds.modified DESC
    """, as_list=True)

    return data

# import frappe
# from frappe import _

# def execute(filters=None):
#     columns, data = [], []
#     columns = get_columns()
#     data = get_data(filters)
#     chart = get_chart(data)
#     message = get_summary(data)
#     return columns, data, message, chart

# def get_columns():
#     return [
#         _("Item Code") + ":Link/Item:100",
#         _("Item Name") + "::150",
#         _("Available Stock") + ":Float:100",
#         _("Last Modified") + ":Datetime:150",
#         _("Modified By") + "::150"
#     ]

# def get_data(filters):
#     data = frappe.db.sql("""
#         SELECT
#             ds.item_code,
#             ds.item_name,
#             ds.available_stock,
#             ds.modified,
#             ds.modified_by
#         FROM
#             `tabDS Stock` as ds
#         ORDER BY
#             ds.modified DESC
#     """, as_list=True)

#     return data

# def get_chart(data):
#     labels = [row[0] for row in data] # 'item_code'
#     datasets = [{'name': 'Available Stock', 'values': [row[2] for row in data]}] # 'available_stock'

#     chart = {
#         "data": {
#             'labels': labels,
#             'datasets': datasets
#         },
#         "type": "bar"
#     }

#     return chart

# def get_summary(data):
#     total_items = len(data)
#     less_than_50 = sum(1 for row in data if row[2] < 50)
#     greater_than_50 = sum(1 for row in data if row[2] > 50)

#     message = """
#     <div style='border: 1px solid #d1d8dd; border-radius: 5px; padding: 20px; margin: 20px 0;'>
#         <h5 style='margin-bottom: 20px;'>Summary Report</h5>
#         <table class='table table-bordered'>
#             <thead>
#                 <tr>
#                     <th>Total Items</th>
#                     <th>Items with Available Stock &lt; 50</th>
#                     <th>Items with Available Stock &gt; 50</th>
#                 </tr>
#             </thead>
#             <tbody>
#                 <tr>
#                     <td>{}</td>
#                     <td>{}</td>
#                     <td>{}</td>
#                 </tr>
#             </tbody>
#         </table>
#     </div>
#     """.format(total_items, less_than_50, greater_than_50)

#     return message
