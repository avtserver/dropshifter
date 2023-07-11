# Copyright (c) 2023, MD Faiyaz Ansari and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class DSOrderDeliveryStatus(Document):
# 	pass


from frappe.model.document import Document
import frappe
from frappe.utils import nowdate
# NameError: name '_' is not defined
from frappe import _

class DSOrderDeliveryStatus(Document):
    pass


# sales order submit

@frappe.whitelist()
def create_status_and_log(doc, method):
    # doc here represents the Sales Order document

    # Create DS Order Delivery Status document
    delivery_status = frappe.new_doc('DS Order Delivery Status')
    delivery_status.sales_order = doc.name
    delivery_status.ds_order_status = 'Pending'
    # delivery_status.sales_order_item = ", ".join([item.item_code for item in doc.items]) # Commented out
    delivery_status.status_updated_on = nowdate()
    # delivery_status.comment = 'Sales order submitted.'
    delivery_status.comment = 'Sales order {} submitted.'.format(doc.name)
    
    delivery_status.save()
    
    # Create DS Order Status Log document and append it to the parent document
    status_log = delivery_status.append('status_logs', {})
    status_log.previous_status = 'Order Placed'
    status_log.new_status = 'Pending'
    status_log.change_time = nowdate()
    status_log.changed_by = frappe.session.user  # Capture the current user
    status_log.sales_order = doc.name
    status_log.comment = 'Sales order submitted.'
	# status_log.comment = 'Sales order {} submitted.'.format(doc.name)
    
    

    # Save DS Order Delivery Status document which also saves the child table 'DS Order Status Log'
    delivery_status.save()
        # Print a message
    frappe.msgprint(_("DS Order Status Updated to {0}").format(status_log.new_status))

#sale invoice submit

@frappe.whitelist()
def update_status_and_log(doc, method):
    # doc here represents the Sales Invoice document

    # Retrieve the name of the sales order from the first item in the sales invoice
    # Make sure all the items in your sales invoice belong to the same sales order
    sales_order = doc.items[0].sales_order if doc.items else None

    # Check if a sales order was found
    if sales_order:
        # Retrieve the existing DS Order Delivery Status document
        try:
            delivery_status = frappe.get_doc('DS Order Delivery Status', {'sales_order': sales_order})
        except frappe.DoesNotExistError:
            frappe.throw(_("DS Order Delivery Status for Sales Order {0} not found.").format(sales_order))
        
        # Capture the previous status before updating it
        previous_status = delivery_status.ds_order_status
        delivery_status.sales_invoice = doc.name
        delivery_status.ds_order_status = 'Invoice Issued, Awaiting Payment'
        delivery_status.status_updated_on = nowdate()
        delivery_status.comment = 'Sales invoice {} submitted.'.format(doc.name)

        # Append a new status log to the document
        status_log = delivery_status.append('status_logs', {})
        status_log.sales_order = sales_order  # Set the sales_order in the child table
        status_log.previous_status = previous_status  # Add the previous status to the log
        status_log.new_status = 'Invoice Issued, Awaiting Payment'
        status_log.change_time = nowdate()
        status_log.changed_by = frappe.session.user  # Capture the current user
        status_log.comment = 'Sales invoice {} Issued, Awaiting Payment.'.format(doc.name)

        # Save the changes to DS Order Delivery Status document which also saves the new status log
        delivery_status.save()

        # Print a message
        frappe.msgprint(_("DS Order Status Updated to {0}").format(status_log.new_status))
    else:
        frappe.throw(_("Sales Order not found in Sales Invoice items."))

# add current payment status from invoice to DS Order Payment Status doc

# @frappe.whitelist()
# def add_entry_to_ds_order_payment_status(doc, method):
#     # doc here represents the Sales Invoice document

#     # Retrieve the name of the sales order from the first item in the sales invoice
#     # Make sure all the items in your sales invoice belong to the same sales order
#     sales_order = doc.items[0].sales_order if doc.items else None

