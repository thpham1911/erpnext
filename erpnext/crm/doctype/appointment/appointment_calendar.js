// Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.views.calendar["Appointment"] = {
	field_map: {
		start: "scheduled_time",
		end: "scheduled_time",
		id: "name",
		title: "customer_name",
		allDay: "allDay",
		status: "status",
	},
	filters: [
		{
			fieldtype: "Select",
			fieldname: "status",
			options: ["", "Open", "Unverified", "Closed"],
			label: __("Status"),
		},
		{
			fieldtype: "Link",
			fieldname: "appointment_with",
			options: "DocType",
			label: __("Appointment With"),
		},
	],
	get_events_method: "erpnext.crm.doctype.appointment.appointment.get_events",
	get_css_class: function (data) {
		if (data.status === "Open") {
			return "success";
		} else if (data.status === "Unverified") {
			return "warning";
		} else if (data.status === "Closed") {
			return "info";
		} else {
			return "default";
		}
	},
};