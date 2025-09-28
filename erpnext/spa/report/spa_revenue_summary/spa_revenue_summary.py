# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"label": _("Service Name"),
			"fieldname": "service_name", 
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("Category"),
			"fieldname": "service_category",
			"fieldtype": "Data", 
			"width": 150
		},
		{
			"label": _("Total Appointments"),
			"fieldname": "total_appointments",
			"fieldtype": "Int",
			"width": 120
		},
		{
			"label": _("Completed"),
			"fieldname": "completed_appointments", 
			"fieldtype": "Int",
			"width": 120
		},
		{
			"label": _("Total Revenue"),
			"fieldname": "total_revenue",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("Average Price"),
			"fieldname": "average_price",
			"fieldtype": "Currency", 
			"width": 120
		},
		{
			"label": _("Completion Rate %"),
			"fieldname": "completion_rate",
			"fieldtype": "Percent",
			"width": 120
		}
	]


def get_data(filters):
	conditions = get_conditions(filters)
	
	data = frappe.db.sql(f"""
		SELECT 
			ss.service_name,
			ss.service_category,
			COUNT(sa.name) as total_appointments,
			SUM(CASE WHEN sa.status = 'Completed' THEN 1 ELSE 0 END) as completed_appointments,
			SUM(CASE WHEN sa.status = 'Completed' THEN sa.final_price ELSE 0 END) as total_revenue,
			AVG(CASE WHEN sa.status = 'Completed' THEN sa.final_price ELSE NULL END) as average_price,
			(SUM(CASE WHEN sa.status = 'Completed' THEN 1 ELSE 0 END) * 100.0 / COUNT(sa.name)) as completion_rate
		FROM `tabSpa Service` ss
		LEFT JOIN `tabSpa Appointment` sa ON ss.name = sa.spa_service {conditions}
		GROUP BY ss.name, ss.service_name, ss.service_category
		HAVING total_appointments > 0
		ORDER BY total_revenue DESC
	""", as_dict=True)
	
	return data


def get_conditions(filters):
	conditions = []
	
	if filters.get("from_date"):
		conditions.append(f"AND sa.appointment_date >= '{filters.get('from_date')}'")
	
	if filters.get("to_date"):
		conditions.append(f"AND sa.appointment_date <= '{filters.get('to_date')}'")
		
	if filters.get("service_category"):
		conditions.append(f"AND ss.service_category = '{filters.get('service_category')}'")
	
	return " ".join(conditions) if conditions else ""