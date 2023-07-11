from frappe.core.doctype.user.user import sign_up as original_sign_up
import frappe


@frappe.whitelist(allow_guest=True)
def sign_up(email, full_name, mobile_no=None):
    # Call the original sign up function
    original_sign_up(email, full_name)

    # Set the mobile_no field
    if mobile_no:
        user = frappe.get_doc("User", email)
        user.mobile_no = mobile_no
        user.save()
