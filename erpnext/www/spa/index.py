import frappe
from frappe import _

no_cache = 1


def get_context(context):
	"""Context for spa management page"""
	context.no_cache = 1
	return context


@frappe.whitelist(allow_guest=True)
def get_spa_services():
	"""Get spa services for display"""
	services = frappe.db.sql("""
		SELECT 
			name, 
			service_name,
			service_category,
			duration_minutes,
			base_price,
			description
		FROM `tabSpa Service`
		ORDER BY service_category, service_name
	""", as_dict=True)
	
	return services


@frappe.whitelist(allow_guest=True)
def get_spa_rooms():
	"""Get spa rooms for display"""
	rooms = frappe.db.sql("""
		SELECT 
			name,
			room_name,
			room_code,
			room_type,
			capacity,
			current_status,
			amenities
		FROM `tabSpa Room`
		ORDER BY room_name
	""", as_dict=True)
	
	return rooms


@frappe.whitelist()
def get_spa_appointments(start=None, end=None):
	"""Get spa appointments for calendar view"""
	conditions = []
	params = {}
	
	if start and end:
		conditions.append("appointment_date BETWEEN %(start)s AND %(end)s")
		params.update({"start": start, "end": end})
	
	where_clause = ""
	if conditions:
		where_clause = "WHERE " + " AND ".join(conditions)
	
	appointments = frappe.db.sql(f"""
		SELECT 
			name,
			customer,
			appointment_date,
			start_time,
			end_time,
			service,
			room,
			status,
			total_amount
		FROM `tabSpa Appointment`
		{where_clause}
		ORDER BY appointment_date, start_time
	""", params, as_dict=True)
	
	return appointments