#     if sales_order:
#         # Create a new DS Order Payment Status document
#         ds_order_payment_status = frappe.new_doc('DS Order Payment Status')
#         ds_order_payment_status.sales_order = sales_order
#         ds_order_payment_status.sales_invoice = doc.name
#         ds_order_payment_status.insert()
        
#         # Print a message
#         frappe.msgprint(_("DS Order Payment Status Updated for Sales Invoice {0}").format(doc.name))
#     else:
#         frappe.throw(_("Sales Order not found in Sales Invoice items."))



# Purchase Order Hoo

@frappe.whitelist()
def update_status_and_log_on_po_submit(doc, method):
    # doc here represents the Purchase Order document

    # Retrieve the name of the sales order from the first item in the purchase order
    # Make sure all the items in your purchase order belong to the same sales order
    sales_order = doc.items[0].sales_order if doc.items else None

    # Check if a sales order was found
    if sales_order:
        # Retrieve the existing DS Order Delivery Status document
        try:
            delivery_status = frappe.get_doc('DS Order Delivery Status', {'sales_order': sales_order})
        except frappe.DoesNotExistError:
            frappe.throw(_("DS Order Delivery Status for Sales Order {0} not found.").format(sales_order))
        
        # Capture the previous status before updating it
        previous_status = delivery_status.ds_order_status
        delivery_status.ds_order_status = 'Supplier Received Order'
        delivery_status.status_updated_on = nowdate()
        delivery_status.purchase_order = doc.name
        delivery_status.comment = 'Purchase order {} submitted. Status updated to {}.'.format(doc.name, delivery_status.ds_order_status)

        # Append a new status log to the document
        status_log = delivery_status.append('status_logs', {})
        status_log.sales_order = sales_order  # Set the sales_order in the child table
        status_log.previous_status = previous_status  # Add the previous status to the log
        status_log.new_status = 'Supplier Received Order'
        status_log.change_time = nowdate()
        status_log.changed_by = frappe.session.user  # Capture the current user
        status_log.comment = 'Purchase order {} submitted. Status updated to {}.'.format(doc.name, status_log.new_status)

        # Save the changes to DS Order Delivery Status document which also saves the new status log
        delivery_status.save()

        # Print a message
        frappe.msgprint(_("DS Order Status Updated to {0}").format(status_log.new_status))
    else:
        frappe.throw(_("Sales Order not found in Purchase Order items."))


        # add record for supplier confirmation of order

@frappe.whitelist()
def create_supplier_order_confirmation_on_po_submit(doc, method):
    # doc here represents the Purchase Order document
    # retrive purchase order
    # Create a new Supplier Order Confirmation document
    supplier_order_confirmation = frappe.new_doc('Supplier Order Confirmation')

    # Set the purchase order field
    supplier_order_confirmation.purchase_order = doc.name
    supplier_order_confirmation.link = doc.name


    # add comment "Approved the order after approved u will get the invoice"
    supplier_order_confirmation.comment = 'Approved the order after approved you will get the Purchase Invoice'
    #   # Save the document as a draft
    supplier_order_confirmation.save()

    # Print a message
    frappe.msgprint(_("Supplier Order Confirmation document created for Purchase Order {0}").format(doc.name))

