frappe.ready(function() {
    if (frappe.session.user !== 'Guest') {
        frappe.call('frappe.client.get', {
            'doctype': 'Customer',
            'filters': {
                'user_id': frappe.session.user
            }
        }).then(response => {
            let customer_group = response.message.customer_group;
            if (customer_group == 'Individual') {
                frappe.msgprint({
                    title: __('Become a Retailer or Wholesaler'),
                    message: __('You are currently an individual customer. Would you like to become a retailer or wholesaler? <a href="/landing_page">Click here</a> to apply.'),
                    indicator: 'blue',
                    wide: true
                });
            }
        });
    }
});
