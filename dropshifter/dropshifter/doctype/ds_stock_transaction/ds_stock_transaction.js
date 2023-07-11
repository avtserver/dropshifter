// Copyright (c) 2023, MD Faiyaz Ansari and contributors
// For license information, please see license.txt

// frappe.ui.form.on("DS Stock Transaction", {
// 	refresh(frm) {

// 	},
// });
// --------------------------------------------
frappe.ui.form.on('DS Stock Transaction', {
    item_code: function(frm) {
        if(frm.doc.item_code){
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'DS Stock',
                    name: frm.doc.item_code
                },
                callback: function(response) {
                    let ds_stock = response.message;
                    if(ds_stock){
                        frm.set_value('current_stock', ds_stock.available_stock);
                    }else{
                        frm.set_value('current_stock', null);
                    }
                }
            });
        }else{
            frm.set_value('current_stock', null);
        }
    },

    after_save: function(frm) {
        var interval = setInterval(function(){
            if(!frm.is_saving){
                clearInterval(interval);
                frappe.call({
                    method: 'frappe.client.get',
                    args: {
                        doctype: 'DS Stock',
                        name: frm.doc.item_code
                    },
                    callback: function(response) {
                        let ds_stock = response.message;
                        if(ds_stock){
                            frappe.show_alert(`Current available stock: ${ds_stock.available_stock}`);
                          
                            frappe.msgprint({
                                title: __('Updated Stock'),
                                indicator: 'green',
                                message: `<div style="text-align: center;">Current available stock: ${ds_stock.available_stock}</div>`
                            });
                         


                           
                        }
                    }
                });
            }
        }, 100);
    }
});


//addition conditions


// Inside ds_stock_transaction.js

frappe.ui.form.on('DS Stock Transaction', {
    type_of_entry: function(frm) {
        if (frm.doc.type_of_entry == 'Add Stock') {
            frm.set_value('transaction_type', 'Add Stock');
        } else if (frm.doc.type_of_entry == 'Sold Stock') {
            frm.set_value('transaction_type', 'Revoke Stock');
        }
    }
});


frappe.ui.form.on('DS Stock Transaction', {
    onload: function(frm) {
        // Hide the transaction_type field when the form is loaded
        frm.toggle_display('Sales_order_ref', false);
    },
    type_of_entry: function(frm) {
        if (frm.doc.type_of_entry == 'Sold Stock') {
         }
        // Show the transaction_type field when type_of_entry field has a value
        frm.toggle_display('Sales_order_ref', true);
    }
});

