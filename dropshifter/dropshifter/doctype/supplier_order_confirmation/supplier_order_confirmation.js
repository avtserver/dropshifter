// Copyright (c) 2023, MD Faiyaz Ansari and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Supplier Order Confirmation", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Supplier Order Confirmation', {
    refresh: function(frm) {
        if (frappe.user.has_role('Administrator')) {
            frm.add_custom_button(__('Create Invoice'), function() {
                // Get the purchase order from the current Supplier Order Confirmation
                let purchase_order = frm.doc.purchase_order;

                // Check if a purchase order was found
                if (purchase_order) {
                    // Navigate to the Purchase Order document
                    frappe.set_route("Form", "Purchase Order", purchase_order);
                } else {
                    frappe.msgprint(__("Please select a Purchase Order first."));
                }
            });
        }
    },
});

// frappe.ui.form.on('Supplier Order Confirmation', {
//     refresh: function(frm) {
//         // clear existing primary action
//         frm.page.clear_primary_action();

//         // add your custom primary action
//         frm.page.set_primary_action(__('Create Invoice'), function() {
//             // Get the purchase order from the current Supplier Order Confirmation
//             let purchase_order = frm.doc.purchase_order;

//             // Check if a purchase order was found
//             if (purchase_order) {
//                 // Navigate to the Purchase Order document
//                 frappe.set_route("Form", "Purchase Order", purchase_order);
//             } else {
//                 frappe.msgprint(__("Please select a Purchase Order first."));
//             }
//         });
//     },
// });
frappe.ui.form.on("Supplier Order Confirmation", {
    on_submit: function(frm) {
        if (frm.doc.status === "Approved") {
            frappe.confirm(
                'Do you want to print the Approved Order Receipt?',
                function(){
                    // if the user clicks on "Yes"
                    let print_format = "Supplier Approved Order Receipt"; // change this to your print format
                    window.open(`/printview?doctype=Supplier Order Confirmation&name=${frm.doc.name}&format=${print_format}`, "_blank");
                },
                function(){
                    // if the user clicks on "No" or cancels the prompt
                    // do nothing
                }
            )
        }
        else if (frm.doc.status === "Cancelled") {
            frappe.msgprint('This order has been cancelled.', 'Order Cancelled');
        }
        else if (frm.doc.status === "Hold") {
            frappe.msgprint('This order is on hold.', 'Order On Hold');
        }
    }
});
frappe.ui.form.on('Supplier Order Confirmation', {
        refresh: function(frm) {
            frm.add_custom_button(__('Print'), 
            function(){
                // if the user clicks on "Yes"
                let print_format = "Supplier Approved Order Receipt"; // change this to your print format
                window.open(`/printview?doctype=Supplier Order Confirmation&name=${frm.doc.name}&format=${print_format}`, "_blank");
            },
            );
        }
    });
    