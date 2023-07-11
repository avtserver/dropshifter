// Copyright (c) 2023, MD Faiyaz Ansari and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Become a Wholesaler", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Become a Wholesaler', {
    refresh: function(frm) {
        if(frm.is_new()) {
            frm.set_value('user', frappe.session.user);
            frm.set_value('status', 'Pending');
        }
    }
});
