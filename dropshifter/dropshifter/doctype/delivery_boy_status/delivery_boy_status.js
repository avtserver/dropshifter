// Copyright (c) 2023, MD Faiyaz Ansari and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Delivery Boy Status", {
// 	refresh(frm) {

// 	},
// });
// frappe.ui.form.on('Delivery Boy Status', {
//     refresh: function(frm) {
//         // Here we add custom actions to the form toolbar
//         frm.add_custom_button(__('Item Received'), function() {
//             // What happens when 'Item Received' is clicked
//             // You could create a new child doc here and update the fields as required
//             let child = frm.add_child('ds_db_status_update');
//             child.status = 'Item Received';
//             child.update_on = frappe.datetime.now_datetime();
//             child.update_by = frappe.session.user;
//             frm.refresh_field('ds_db_status_update');
//         });

//         frm.add_custom_button(__('Out for delivery'), function() {
//             // What happens when 'Out for Delivery' is clicked
//             let child = frm.add_child('ds_db_status_update');
//             child.status = 'Out for delivery';
//             child.update_on = frappe.datetime.now_datetime();
//             child.update_by = frappe.session.user;
//             frm.refresh_field('ds_db_status_update');
//         });

//         frm.add_custom_button(__('Delivered'), function() {
//             // What happens when 'Delivered' is clicked
//             let child = frm.add_child('ds_db_status_update');
//             child.status = 'Delivered';
//             child.update_on = frappe.datetime.now_datetime();
//             child.update_by = frappe.session.user;
//             frm.refresh_field('ds_db_status_update');
//             // Submit the document
//             frm.save('Submit');
//         });
//     },
// });

// 2
// frappe.ui.form.on('Delivery Boy Status', {
//     refresh: function(frm) {
//         // Flag to track the clicked state of each button
//         var itemReceivedClicked = false;
//         var outForDeliveryClicked = false;
//         var deliveredClicked = false;

//         frm.add_custom_button(__('Item Received'), function() {
//             if (!itemReceivedClicked) {
//                 itemReceivedClicked = true;

//                 // What happens when 'Item Received' is clicked
//                 // You could create a new child doc here and update the fields as required
//                 let child = frm.add_child('ds_db_status_update');
//                 child.status = 'Item Received';
//                 child.update_on = frappe.datetime.now_datetime();
//                 child.update_by = frappe.session.user;
//                 frm.refresh_field('ds_db_status_update');
//             }
//         });

//         frm.add_custom_button(__('Out for delivery'), function() {
//             if (!outForDeliveryClicked) {
//                 outForDeliveryClicked = true;

//                 // What happens when 'Out for Delivery' is clicked
//                 let child = frm.add_child('ds_db_status_update');
//                 child.status = 'Out for delivery';
//                 child.update_on = frappe.datetime.now_datetime();
//                 child.update_by = frappe.session.user;
//                 frm.refresh_field('ds_db_status_update');
//             }
//         });

//         frm.add_custom_button(__('Delivered'), function() {
//             if (!deliveredClicked) {
//                 deliveredClicked = true;

//                 // What happens when 'Delivered' is clicked
//                 let child = frm.add_child('ds_db_status_update');
//                 child.status = 'Delivered';
//                 child.update_on = frappe.datetime.now_datetime();
//                 child.update_by = frappe.session.user;
//                 frm.refresh_field('ds_db_status_update');
//                 // Submit the document
//                 frm.save('Submit');
//             }
//         });
//     },
// });
// 3

// frappe.ui.form.on('Delivery Boy Status', {
//     refresh: function(frm) {
//         // Flag to track the clicked state of each button
//         var itemReceivedClicked = false;
//         var outForDeliveryClicked = false;
//         var deliveredClicked = false;

//         frm.add_custom_button(__('Item Received'), function() {
//             if (!itemReceivedClicked) {
//                 itemReceivedClicked = true;

