// Copyright (c) 2023, MD Faiyaz Ansari and contributors
// For license information, please see license.txt
/* eslint-disable */

// frappe.query_reports["Supplier Order Confirmation Report"] = {
// 	"filters": [

// 	]
// };
frappe.query_reports["Supplier Order Confirmation Report"] = {
    "filters": [
        {
            "fieldname":"purchase_order",
            "label": __("Purchase Order"),
            "fieldtype": "Link",
            "options": "Purchase Order"
        },
        {
            "fieldname":"delivery_due_date",
            "label": __("Delivery Due Date"),
            "fieldtype": "Date"
        },
        {
            "fieldname":"status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": "\nApproved\nCancelled\nHold"
        },
        // {
        //     "fieldname":"comment",
        //     "label": __("Comment"),
        //     "fieldtype": "Data"
        // }
    ]
}
