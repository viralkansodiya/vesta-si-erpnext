frappe.dashboards.chart_sources["Month Vs Delay"] = {
	method: "vesta_si_erpnext.vesta_si_erpnext.dashboard_chart_source.month_vs_delay.month_vs_delay.get_data",
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company")
		},
        {
            fieldname: "fiscal_year",
			label: __("Fiscal Year"),
			fieldtype: "Link",
			options: "Fiscal Year",
			default: frappe.sys_defaults.fiscal_year
        },
		{
			fieldname : "chart_type",
			label : "Chart Type",
			fieldtype : "Select",
			options : ["Payments On Time", "Payments On Delay"],
			default : "Payments On Time"
		}
	]
};