# after submit of supplier order confirmation update status in DS Order Delivery Status doc
@frappe.whitelist()
def update_ds_order_status_on_soc_submit(doc, method):
    # doc here represents the Supplier Order Confirmation document

    # Retrieve the Purchase Order from the Supplier Order Confirmation
    purchase_order = doc.purchase_order

    # Retrieve the existing DS Order Delivery Status document
    try:
        delivery_status = frappe.get_doc('DS Order Delivery Status', {'purchase_order': purchase_order})
    except frappe.DoesNotExistError:
        frappe.throw(_("DS Order Delivery Status for Purchase Order {0} not found.").format(purchase_order))

    # Capture the previous status before updating it
    previous_status = delivery_status.ds_order_status

    # Update DS Order Delivery Status based on Supplier Order Confirmation status
    if doc.status == 'Approved':
        delivery_status.ds_order_status = 'Order Processed'
    elif doc.status == 'Cancelled':
        delivery_status.ds_order_status = 'Order cancelled by Supplier'
    elif doc.status == 'Hold':
        delivery_status.ds_order_status = 'Order in hold'

    delivery_status.status_updated_on = nowdate()
    delivery_status.comment = 'Status updated to {} by Supplier against {}.'.format(delivery_status.ds_order_status, doc.name)

    # Append a new status log to the DS Order Delivery Status document
    status_log = delivery_status.append('status_logs', {})
    status_log.purchase_order = purchase_order  # Set the purchase_order in the child table
    status_log.previous_status = previous_status  # Add the previous status to the log
    status_log.new_status = delivery_status.ds_order_status
    status_log.change_time = nowdate()
    status_log.changed_by = frappe.session.user  # Capture the current user
    status_log.comment = 'Status updated to {} by Supplier against {}.'.format(status_log.new_status, doc.name)

    # Save the changes to DS Order Delivery Status document which also saves the new status log
    delivery_status.save()

    # Print a message
    frappe.msgprint(_("DS Order Status Updated to {0}").format(status_log.new_status))
# validation for hold
# def validate(self):
#     if self.status == "Hold" and self.docstatus == 1:
#         frappe.throw(_("Cannot submit Supplier Order Confirmation with status 'Hold'"))

# Purchase Invoice Hoo
@frappe.whitelist()
def update_status_and_log_on_pi_submit(doc, method):
    # doc here represents the Purchase Invoice document

    # Retrieve the name of the purchase order from the first item in the purchase invoice
    purchase_order = doc.items[0].purchase_order if doc.items else None

    # Check if a purchase order was found
    if purchase_order:
        # Retrieve the purchase order document
        purchase_order_doc = frappe.get_doc('Purchase Order', purchase_order)
        
        # Retrieve the name of the sales order from the first item in the purchase order
        sales_order = purchase_order_doc.items[0].sales_order if purchase_order_doc.items else None

        if not sales_order:
            frappe.throw(_("Sales Order not found in Purchase Order items."))
        
        # Retrieve the existing DS Order Delivery Status document
        try:
            delivery_status = frappe.get_doc('DS Order Delivery Status', {'sales_order': sales_order})
        except frappe.DoesNotExistError:
            frappe.throw(_("DS Order Delivery Status for Sales Order {0} not found.").format(sales_order))

        # Capture the previous status before updating it
        previous_status = delivery_status.ds_order_status
        delivery_status.ds_order_status = 'Order Ready for Pickup'
        delivery_status.status_updated_on = nowdate()
        delivery_status.purchase_invoice = doc.name
        delivery_status.comment = 'Purchase invoice {} submitted. Status updated to {}.'.format(doc.name, delivery_status.ds_order_status)

        # Append a new status log to the document
        status_log = delivery_status.append('status_logs', {})
        status_log.sales_order = sales_order  # Set the sales_order in the child table
        status_log.previous_status = previous_status  # Add the previous status to the log
        status_log.new_status = 'Order Ready for Pickup'
        status_log.change_time = nowdate()
        status_log.changed_by = frappe.session.user  # Capture the current user
        status_log.comment = 'Purchase invoice {} submitted. Status updated to {}.'.format(doc.name, status_log.new_status)

        # Save the changes to DS Order Delivery Status document which also saves the new status log
        delivery_status.save()

        # Print a message
        frappe.msgprint(_("DS Order Status Updated to {0}").format(status_log.new_status))
    else:
        frappe.throw(_("Purchase Order not found in Purchase Invoice items."))

# and also create delivery boy status entry for further order status update

# @frappe.whitelist()
# def create_delivery_boy_status_on_pi_submit(doc, method):
#     # Retrieve the name of the purchase order from the first item in the purchase invoice
#     purchase_order = doc.items[0].purchase_order if doc.items else None

