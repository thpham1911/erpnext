# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today, add_days, get_datetime
from datetime import datetime


def send_birthday_reminders():
	"""Send birthday reminders to customers"""
	try:
		# Get customers whose birthday is today and have birthday reminder enabled
		customers = frappe.db.sql("""
			SELECT name, customer_name, mobile_no, email_id, date_of_birth 
			FROM `tabCustomer` 
			WHERE birthday_reminder = 1 
			AND date_of_birth IS NOT NULL 
			AND DAY(date_of_birth) = DAY(CURDATE()) 
			AND MONTH(date_of_birth) = MONTH(CURDATE())
		""", as_dict=True)
		
		for customer in customers:
			send_birthday_message(customer)
			
	except Exception as e:
		frappe.log_error(f"Error in birthday reminders: {str(e)}")


def send_birthday_message(customer):
	"""Send birthday message to individual customer"""
	try:
		message = f"Happy Birthday {customer.customer_name}! 🎉 Enjoy a special 20% discount on all spa services this month. Call us to book your celebration!"
		
		# Send SMS if mobile number exists
		if customer.mobile_no:
			frappe.sendmail(
				recipients=[customer.mobile_no],
				message=message,
				subject="Happy Birthday!",
				as_sms=True
			)
		
		# Send email if email exists
		if customer.email_id:
			frappe.sendmail(
				recipients=[customer.email_id],
				subject="Happy Birthday from Our Spa!",
				template="birthday_greeting",
				args=customer
			)
			
	except Exception as e:
		frappe.log_error(f"Error sending birthday message to {customer.name}: {str(e)}")


def send_appointment_reminders():
	"""Send appointment reminders for tomorrow's appointments"""
	try:
		tomorrow = add_days(today(), 1)
		
		appointments = frappe.get_all("Spa Appointment",
			filters={
				"appointment_date": tomorrow,
				"status": ["in", ["Scheduled", "Confirmed"]],
				"reminder_sent": 0
			},
			fields=["*"]
		)
		
		for appointment in appointments:
			send_appointment_reminder(appointment)
			
	except Exception as e:
		frappe.log_error(f"Error in appointment reminders: {str(e)}")


def send_appointment_reminder(appointment):
	"""Send reminder for individual appointment"""
	try:
		message = f"Reminder: You have a spa appointment tomorrow at {appointment['appointment_time']} for {appointment['service_name']}. See you soon!"
		
		# Send SMS if mobile number exists
		if appointment.get('customer_mobile'):
			frappe.sendmail(
				recipients=[appointment['customer_mobile']],
				message=message,
				subject="Appointment Reminder",
				as_sms=True
			)
		
		# Send email if email exists  
		if appointment.get('customer_email'):
			frappe.sendmail(
				recipients=[appointment['customer_email']],
				subject="Spa Appointment Reminder",
				template="appointment_reminder",
				args=appointment
			)
		
		# Mark reminder as sent
		frappe.db.set_value("Spa Appointment", appointment['name'], "reminder_sent", 1)
		
	except Exception as e:
		frappe.log_error(f"Error sending appointment reminder for {appointment['name']}: {str(e)}")


def check_membership_renewals():
	"""Check and send membership renewal reminders"""
	try:
		# Get memberships expiring in 30 days
		expiring_memberships = frappe.db.sql("""
			SELECT * FROM `tabSpa Membership`
			WHERE status = 'Active'
			AND renewal_reminder_sent = 0
			AND DATEDIFF(end_date, CURDATE()) <= 30
			AND DATEDIFF(end_date, CURDATE()) > 0
		""", as_dict=True)
		
		for membership in expiring_memberships:
			send_renewal_reminder(membership)
			
	except Exception as e:
		frappe.log_error(f"Error checking membership renewals: {str(e)}")


def send_renewal_reminder(membership):
	"""Send renewal reminder for membership"""
	try:
		customer = frappe.get_doc("Customer", membership['customer'])
		
		message = f"Your {membership['membership_type']} membership expires on {membership['end_date']}. Renew now to continue enjoying exclusive benefits!"
		
		# Send SMS if mobile number exists
		if customer.mobile_no:
			frappe.sendmail(
				recipients=[customer.mobile_no],
				message=message,
				subject="Membership Renewal",
				as_sms=True
			)
		
		# Send email if email exists
		if customer.email_id:
			frappe.sendmail(
				recipients=[customer.email_id],
				subject="Membership Renewal Reminder",
				template="membership_renewal",
				args=membership
			)
		
		# Mark reminder as sent
		frappe.db.set_value("Spa Membership", membership['name'], "renewal_reminder_sent", 1)
		
	except Exception as e:
		frappe.log_error(f"Error sending renewal reminder for {membership['name']}: {str(e)}")


