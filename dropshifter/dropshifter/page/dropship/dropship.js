frappe.pages['dropship'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Dropship Dashboard',
        single_column: true
    });

    page.main.html(frappe.render_template("dropship", {}));

    // Fetch DS Stock items and display them in the list   1

	frappe.call({
		method: "frappe.client.get_list",
		args: {
			doctype: "DS Stock",
			fields: ["name", "item_name", "item_code", "available_stock", "modified"],
		},
		callback: function(r) {
			var html = '';
			var lowStockCount = 0; // Counter for DS Stock items with stock less than 50
	
			// Sort the array by 'available_stock' field
			r.message.sort(function(a, b) {
				return a.available_stock - b.available_stock;
			});
			
			$.each(r.message || [], function(i, d) {
				// Convert creation date to DD/MM/YYYY format
				let creation_date = frappe.datetime.str_to_user(d.modified);
	
				html += `<tr>
						   <td>${i+1}</td>
						   <td>${d.name}</td>
						   <td>${d.item_name}</td>
						   <td class='item-code'>${d.item_code}</td>
						   <td>${d.available_stock}</td>
						   <td>${creation_date}</td>
						 </tr>`;
	
				// Increase the lowStockCount if available_stock is less than 50
				if (d.available_stock < 50) {
					lowStockCount++;
				}
			});
			$('#ds-stock-list tbody').html(html);
	
			// Update the total number card
			$('#total-ds-stock').text(r.message.length);
			
			// Update the low stock count card
			$('#low-stock-ds-items').text(lowStockCount);
		}
	});
	
	

    // Search function
    $("#search-ds-stock").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#ds-stock-list tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
}


2