#     # Check if a purchase order was found
#     if purchase_order:
#         # Create a new Delivery Boy Status document
#         delivery_boy_status = frappe.new_doc('Delivery Boy Status')

#         # Set the purchase order and purchase invoice fields
#         delivery_boy_status.purchase_order = purchase_order
#         delivery_boy_status.purchase_invoice = doc.name

#         # Save the document as a draft
#         delivery_boy_status.save()

#         # Print a message
#         frappe.msgprint(_("Delivery Boy Status document created for <b>further order updates</b>."))
#     else:
#         frappe.throw(_("Purchase Order not found in Purchase Invoice items."))
import re
import html

@frappe.whitelist()
def create_delivery_boy_status_on_pi_submit(doc, method):
    # Retrieve the name of the purchase order from the first item in the purchase invoice
    purchase_order_name = doc.items[0].purchase_order if doc.items else None

    # Check if a purchase order was found
    if purchase_order_name:
        # Retrieve the purchase order document
        purchase_order = frappe.get_doc('Purchase Order', purchase_order_name)

        # Retrieve the sales order from the first item in the purchase order
        sales_order = purchase_order.items[0].sales_order if purchase_order.items else None

        # Check if a sales order was found
        if not sales_order:
            frappe.throw(_("Sales Order not found in Purchase Order items."))

        # Retrieve the name of the sales invoice from the sales order
        sales_invoice_name = frappe.get_value('Sales Invoice Item', {'sales_order': sales_order}, 'parent')

        # Check if a sales invoice was found
        if not sales_invoice_name:
            frappe.throw(_("Sales Invoice not found for the Sales Order."))

        # Retrieve the sales invoice document
        sales_invoice = frappe.get_doc('Sales Invoice', sales_invoice_name)

        # Check the status of the sales invoice
        order_payment_status = "Paid" if sales_invoice.status == "Paid" else "COD"

        # Fetch the shipping address
        shipping_address = frappe.get_doc('Address', doc.shipping_address)
        delivery_pin_code = shipping_address.pincode

        # Fetch the delivery boy based on pin code
        delivery_boys = frappe.db.sql("""
            SELECT `parent`
            FROM `tabDelivery Boy Area`
            WHERE `pin_code`=%s
        """, (delivery_pin_code,), as_dict=True)

        # Check if a delivery boy was found
        if not delivery_boys:
            frappe.throw(_("No delivery boy found for the pin code."))

        # Retrieve the name of the first delivery boy
        delivery_boy = delivery_boys[0].parent

        # Create a new Delivery Boy Status document
        delivery_boy_status = frappe.new_doc('Delivery Boy Status')

        # Set the purchase order, purchase invoice, sales order, sales invoice, and delivery pin code fields
        delivery_boy_status.purchase_order = purchase_order_name
        delivery_boy_status.purchase_invoice = doc.name
        delivery_boy_status.sales_order = sales_order
        delivery_boy_status.sales_order_display = sales_order
        delivery_boy_status.sales_invoice = sales_invoice_name
        delivery_boy_status.order_payment_status = order_payment_status
        delivery_boy_status.delivery_pin_code = delivery_pin_code
        delivery_boy_status.current_status = 'Order Ready for Pickup'
        delivery_boy_status.update_status = ' '

        # Remove HTML tags from the address fields
        clean_shipping_address = re.sub(r'<.*?>', '', doc.shipping_address_display)
        clean_supplier_address = re.sub(r'<.*?>', '', doc.address_display)

        delivery_boy_status.delivery_address = clean_shipping_address
        delivery_boy_status.supplier_address = clean_supplier_address

        delivery_boy_status.delivery_boy = delivery_boy

        # Save the document as a draft
        delivery_boy_status.save()

        # Print a message
        frappe.msgprint(_("Delivery Boy Status document created for <b>further order updates</b>."))
    else:
        frappe.throw(_("Purchase Order not found in Purchase Invoice items."))

# further order status update by Delivery Boy Status document normaly

