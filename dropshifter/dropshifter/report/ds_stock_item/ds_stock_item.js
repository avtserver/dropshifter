// Copyright (c) 2023, MD Faiyaz Ansari and contributors
// For license information, please see license.txt
/* eslint-disable */

// frappe.query_reports["DS Stock Item"] = {
// 	"filters": [

// 	]
// };


frappe.query_reports["DS Stock Item"] = {
    "filters": [
        // Add your filters here
    ],
    "formatter": function(value, row, column, data, default_formatter) {
        // Format your data if needed
    },
    "after_datatable_render": function(table) {
        // Use this to make any changes after your datatable is rendered
    },
    "chart": {
        "type": 'bar',
        "data": {
            "labels": frappe.report_utils.get_chart_labels("Item Code"),
            "datasets": [{
                'name': 'Available Stock',
                'values': frappe.report_utils.get_chart_values("Available Stock")
            }]
        }
    }
}


