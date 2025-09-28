# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import now, get_datetime, add_to_date, get_time
from datetime import datetime, timedelta


class SpaAppointment(Document):
	def autoname(self):
		self.name = make_autoname(self.naming_series)

	def before_insert(self):
		self.created_by = frappe.session.user
		self.set_final_price()

	def validate(self):
		self.validate_appointment_time()
		self.validate_staff_availability()
		self.set_duration_from_service()
		self.check_customer_category()

	def set_duration_from_service(self):
		if self.spa_service and not self.duration_minutes:
			service = frappe.get_doc("Spa Service", self.spa_service)
			self.duration_minutes = service.duration_minutes

	def validate_appointment_time(self):
		if self.appointment_date and self.appointment_time:
			appointment_datetime = get_datetime(f"{self.appointment_date} {self.appointment_time}")
			if appointment_datetime <= get_datetime(now()):
				frappe.throw("Appointment date and time must be in the future")

	def validate_staff_availability(self):
		if self.assigned_staff and self.appointment_date and self.appointment_time:
			# Check if staff is already booked at this time
			existing_appointments = frappe.get_all("Spa Appointment",
				filters={
					"assigned_staff": self.assigned_staff,
					"appointment_date": self.appointment_date,
					"status": ["in", ["Scheduled", "Confirmed", "In Progress"]],
					"name": ["!=", self.name or ""]
				},
				fields=["appointment_time", "duration_minutes"]
			)
			
			current_start = get_time(self.appointment_time)
			current_end = (datetime.combine(datetime.today(), current_start) + 
						  timedelta(minutes=self.duration_minutes or 60)).time()
			
			for apt in existing_appointments:
				existing_start = get_time(apt.appointment_time)
				existing_end = (datetime.combine(datetime.today(), existing_start) + 
							   timedelta(minutes=apt.duration_minutes or 60)).time()
				
				# Check for time overlap
				if (current_start < existing_end and current_end > existing_start):
					frappe.throw(f"Staff {self.assigned_staff} is already booked during this time")

	def set_final_price(self):
		if self.spa_service and self.customer:
			service = frappe.get_doc("Spa Service", self.spa_service)
			self.final_price = service.get_price_for_customer(self.customer)
			self.discount_amount = (service.base_price or 0) - self.final_price

	def check_customer_category(self):
		if self.customer:
			customer = frappe.get_doc("Customer", self.customer)
			# Check if this is truly a new customer
			existing_appointments = frappe.get_all("Spa Appointment",
				filters={"customer": self.customer, "status": "Completed"},
				limit=1
			)
			self.is_new_customer = 1 if not existing_appointments else 0

	def on_update(self):
		self.update_status_timestamps()
		self.send_notifications_if_needed()

	def update_status_timestamps(self):
		if self.status == "Confirmed" and not self.confirmed_at:
			self.db_set("confirmed_at", now())
		elif self.status == "Completed" and not self.completed_at:
			self.db_set("completed_at", now())
			self.create_service_history()
		elif self.status == "Cancelled" and not self.cancelled_at:
			self.db_set("cancelled_at", now())

	def send_notifications_if_needed(self):
		if self.status == "Confirmed" and not self.sms_sent:
			self.send_confirmation_sms()
		if self.status == "Confirmed" and not self.email_sent:
			self.send_confirmation_email()

	def send_confirmation_sms(self):
		if self.customer_mobile:
			message = f"Your spa appointment on {self.appointment_date} at {self.appointment_time} has been confirmed. Service: {self.service_name}"
			try:
				frappe.sendmail(
					recipients=[self.customer_mobile],
					subject="Appointment Confirmed",
					message=message,
					as_sms=True
				)
				self.db_set("sms_sent", 1)
			except Exception as e:
				frappe.log_error(f"Failed to send SMS: {str(e)}")

	def send_confirmation_email(self):
		if self.customer_email:
			try:
				frappe.sendmail(
					recipients=[self.customer_email],
					subject="Spa Appointment Confirmation",
					template="spa_appointment_confirmation",
					args=self.as_dict()
				)
				self.db_set("email_sent", 1)
			except Exception as e:
				frappe.log_error(f"Failed to send email: {str(e)}")

	def create_service_history(self):
		"""Create service history when appointment is completed"""
		service_history = frappe.new_doc("Customer Service History")
		service_history.customer = self.customer
		service_history.service_date = self.appointment_date
		service_history.spa_service = self.spa_service
		service_history.service_name = self.service_name
		service_history.staff_assigned = self.assigned_staff
		service_history.price_paid = self.final_price
		service_history.appointment_reference = self.name
		service_history.save(ignore_permissions=True)


@frappe.whitelist()
def get_available_time_slots(date, service, staff=None):
	"""Get available time slots for a given date and service"""
	if not date or not service:
		return []
	
	service_doc = frappe.get_doc("Spa Service", service)
	duration = service_doc.duration_minutes or 60
	
	# Get existing appointments for the date
	filters = {
		"appointment_date": date,
		"status": ["in", ["Scheduled", "Confirmed", "In Progress"]]
	}
	
	if staff:
		filters["assigned_staff"] = staff
	
	existing_appointments = frappe.get_all("Spa Appointment",
		filters=filters,
		fields=["appointment_time", "duration_minutes", "assigned_staff"]
	)
	
	# Generate available slots (9 AM to 8 PM, 30-minute intervals)
	start_hour = 9
	end_hour = 20
	interval_minutes = 30
	
	available_slots = []
	
	for hour in range(start_hour, end_hour):
		for minutes in range(0, 60, interval_minutes):
			slot_time = f"{hour:02d}:{minutes:02d}:00"
			slot_datetime = datetime.combine(datetime.today(), get_time(slot_time))
			slot_end = slot_datetime + timedelta(minutes=duration)
			
			# Check if this slot conflicts with existing appointments
			is_available = True
			for apt in existing_appointments:
				apt_start = datetime.combine(datetime.today(), get_time(apt.appointment_time))
				apt_end = apt_start + timedelta(minutes=apt.duration_minutes or 60)
				
				# If staff is specified, only check for that staff
				if staff and apt.assigned_staff != staff:
					continue
				
				if (slot_datetime < apt_end and slot_end > apt_start):
					is_available = False
					break
			
			if is_available and slot_end.time() <= get_time(f"{end_hour}:00:00"):
				available_slots.append(slot_time)
	
	return available_slots