# @frappe.whitelist()
# def update_ds_order_delivery_status_on_db_save(doc, method):
#     # doc here represents the Delivery Boy Status document

#     # Retrieve the purchase order
#     purchase_order_doc = frappe.get_doc('Purchase Order', doc.purchase_order)
#     sales_order = purchase_order_doc.items[0].sales_order if purchase_order_doc.items else None

#     # Check if a sales order was found
#     if sales_order:
#         # Retrieve the existing DS Order Delivery Status document
#         delivery_status = frappe.get_doc('DS Order Delivery Status', {'sales_order': sales_order})

#         # Get the latest status update from Delivery Boy Status
#         latest_status_update = doc.ds_db_status_update[-1] if doc.ds_db_status_update else None

#         if latest_status_update:
#             # Capture the previous status before updating it
#             previous_status = delivery_status.ds_order_status

#             # if latest_status_update.status == 'Item Received':
#             #     # Update DS Order Delivery Status
#             #     delivery_status.ds_order_status = 'Item has been picked up by Delivery Boy'

#             # elif latest_status_update.status == 'Out for delivery':
#             #     # Update DS Order Delivery Status
#             #     delivery_status.ds_order_status = 'Item is out for delivery'

#             # elif latest_status_update.status == 'Delivered':
#             #     # Update DS Order Delivery Status
#             #     delivery_status.ds_order_status = 'Item has been delivered'

#             delivery_status.status_updated_on = nowdate()
#             delivery_status.comment = 'Status updated to {} on update of Delivery Boy Status {}.'.format(delivery_status.ds_order_status, doc.name)

#             # Append a new status log to the DS Order Delivery Status document
#             status_log = delivery_status.append('status_logs', {})
#             status_log.sales_order = sales_order  # Set the sales_order in the child table
#             status_log.previous_status = previous_status  # Add the previous status to the log
#             status_log.new_status = delivery_status.ds_order_status
#             status_log.change_time = nowdate()
#             status_log.changed_by = frappe.session.user  # Capture the current user
#             status_log.comment = 'Status updated to {} on update of Delivery Boy Status {}.'.format(status_log.new_status, doc.name)

#             # Save the changes to DS Order Delivery Status document which also saves the new status log
#             delivery_status.save()

#             # Print a message
#             frappe.msgprint(_("DS Order Status Updated to {0}").format(status_log.new_status))
#         else:
#             frappe.throw(_("No status update found in Delivery Boy Status updates."))
#     else:
#         frappe.throw(_("Sales Order not found in Purchase Order items."))

@frappe.whitelist()
def update_ds_order_delivery_status_on_db_save(doc, method):
    # doc here represents the Delivery Boy Status document

    # Retrieve the purchase order
    purchase_order_doc = frappe.get_doc('Purchase Order', doc.purchase_order)
    sales_order = purchase_order_doc.items[0].sales_order if purchase_order_doc.items else None

    # Check if a sales order was found
    if sales_order:
        # Retrieve the existing DS Order Delivery Status document
        delivery_status = frappe.get_doc('DS Order Delivery Status', {'sales_order': sales_order})

        # Get the latest status update from Delivery Boy Status
        latest_status_update = doc.ds_db_status_update[-1] if doc.ds_db_status_update else None

        if latest_status_update:
            # Capture the previous status before updating it
            previous_status = delivery_status.ds_order_status

            if latest_status_update.status == 'Item Received':
                # Update DS Order Delivery Status
                delivery_status.ds_order_status = 'Item has been picked up by Delivery Boy'
                

            elif latest_status_update.status == 'Out for delivery':
                # Update DS Order Delivery Status
                delivery_status.ds_order_status = 'Item is out for delivery'
                

            elif latest_status_update.status == 'Delivered':
                # Update DS Order Delivery Status
                delivery_status.ds_order_status = 'Item has been delivered'
               

            delivery_status.status_updated_on = nowdate()
            delivery_status.comment = 'Status updated to {} on update of Delivery Boy Status {}.'.format(delivery_status.ds_order_status, doc.name)

            # Append a new status log to the DS Order Delivery Status document
            status_log = delivery_status.append('status_logs', {})
            status_log.sales_order = sales_order  # Set the sales_order in the child table
            status_log.previous_status = previous_status  # Add the previous status to the log
            status_log.new_status = delivery_status.ds_order_status
            status_log.change_time = nowdate()
            status_log.changed_by = frappe.session.user  # Capture the current user
            status_log.comment = 'Status updated to {} on update of Delivery Boy Status {}.'.format(status_log.new_status, doc.name)

            # Save the changes to DS Order Delivery Status document which also saves the new status log
            delivery_status.save()

            # Print a message
            frappe.msgprint(_("DS Order Status Updated to {0}").format(status_log.new_status))
        else:
            pass
    else:
        frappe.throw(_("Sales Order not found in Purchase Order items."))


