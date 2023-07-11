from . import __version__ as app_version
import dropshifter.dropshifter.api

app_name = "dropshifter"
app_title = "DropShifter"
app_publisher = "MD Faiyaz Ansari"
app_description = "This app will mannaged all Enterprises workflow with supplier or vendor"
app_email = "faiyaz@avtutoring.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/dropshifter/css/dropshifter.css"
# app_include_js = "/assets/dropshifter/js/dropshifter.js"
app_include_js = "/assets/dropshifter/js/custom_sales_order_script.js"
# add one more js
# app_include_js = "/assets/dropshifter/js/website_script.js"
# app_include_js = ["/assets/dropshifter/js/custom_sales_order_script.js", "/assets/dropshifter/js/signup.js"]



# include js, css files in header of web template
# web_include_css = "/assets/dropshifter/css/dropshifter.css"
# web_include_js = "/assets/dropshifter/js/dropshifter.js"




# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "dropshifter/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "/home"
# home_page = "/homepage"
# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]


# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "dropshifter.utils.jinja_methods",
#	"filters": "dropshifter.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "dropshifter.install.before_install"
# after_install = "dropshifter.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "dropshifter.uninstall.before_uninstall"
# after_uninstall = "dropshifter.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "dropshifter.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }
# hooks.py  dropshifter.dropshifter.doctype.custom_script.get_item_supplier
doc_events = {
    # "Sales Order Item": {
    #     "on_update": "dropshifter.dropshifter.doctype.ds_order_delivery_status.ds_order_delivery_status.get_item_supplier"
    # },

    "Sales Order": {
        "on_submit": [
            "dropshifter.dropshifter.doctype.ds_stock_transaction.ds_stock_transaction.create_from_sales_order",
            "dropshifter.dropshifter.doctype.ds_order_delivery_status.ds_order_delivery_status.create_status_and_log"
        ]
    },
    "Sales Invoice": {
        "on_submit": "dropshifter.dropshifter.doctype.ds_order_delivery_status.ds_order_delivery_status.update_status_and_log"   
    },
    # "dropshifter.dropshifter.doctype.ds_order_delivery_status.ds_order_delivery_status.add_entry_to_ds_order_payment_status",
    
    "Payment Entry": {
        "on_submit": "dropshifter.dropshifter.doctype.ds_order_delivery_status.ds_order_delivery_status.update_status_on_payment_entry_submit"
    },
    "Purchase Order": {
        "on_submit": [
            "dropshifter.dropshifter.doctype.ds_order_delivery_status.ds_order_delivery_status.create_supplier_order_confirmation_on_po_submit",
            "dropshifter.dropshifter.doctype.ds_order_delivery_status.ds_order_delivery_status.update_status_and_log_on_po_submit"
        ]
        },
    "Supplier Order Confirmation": {
        "on_submit": "dropshifter.dropshifter.doctype.ds_order_delivery_status.ds_order_delivery_status.update_ds_order_status_on_soc_submit"
        },
    "Purchase Invoice": {
        "on_submit": [
            "dropshifter.dropshifter.doctype.ds_order_delivery_status.ds_order_delivery_status.update_status_and_log_on_pi_submit",
            "dropshifter.dropshifter.doctype.ds_order_delivery_status.ds_order_delivery_status.create_delivery_boy_status_on_pi_submit"
            # "dropshifter.dropshifter.doctype.ds_order_delivery_status.ds_order_delivery_status.get_sales_order_from_purchase_invoice"
        ]
    },
    "Delivery Boy Status": {
        "on_update": "dropshifter.dropshifter.doctype.ds_order_delivery_status.ds_order_delivery_status.update_ds_order_delivery_status_on_db_save",
        "on_submit": "dropshifter.dropshifter.doctype.delivery_boy_status.delivery_boy_status.update_po_status_on_submit"
    },

   "Item": {
        "after_insert": "dropshifter.dropshifter.doctype.ds_stock.ds_stock.create_ds_stock_from_item",
    },
    "DS Stock": {
        "on_update": "dropshifter.dropshifter.doctype.ds_stock.ds_stock.check_uncheck_published",
    },
    "Become a Retailer": {
        "on_submit": "dropshifter.dropshifter.api.approve_retailer",
    }
}



# add fixtures
fixtures = [
    {"doctype": "Print Format", "filters": [["name", "=", "Drop Shipping Sales Invoice"]]},
]
fixtures = ["Customer Group", "Price List"]

fixtures = [
    "Color"
]
# fixtures = [
#     {"dt": "Web Page", "filters": [["name", "=", "homepage"]]},
#     {"dt": "Website Slideshow", "filters": [["name", "=", "homepage"]]},
#     {"dt": "Web Page Block", "filters": [["parent", "=", "homepage"]]}
# ]
fixtures = [
    "Website Theme",
    "Web Page",
    "Website Slideshow",
    # "Web Page Block",
    "System Settings",
    "Website Settings",
    "Custom HTML Block",
    "Role",
    "Portal Settings"





]



# fixtures = [
#     {"dt":"Custom Field", "filters": [
#         ["dt", "=", "Item"],
#         ["fieldname", "=", "ds_maintain_stock"]
#     ]}
# ]

# If you have multiple custom fields for a doctype, and you want to export all of them, you can modify the filter to include just the doctype name:

# fixtures = [
#     {"dt":"Custom Field", "filters": [
#         ["dt", "=", "Item"]
#     ]}
# ]
# Multiple Doctypes

# fixtures = ["Doctype Name 1", "Doctype Name 2"]
# In this case, all records from "Doctype Name 1" and "Doctype Name 2" will be exported.

# Specific Filters

# fixtures = [
#     {"dt":"Doctype Name", "filters": [["fieldname", "operator", "value"]]}
# ]

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"dropshifter.tasks.all"
#	],
#	"daily": [
#		"dropshifter.tasks.daily"
#	],
#	"hourly": [
#		"dropshifter.tasks.hourly"
#	],
#	"weekly": [
#		"dropshifter.tasks.weekly"
#	],
#	"monthly": [
#		"dropshifter.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "dropshifter.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "dropshifter.event.get_events"
# }
# override_whitelisted_methods = {
#     'frappe.core.doctype.user.user.sign_up': 'dropshifter.custom_user.sign_up'
# }

#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "dropshifter.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["dropshifter.utils.before_request"]
# after_request = ["dropshifter.utils.after_request"]

# Job Events
# ----------
# before_job = ["dropshifter.utils.before_job"]
# after_job = ["dropshifter.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"dropshifter.auth.validate"
# ]