//                 // What happens when 'Item Received' is clicked
//                 // You could create a new child doc here and update the fields as required
//                 let child = frm.add_child('ds_db_status_update');
//                 child.status = 'Item Received';
//                 child.update_on = frappe.datetime.now_datetime();
//                 child.update_by = frappe.session.user;
//                 frm.refresh_field('ds_db_status_update');
//             }
//         });

//         frm.add_custom_button(__('Out for delivery'), function() {
//             if (!outForDeliveryClicked) {
//                 outForDeliveryClicked = true;

//                 // What happens when 'Out for Delivery' is clicked
//                 let child = frm.add_child('ds_db_status_update');
//                 child.status = 'Out for delivery';
//                 child.update_on = frappe.datetime.now_datetime();
//                 child.update_by = frappe.session.user;
//                 frm.refresh_field('ds_db_status_update');
//             }
//         });

//         frm.add_custom_button(__('Delivered'), function() {
//             if (!deliveredClicked) {
//                 frappe.call({
//                     method: 'frappe.client.get',
//                     args: {
//                         doctype: 'DS Order Delivery Status',
//                         filters: {
//                             'purchase_order': frm.doc.purchase_order
//                         }
//                     },
//                     callback: function(response) {
//                         var sales_invoice = response.message.sales_invoice;
//                         frappe.call({
//                             method: 'frappe.client.get',
//                             args: {
//                                 doctype: 'Sales Invoice',
//                                 name: sales_invoice
//                             },
//                             callback: function(r) {
//                                 if (r.message.status === 'Paid') {
//                                     deliveredClicked = true;
                                    
//                                     // What happens when 'Delivered' is clicked
//                                     let child = frm.add_child('ds_db_status_update');
//                                     child.status = 'Delivered';
//                                     child.update_on = frappe.datetime.now_datetime();
//                                     child.update_by = frappe.session.user;
//                                     frm.refresh_field('ds_db_status_update');
//                                     // Submit the document
//                                     frm.save('Submit');
//                                 } else {
//                                     // frappe.msgprint(__('Please make the payment for this order first.'));
//                                     frappe.msgprint(__('Please make the payment for this order first. You can pay it <a href="/app/sales-invoice/'+sales_invoice+'">here</a>.'));                        
//                                 }
//                             }
//                         });
//                     }
//                 });
//             }
//         });
//     },
// });
// frappe.ui.form.on('Delivery Boy Status', {
//     refresh: function(frm) {
//         // Get the last status from child table
//         var last_status = null;
//         if (frm.doc.ds_db_status_update && frm.doc.ds_db_status_update.length > 0) {
//             last_status = frm.doc.ds_db_status_update[frm.doc.ds_db_status_update.length - 1].status;
//         }

//         // Clear existing primary action
//         frm.page.clear_primary_action();

