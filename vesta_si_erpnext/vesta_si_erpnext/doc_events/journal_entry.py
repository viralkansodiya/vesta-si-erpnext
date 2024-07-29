import frappe
from frappe.utils import get_link_to_form, comma_and, flt


def check_pi_link(self, method):
    if doc := frappe.db.exists("Purchase Invoice", self.cheque_no):
        frappe.throw(f"Journal Entry is link with purchase invoice {get_link_to_form('Purchase Invoice',doc)}")