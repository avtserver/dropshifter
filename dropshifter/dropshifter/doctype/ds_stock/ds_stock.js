// Copyright (c) 2023, MD Faiyaz Ansari and contributors
// For license information, please see license.txt

// frappe.ui.form.on("DS Stock", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('DS Stock', {
    refresh: function(frm) {
        // add a custom button to the form
        // add primary button
        frm.page.set_primary_action(__('Update Stock'), function() {
        // frm.add_custom_button(__('Update Stock'), function() {
            // set the route options to prefill the 'item_code' field in the new document
            frappe.route_options = {
                "item_code": frm.doc.item_code
            };
            // create a new DS Stock Transaction document
            frappe.new_doc('DS Stock Transaction');

            //set value on ds stock transaction item_code field
        });
    }
});


