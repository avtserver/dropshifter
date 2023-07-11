frappe.ui.form.on('Sales Order Item', {
	item_code: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		
		// Add a short delay before setting the supplier field
		setTimeout(function() {
			if (child.supplier_name) {
				child.supplier = child.supplier_name;

				// If supplier has value, check the field "delivered_by_supplier"
				child.delivered_by_supplier = 1;
				frm.refresh_field("items");
			} else {
				// If supplier doesn't have a value, uncheck the field "delivered_by_supplier"
				child.delivered_by_supplier = 0;
			}
		}, 500);  // 500 milliseconds delay
	}
});
