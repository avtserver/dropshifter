// Copyright (c) 2023, MD Faiyaz Ansari and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Become a Retailer", {
// 	refresh(frm) {

// 	},
// });
// frappe.ui.form.on('Become a Retailer', {
//     refresh: function(frm) {
//         if(frm.is_new()) {
//             frm.set_value('user', frappe.session.user);
//             frm.set_value('status', 'Pending');
//         }
//     }
// });
frappe.ui.form.on('Become a Retailer', {
    status: function(frm) {
        if(frm.doc.status === 'Approved') {
            frappe.call({
                method: 'dropshifter.dropshifter.api.change_customer_group',
                args: {
                    'user': frm.doc.user
                },
                callback: function(response) {
                    // handle any post-operation actions here, if needed
                }
            });
        }
    }
});