# @frappe.whitelist()
# def update_status_on_payment_submit(doc, method):
#     # doc here represents the Payment Entry document

#     # Retrieve the name of the sales invoice from the Payment Entry
#     sales_invoice = doc.references[0].reference_name if doc.references else None

#     # Check if a sales invoice was found
#     if sales_invoice:
#         # Retrieve the sales invoice document
#         sales_invoice_doc = frappe.get_doc('Sales Invoice', sales_invoice)

#         # Retrieve the name of the sales order from the first item in the sales invoice
#         sales_order = sales_invoice_doc.items[0].sales_order if sales_invoice_doc.items else None

#         if sales_order:
#             # Retrieve the existing DS Order Delivery Status document
#             try:
#                 delivery_status = frappe.get_doc('DS Order Delivery Status', {'sales_order': sales_order})
#             except frappe.DoesNotExistError:
#                 frappe.throw(_("DS Order Delivery Status for Sales Order {0} not found.").format(sales_order))

#             # Capture the previous status before updating it
#             previous_status = delivery_status.ds_order_status

#             # Update the DS Order Delivery Status depending on the status of the sales invoice
#             if sales_invoice_doc.status == "Paid":
#                 delivery_status.ds_order_status = 'Paid'
#                 delivery_status.comment = 'Payment received for sales invoice'
#             else:
#                 delivery_status.ds_order_status = 'POD'
#                 delivery_status.comment = 'Payment on Delivery for sales invoice {}.'.format(sales_invoice)

#             delivery_status.status_updated_on = nowdate()

#             # Append a new status log to the document
#             status_log = delivery_status.append('status_logs', {})
#             status_log.sales_order = sales_order  # Set the sales_order in the child table
#             status_log.previous_status = previous_status  # Add the previous status to the log
#             status_log.new_status = delivery_status.ds_order_status
#             status_log.change_time = nowdate()
#             status_log.changed_by = frappe.session.user  # Capture the current user
#             status_log.comment = delivery_status.comment

#             # Save the changes to DS Order Delivery Status document which also saves the new status log
#             delivery_status.save()

#             # Print a message
#             frappe.msgprint(_("DS Order Status Updated to {0}").format(status_log.new_status))
#         else:
#             frappe.throw(_("Sales Order not found in Sales Invoice items."))
#     else:
#         frappe.throw(_("Sales Invoice not found in Payment Entry references."))

# @frappe.whitelist()
# def update_status_on_payment_entry_submit(doc, method):
#     # Retrieve the Sales Order from the first reference in the Payment Entry
#     sales_order = None
#     for reference in doc.references:
#         if reference.reference_doctype == 'Sales Order':
#             sales_order = reference.reference_name
#             break

#     # Check if a Sales Order was found
#     if sales_order:
#         # Retrieve the existing DS Order Delivery Status document
#         try:
#             delivery_status = frappe.get_doc('DS Order Delivery Status', {'sales_order': sales_order})
#         except frappe.DoesNotExistError:
#             frappe.throw(_("DS Order Delivery Status for Sales Order {0} not found.").format(sales_order))

