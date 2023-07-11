# Copyright (c) 2023, MD Faiyaz Ansari and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    if not filters: filters = {}

    columns = get_columns()
    data = get_data(filters)

    return columns, data

def get_columns():
    return [
        _("Purchase Order") + ":Link/Purchase Order:120",
        _("Delivery Due Date") + ":Date:120",
        _("Status") + ":Data:120",
      
        _("Comment") + ":Data:300",  # Adding comment here
    ]

def get_data(filters):
    conditions = get_conditions(filters)

    return frappe.db.sql("""
        SELECT
            purchase_order,
            delivery_due_date,
            status,
            comment  # Adding comment here
        FROM
            `tabSupplier Order Confirmation`
        WHERE
            docstatus < 2 %s
        ORDER BY
            modified desc
    """ % conditions, filters, as_dict=1)


def get_conditions(filters):
    conditions = ""
    if filters.get("purchase_order"): conditions += " and purchase_order=%(purchase_order)s"
    if filters.get("delivery_due_date"): conditions += " and delivery_due_date=%(delivery_due_date)s"
    if filters.get("status"): conditions += " and status=%(status)s"
    if filters.get("comment"): conditions += " and comment=%(comment)s"  # Adding condition for comment

    return conditions
