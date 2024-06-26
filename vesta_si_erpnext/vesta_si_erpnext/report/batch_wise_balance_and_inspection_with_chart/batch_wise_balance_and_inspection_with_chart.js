// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Batch-Wise Balance and Inspection with Chart"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"item_code",
			"label": __("Item Code"),
			"fieldtype": "Link",
			"options": "Item",
			"get_query": function() {
				return {
					filters: {
						"has_batch_no": 1
					}
				};
			}
		},
		{
			"fieldname":"warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse",
			"get_query": function() {
				let company = frappe.query_report.get_filter_value('company');
				return {
					filters: {
						"company": company
					}
				};
			}
		},
		{
			"fieldname":"qi_parameter",
			"label": __("QI Parameter"),
			"fieldtype": "Link",
			"options": "Quality Inspection Parameter",
			"reqd": 1
		}
	],
	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data['ucl'] > data['qi_parameter'] > data['lcl']){
			if (column.fieldname == "batch"){
				value = value.replace('<a ', '<a style="color: green;" ')
				console.log(value)
			}
		}
		if (data['qi_parameter'] > data['ucl']){
			if (column.fieldname == "batch"){
				value = value.replace('<a ', '<a style="color: red;" ')
				console.log(value)
			}
		}
		if (data['qi_parameter'] < data['lcl']){
			if (column.fieldname == "batch"){
				value = value.replace('<a ', '<a style="color: red;" ')
				console.log(value)
			}
		}
		
		return value
	}
};