#         # Capture the previous status before updating it
#         previous_status = delivery_status.ds_order_status

#         # Check the status of the Payment Entry and update DS Order Delivery Status accordingly
#         if doc.docstatus == 1:  # Document is submitted
#             delivery_status.ds_order_status = 'Paid'
#         else:
#             delivery_status.ds_order_status = 'Payment Awaiting'

#         delivery_status.status_updated_on = nowdate()

#         # Append a new status log to the document
#         status_log = delivery_status.append('status_logs', {})
#         status_log.sales_order = sales_order  # Set the sales_order in the child table
#         status_log.previous_status = previous_status  # Add the previous status to the log
#         status_log.new_status = delivery_status.ds_order_status
#         status_log.change_time = nowdate()
#         status_log.changed_by = frappe.session.user  # Capture the current user

#         # Save the changes to DS Order Delivery Status document which also saves the new status log
#         delivery_status.save()

#         # Print a message
#         frappe.msgprint(_("DS Order Status Updated to {0}").format(status_log.new_status))
#     else:
#         frappe.throw(_("Sales Order not found in Payment Entry references."))

@frappe.whitelist()
def update_status_on_payment_entry_submit(doc, method):
    # Check the value of payment_type, return if it's not 'Receive'
    if doc.payment_type != 'Receive':
        return

    # Try to retrieve the Sales Invoice or Sales Order from the Payment Entry references
    sales_invoice = None
    sales_order = None
    for reference in doc.references:
        if reference.reference_doctype == 'Sales Invoice':
            sales_invoice = reference.reference_name
            break
        elif reference.reference_doctype == 'Sales Order':
            sales_order = reference.reference_name
            break

    # Rest of the code...

# @frappe.whitelist()
# def update_status_on_payment_entry_submit(doc, method):
#     # Try to retrieve the Sales Invoice or Sales Order from the Payment Entry references
#     sales_invoice = None
#     sales_order = None
#     for reference in doc.references:
#         if reference.reference_doctype == 'Sales Invoice':
#             sales_invoice = reference.reference_name
#             break
#         elif reference.reference_doctype == 'Sales Order':
#             sales_order = reference.reference_name
#             break

    # Check if a Sales Invoice or Sales Order was found
    if sales_invoice:
        # Get the Sales Invoice document
        sales_invoice_doc = frappe.get_doc('Sales Invoice', sales_invoice)

        # Get the Sales Order from the Sales Invoice
        sales_order = sales_invoice_doc.items[0].sales_order if sales_invoice_doc.items else None

    if sales_order:
        # Retrieve the existing DS Order Delivery Status document
        try:
            delivery_status = frappe.get_doc('DS Order Delivery Status', {'sales_order': sales_order})
        except frappe.DoesNotExistError:
            frappe.throw(_("DS Order Delivery Status for Sales Order {0} not found.").format(sales_order))

        # Capture the previous status before updating it
        previous_status = delivery_status.ds_order_status

        # Check the status of the Payment Entry and update DS Order Delivery Status accordingly
        if doc.docstatus == 1:  # Document is submitted
            delivery_status.ds_order_status = 'Paid'
        else:
            delivery_status.ds_order_status = 'Payment Awaiting'

        delivery_status.status_updated_on = nowdate()

        # Append a new status log to the document
        status_log = delivery_status.append('status_logs', {})
        status_log.sales_order = sales_order  # Set the sales_order in the child table
        status_log.previous_status = previous_status  # Add the previous status to the log
        status_log.new_status = delivery_status.ds_order_status
        status_log.change_time = nowdate()
        status_log.changed_by = frappe.session.user  # Capture the current user

        # Save the changes to DS Order Delivery Status document which also saves the new status log
        delivery_status.save()

        # Print a message
        frappe.msgprint(_("DS Order Status Updated to {0}").format(status_log.new_status))
    else:
        frappe.throw(_("Sales Invoice/Sales Order not found in Payment Entry references."))

# get supplier name in sales order

