import datetime
import json

import frappe
from frappe import _
from frappe.utils.data import get_system_timezone

no_cache = 1


def get_context(context):
	"""Context for booking calendar page"""
	is_enabled = frappe.db.get_single_value("Appointment Booking Settings", "enable_scheduling")
	if is_enabled:
		context.no_cache = 1
		return context
	else:
		frappe.redirect_to_message(
			_("Appointment Scheduling Disabled"),
			_("Appointment Scheduling has been disabled for this site"),
			http_status_code=302,
			indicator_color="red",
		)
		raise frappe.Redirect


@frappe.whitelist(allow_guest=True)
def get_booking_calendar_events(start, end):
	"""Get appointment events for calendar view"""
	if not start or not end:
		return []
	
	appointments = frappe.db.sql("""
		SELECT 
			name, 
			customer_name,
			customer_email,
			scheduled_time,
			status,
			appointment_with,
			party
		FROM `tabAppointment`
		WHERE scheduled_time BETWEEN %(start)s AND %(end)s
		AND status != 'Closed'
		ORDER BY scheduled_time
	""", {
		"start": start,
		"end": end
	}, as_dict=True)
	
	# Format events for FullCalendar
	events = []
	for appointment in appointments:
		# Create title with customer name and status
		title = f"{appointment.customer_name}"
		if appointment.status == "Unverified":
			title += " (Unverified)"
		
		event = {
			"id": appointment.name,
			"title": title,
			"start": appointment.scheduled_time.isoformat() if appointment.scheduled_time else None,
			"backgroundColor": get_event_color(appointment.status),
			"borderColor": get_event_color(appointment.status),
			"extendedProps": {
				"customer_name": appointment.customer_name,
				"customer_email": appointment.customer_email,
				"status": appointment.status,
				"appointment_with": appointment.appointment_with,
				"party": appointment.party,
				"appointment_id": appointment.name
			}
		}
		events.append(event)
	
	return events


@frappe.whitelist(allow_guest=True)
def get_available_slots_for_date(date, timezone="UTC"):
	"""Get available time slots for a specific date"""
	from erpnext.www.book_appointment.index import get_appointment_slots
	
	# Reuse existing appointment slot logic
	return get_appointment_slots(date, timezone)


@frappe.whitelist(allow_guest=True)
def create_appointment_from_calendar(date, time, customer_name, customer_email, customer_phone=None, customer_notes=None, timezone="UTC"):
	"""Create appointment from calendar interface"""
	from erpnext.www.book_appointment.index import create_appointment
	
	contact = {
		"customer_name": customer_name,
		"customer_email": customer_email,
		"customer_phone_number": customer_phone or "",
		"customer_details": customer_notes or ""
	}
	
	return create_appointment(date, time, timezone, contact)


@frappe.whitelist()
def get_appointment_details(appointment_name):
	"""Get detailed information about an appointment"""
	if not frappe.has_permission("Appointment", "read"):
		frappe.throw(_("Not permitted to read appointment details"))
	
	appointment = frappe.get_doc("Appointment", appointment_name)
	
	return {
		"name": appointment.name,
		"customer_name": appointment.customer_name,
		"customer_email": appointment.customer_email,
		"customer_phone_number": appointment.customer_phone_number,
		"customer_details": appointment.customer_details,
		"scheduled_time": appointment.scheduled_time,
		"status": appointment.status,
		"appointment_with": appointment.appointment_with,
		"party": appointment.party,
		"calendar_event": appointment.calendar_event
	}


@frappe.whitelist()
def update_appointment_status(appointment_name, status):
	"""Update appointment status"""
	if not frappe.has_permission("Appointment", "write"):
		frappe.throw(_("Not permitted to update appointment"))
	
	valid_statuses = ["Open", "Unverified", "Closed"]
	if status not in valid_statuses:
		frappe.throw(_("Invalid status. Must be one of: {0}").format(", ".join(valid_statuses)))
	
	appointment = frappe.get_doc("Appointment", appointment_name)
	appointment.status = status
	appointment.save(ignore_permissions=True)
	
	return {"success": True, "message": _("Appointment status updated successfully")}


def get_event_color(status):
	"""Get color for event based on status"""
	color_map = {
		"Open": "#28a745",      # Green
		"Unverified": "#ffc107", # Yellow
		"Closed": "#6c757d"     # Gray
	}
	return color_map.get(status, "#007bff")  # Default blue