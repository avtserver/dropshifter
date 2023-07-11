frappe.ready(function() {
    // get field elements
    const userField = $('[data-fieldname="user"]');
    const statusField = $('[data-fieldname="status"]');

    // set field values
    userField.val(frappe.session.user);
    statusField.val('Pending');
});
