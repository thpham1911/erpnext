# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import today, add_days, get_datetime
from erpnext.spa.utils import book_appointment_from_website


def get_context(context):
	"""Get context for spa appointment booking web form"""
	context.no_cache = 1
	context.show_sidebar = True
	
	# Get available spa services for the dropdown
	context.spa_services = frappe.get_all("Spa Service",
		filters={"is_active": 1},
		fields=["name", "service_name", "service_category", "duration_minutes", "base_price"],
		order_by="service_category, service_name"
	)
	
	# Get minimum booking date (tomorrow)
	context.min_date = add_days(today(), 1)
	
	return context


@frappe.whitelist(allow_guest=True)
def submit_appointment_request(data):
	"""Handle appointment request submission from website"""
	try:
		data = frappe.parse_json(data)
		
		# Validate required fields
		required_fields = ['customer_name', 'customer_mobile', 'spa_service', 'appointment_date', 'appointment_time']
		for field in required_fields:
			if not data.get(field):
				return {"success": False, "message": f"{field.replace('_', ' ').title()} is required"}
		
		# Validate appointment date is in future
		appointment_date = data.get('appointment_date')
		if appointment_date <= today():
			return {"success": False, "message": "Please select a future date for your appointment"}
		
		# Check if service exists
		service = frappe.get_doc("Spa Service", data.get('spa_service'))
		if not service.is_active:
			return {"success": False, "message": "Selected service is not available"}
		
		# Prepare customer data
		customer_data = {
			'name': data.get('customer_name'),
			'mobile': data.get('customer_mobile'),
			'email': data.get('customer_email')
		}
		
		# Prepare appointment data
		appointment_data = {
			'service': data.get('spa_service'),
			'date': appointment_date,
			'time': data.get('appointment_time'),
			'notes': data.get('customer_notes', '')
		}
		
		# Book appointment
		result = book_appointment_from_website(customer_data, appointment_data)
		
		if result.get('success'):
			return {
				"success": True,
				"message": "Thank you! Your appointment request has been submitted. We will contact you shortly to confirm your booking.",
				"appointment_id": result.get('appointment_id')
			}
		else:
			return {
				"success": False, 
				"message": result.get('error', 'Failed to book appointment. Please try again.')
			}
			
	except Exception as e:
		frappe.log_error(f"Error in appointment booking: {str(e)}")
		return {
			"success": False,
			"message": "An error occurred while processing your request. Please try again or contact us directly."
		}


@frappe.whitelist(allow_guest=True) 
def get_available_slots(date, service):
	"""Get available time slots for a specific date and service"""
	try:
		from erpnext.spa.doctype.spa_appointment.spa_appointment import get_available_time_slots
		
		slots = get_available_time_slots(date, service)
		return {"success": True, "slots": slots}
		
	except Exception as e:
		frappe.log_error(f"Error getting available slots: {str(e)}")
		return {"success": False, "slots": []}


@frappe.whitelist(allow_guest=True)
def get_service_details(service_name):
	"""Get details of a specific spa service"""
	try:
		service = frappe.get_doc("Spa Service", service_name)
		return {
			"success": True,
			"service": {
				"name": service.name,
				"service_name": service.service_name,
				"service_category": service.service_category,
				"duration_minutes": service.duration_minutes,
				"base_price": service.base_price,
				"description": service.description
			}
		}
		
	except Exception as e:
		return {"success": False, "error": str(e)}