@frappe.whitelist()
def get_spa_dashboard_data():
	"""Get data for spa management dashboard"""
	try:
		today_appointments = frappe.db.count("Spa Appointment", {
			"appointment_date": today(),
			"status": ["not in", ["Cancelled", "No Show"]]
		})
		
		monthly_revenue = frappe.db.sql("""
			SELECT COALESCE(SUM(final_price), 0) as revenue
			FROM `tabSpa Appointment`
			WHERE MONTH(appointment_date) = MONTH(CURDATE())
			AND YEAR(appointment_date) = YEAR(CURDATE())
			AND status = 'Completed'
		""", as_dict=True)[0]['revenue']
		
		active_memberships = frappe.db.count("Spa Membership", {
			"status": "Active",
			"end_date": [">=", today()]
		})
		
		available_rooms = frappe.db.count("Spa Room", {
			"is_active": 1,
			"current_status": "Available"
		})
		
		return {
			"today_appointments": today_appointments,
			"monthly_revenue": monthly_revenue,
			"active_memberships": active_memberships,
			"available_rooms": available_rooms
		}
		
	except Exception as e:
		frappe.log_error(f"Error getting dashboard data: {str(e)}")
		return {}


@frappe.whitelist()
def book_appointment_from_website(customer_data, appointment_data):
	"""Book appointment from website form"""
	try:
		# Create or get customer
		if customer_data.get('email'):
			customer = frappe.db.get_value("Customer", 
				{"email_id": customer_data['email']}, "name")
		else:
			customer = None
			
		if not customer:
			# Create new customer
			customer_doc = frappe.new_doc("Customer")
			customer_doc.customer_name = customer_data['name']
			customer_doc.customer_type = "Individual"
			customer_doc.customer_category = "New Customer"
			
			if customer_data.get('mobile'):
				# Create contact with mobile number
				from erpnext.selling.doctype.customer.customer import make_contact
				contact = make_contact({
					"doctype": "Customer",
					"name": customer_doc.name,
					"customer_name": customer_data['name'],
					"mobile_no": customer_data['mobile'],
					"email_id": customer_data.get('email'),
					"customer_type": "Individual"
				})
				customer_doc.customer_primary_contact = contact.name
				
			customer_doc.save(ignore_permissions=True)
			customer = customer_doc.name
		
		# Create appointment
		appointment = frappe.new_doc("Spa Appointment")
		appointment.customer = customer
		appointment.spa_service = appointment_data['service']
		appointment.appointment_date = appointment_data['date']
		appointment.appointment_time = appointment_data['time']
		appointment.customer_notes = appointment_data.get('notes', '')
		appointment.status = "Scheduled"
		appointment.confirmation_required = 1
		
		appointment.save(ignore_permissions=True)
		
		# Send confirmation
		send_appointment_confirmation(appointment.name)
		
		return {"success": True, "appointment_id": appointment.name}
		
	except Exception as e:
		frappe.log_error(f"Error booking appointment from website: {str(e)}")
		return {"success": False, "error": str(e)}


def send_appointment_confirmation(appointment_name):
	"""Send confirmation for newly booked appointment"""
	try:
		appointment = frappe.get_doc("Spa Appointment", appointment_name)
		appointment.send_confirmation_sms()
		appointment.send_confirmation_email()
		
	except Exception as e:
		frappe.log_error(f"Error sending appointment confirmation: {str(e)}")


def update_room_status():
	"""Update room status based on current appointments"""
	try:
		current_time = get_datetime()
		
		# Get all active appointments happening now
		active_appointments = frappe.get_all("Spa Appointment",
			filters={
				"appointment_date": current_time.date(),
				"status": "In Progress"
			},
			fields=["room_assigned", "appointment_time", "duration_minutes"]
		)
		
		# Mark rooms as occupied for active appointments
		occupied_rooms = []
		for apt in active_appointments:
			if apt.room_assigned:
				apt_start = get_datetime(f"{current_time.date()} {apt.appointment_time}")
				apt_end = apt_start + frappe.utils.timedelta(minutes=apt.duration_minutes or 60)
				
				if apt_start <= current_time <= apt_end:
					occupied_rooms.append(apt.room_assigned)
					frappe.db.set_value("Spa Room", apt.room_assigned, "current_status", "Occupied")
		
		# Mark other rooms as available (if not in maintenance)
		all_rooms = frappe.get_all("Spa Room", 
			filters={"is_active": 1}, 
			fields=["name", "current_status"]
		)
		
		for room in all_rooms:
			if (room.name not in occupied_rooms and 
				room.current_status not in ["Maintenance", "Out of Order"]):
				frappe.db.set_value("Spa Room", room.name, "current_status", "Available")
		
		frappe.db.commit()
		
	except Exception as e:
		frappe.log_error(f"Error updating room status: {str(e)}")