//         // Conditionally add the custom button based on the last status
//         if (frm.doc.docstatus !== 1) {
//             // Only add buttons if the document is not submitted
//             if (!last_status || last_status === 'Delivered') {
//                 // If no status yet, or last status is 'Delivered'
//                 frm.page.set_primary_action(__('Item Received'), function() {
//                     let child = frm.add_child('ds_db_status_update');
//                     child.status = 'Item Received';
//                     child.update_on = frappe.datetime.now_datetime();
//                     child.update_by = frappe.session.user;
//                     frm.doc.current_status = 'Item Received';  // update the current_status field
//                     frm.refresh_field('ds_db_status_update');
//                     frm.save().then(() => {
//                         frm.reload_doc();
//                     });
//                 });
//             } else if (last_status === 'Item Received') {
//                 // If last status is 'Item Received'
//                 frm.page.set_primary_action(__('Out for delivery'), function() {
//                     let child = frm.add_child('ds_db_status_update');
//                     child.status = 'Out for delivery';
//                     child.update_on = frappe.datetime.now_datetime();
//                     child.update_by = frappe.session.user;
//                     frm.doc.current_status = 'Out for delivery';  // update the current_status field
//                     frm.refresh_field('ds_db_status_update');
//                     frm.save().then(() => {
//                         frm.reload_doc();
//                     });
//                 });
//             } else if (last_status === 'Out for delivery') {
//                 // If last status is 'Out for delivery'
//                 frm.page.set_primary_action(__('Delivered'), function() {
//                     frappe.call({
//                         method: 'frappe.client.get',
//                         args: {
//                             doctype: 'DS Order Delivery Status',
//                             filters: {
//                                 'purchase_order': frm.doc.purchase_order
//                             }
//                         },
//                         callback: function(response) {
//                             var sales_invoice = response.message.sales_invoice;
//                             frappe.call({
//                                 method: 'frappe.client.get',
//                                 args: {
//                                     doctype: 'Sales Invoice',
//                                     name: sales_invoice
//                                 },
//                                 callback: function(r) {
//                                     if (r.message.status === 'Paid') {
//                                         let child = frm.add_child('ds_db_status_update');
//                                         child.status = 'Delivered';
//                                         child.update_on = frappe.datetime.now_datetime();
//                                         child.update_by = frappe.session.user;
//                                         frm.doc.current_status = 'Delivered';  // update the current_status field
//                                         frm.refresh_field('ds_db_status_update');
//                                         // Submit the document
//                                         frm.save('Submit').then(() => {
//                                             frm.reload_doc();
//                                         });
//                                     } else {
//                                         frappe.msgprint(__('Please make the payment for this order first. You can pay it <a href="/app/sales-invoice/'+sales_invoice+'">here</a>.'));
//                                     }
//                                 }
//                             });
//                         }
//                     });
//                 });
//             }
//         }
//     },
// });

frappe.ui.form.on('Delivery Boy Status', {
    refresh: function(frm) {
        frm.add_custom_button(__('Delivery Receipt'), 
        function(){
            // if the user clicks on "Yes"
            let print_format = "Delivery Receipt"; // change this to your print format
            window.open(`/printview?doctype=Delivery Boy Status&name=${frm.doc.name}&format=${print_format}`, "_blank");
        },
        );
    }
});

// update status field and child table log update


frappe.ui.form.on('Delivery Boy Status', 'update_status', function(frm) {
    // Check the selected status
    let selected_status = frm.doc.update_status;

    // Check if this status already exists in the child table
    let already_exists = frm.doc.ds_db_status_update.some(function(row) {
        return row.status === selected_status;
    });

    if (already_exists) {
        frappe.msgprint(__("Status '" + selected_status + "' is already updated."));
        return;
    }

    if (selected_status === 'Delivered') {
        frappe.call({
            method: 'frappe.client.get',
            args: {
                doctype: 'Sales Invoice',
                name: frm.doc.sales_invoice  // replace with the correct field name
            },
            callback: function(r) {
                if (r.message.status === 'Paid') {
                    // Create a new child doc and update the fields
                    let child = frm.add_child('ds_db_status_update');
                    child.status = 'Delivered';
                    child.update_on = frappe.datetime.now_datetime();
                    child.update_by = frappe.session.user;
                    frm.doc.current_status = 'Delivered';

                    frm.refresh_field('ds_db_status_update');
                    
                    // Submit the document
                    frm.save('Submit');
                } else {
                    frappe.msgprint(__('Please make the payment for this order first. You can pay it <a href="/app/sales-invoice/'+frm.doc.sales_invoice+'">here</a>.'));
                }
            }
        });
    } else {
        // Create a new child doc and update the fields
        let child = frm.add_child('ds_db_status_update');
        child.status = selected_status;
        child.update_on = frappe.datetime.now_datetime();
        child.update_by = frappe.session.user;
        frm.doc.current_status = selected_status;

        frm.refresh_field('ds_db_status_update');

        // Save the document
        frm.save();
    }
});

frappe.ui.form.on('Delivery Boy Status', 'refresh', function(frm) {
    // Disable the submit button unless the status is 'Delivered'
    frm.disable_save();
    if (frm.doc.update_status === 'Delivered') {
        frm.enable_save();
    }
});

