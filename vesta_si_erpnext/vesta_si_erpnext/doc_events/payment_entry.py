import frappe
from erpnext.accounts.doctype.payment_entry.payment_entry import get_negative_outstanding_invoices
from frappe.utils import get_link_to_form, comma_and, flt
from frappe.utils import (
	add_days,
	add_months,
	cint,
	comma_and,
	flt,
	fmt_money,
	formatdate,
	get_last_day,
	get_link_to_form,
	getdate,
	nowdate,
	today,
)

def validate(self, method):
    
    currency_list = []    
    if self.party_type == "Supplier":
        for row in self.references:
            currency_list.append(frappe.db.get_value(row.reference_doctype , row.reference_name , 'currency'))

        if len(list(set(currency_list))) > 1:
            frappe.throw("Purchase Invoices have different currencies. All selected purchase invoices must have the same currency.")
        elif list(set(currency_list)) and self.paid_from_account_currency != list(set(currency_list))[0]:
            frappe.throw(f"Account Paid From should be in <b>{list(set(currency_list))[0]}<b>")
        party_account_currency = frappe.db.get_value("Account", self.paid_to, 'account_currency')
        
        company_currency = frappe.db.get_value("Company", self.company, 'default_currency')
        
        # if self.payment_type == "Pay" and self.party_type == "Supplier":
        #     data = get_negative_outstanding_invoices(
        #             "Supplier", 
        #             self.party, 
        #             self.paid_to, 
        #             party_account_currency, 
        #             company_currency,
        #             condition = '')
        #     if len(data):
        #         for row in data:
        #             message = "Debit Note and Payment Entry available against this supplier {0}<br>".format(get_link_to_form(self.party_type, self.party))
        #             message +="First reconcile those entry, reference available as mentioned below"
        #             message += "<br><br>"
        #             message += """<table width='100%'>"""
        #             for row in data:
        #                 message += "<tr><td>{0}</td><td>{1} {2}</td></tr>".format(get_link_to_form(row.voucher_type, row.voucher_no),self.paid_to_account_currency, row.outstanding_amount)
        #             message += "</table>"
        #             frappe.throw(message)
        # if len(self.references):
        #     if self.references[0].reference_doctype == "Purchase Invoice":
        #         doc = frappe.get_doc("Purchase Invoice", self.references[0].reference_name)
        #         get_advance_entries(doc)

def get_advance_entries(self):
	res = self.get_advance_entries(
			include_unallocated=not cint(self.get("only_include_allocated_payments"))
		)
	if res and not self.allocate_advances_automatically:
		if not len(self.advances):
			frappe.throw("Advance payments available against supplier <b>{0}</b> <br> Enable <b>'Set Advances and Allocate (FIFO)'</b> or click on the <b>'Get Advances Paid'</b> button under the payments section.".format(self.supplier))

def on_submit(self, method):
    if not (self.custom_is_manual_payment_process and self.custom_xml_file_generated):
        frappe.throw("XML file is not generated for this payment entry <b>{0}</b>.".format(self.name))
    data =  frappe.db.sql(f'''
            Select parent From `tabPayment Transaction Log` 
            Where payment_entry = "{self.name}"
        ''', as_dict =1)
    if len(data):
        pel_doc = frappe.get_doc('Payment Export Log', data[0].parent)
        for row in pel_doc.logs:
            if row.payment_entry == self.name:
                frappe.db.set_value(row.doctype , row.name, 'status', 'Submitted')