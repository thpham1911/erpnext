# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import today, add_days, date_diff, getdate


class SpaMembership(Document):
	def autoname(self):
		self.name = make_autoname(self.naming_series)

	def before_insert(self):
		self.created_by = frappe.session.user
		self.created_date = today()
		self.calculate_remaining_sessions()

	def validate(self):
		self.validate_dates()
		self.calculate_remaining_sessions()
		self.update_status_based_on_dates()

	def validate_dates(self):
		if getdate(self.start_date) >= getdate(self.end_date):
			frappe.throw("End date must be after start date")

	def calculate_remaining_sessions(self):
		self.remaining_sessions = (self.total_sessions or 0) - (self.used_sessions or 0)

	def update_status_based_on_dates(self):
		today_date = getdate(today())
		end_date = getdate(self.end_date)
		
		if today_date > end_date and self.status == "Active":
			self.status = "Expired"
		elif today_date <= end_date and self.status == "Expired":
			self.status = "Active"

	def use_session(self, spa_appointment=None):
		"""Deduct one session from membership"""
		if self.status != "Active":
			frappe.throw("Membership is not active")
		
		if self.remaining_sessions <= 0:
			frappe.throw("No remaining sessions in this membership")
		
		self.used_sessions = (self.used_sessions or 0) + 1
		self.remaining_sessions = self.total_sessions - self.used_sessions
		self.last_used_date = today()
		
		# Save the membership
		self.save(ignore_permissions=True)
		
		# Log the usage
		self.log_session_usage(spa_appointment)

	def log_session_usage(self, spa_appointment=None):
		"""Log session usage for tracking"""
		usage_log = frappe.new_doc("Spa Membership Usage")
		usage_log.membership = self.name
		usage_log.customer = self.customer
		usage_log.usage_date = today()
		usage_log.sessions_used = 1
		
		if spa_appointment:
			usage_log.spa_appointment = spa_appointment
			appointment_doc = frappe.get_doc("Spa Appointment", spa_appointment)
			usage_log.spa_service = appointment_doc.spa_service
			usage_log.staff_assigned = appointment_doc.assigned_staff
			
		usage_log.save(ignore_permissions=True)

	def get_membership_discount(self):
		"""Get discount percentage based on membership type"""
		discount_map = {
			"Basic": 5,
			"Silver": 10,
			"Gold": 15,
			"Platinum": 20,
			"VIP": 25,
			"Couple": 15,
			"Family": 20
		}
		return discount_map.get(self.membership_type, 0)

	def is_priority_customer(self):
		"""Check if customer has priority booking privileges"""
		return self.priority_booking or self.membership_type in ["Platinum", "VIP"]

	def check_renewal_needed(self):
		"""Check if membership needs renewal reminder"""
		days_to_expiry = date_diff(self.end_date, today())
		
		# Send reminder 30 days before expiry
		if days_to_expiry <= 30 and not self.renewal_reminder_sent:
			self.send_renewal_reminder()
			self.db_set("renewal_reminder_sent", 1)

	def send_renewal_reminder(self):
		"""Send renewal reminder to customer"""
		try:
			customer_doc = frappe.get_doc("Customer", self.customer)
			
			# Send SMS if mobile number available
			if customer_doc.mobile_no:
				message = f"Your {self.membership_type} membership expires on {self.end_date}. Contact us to renew!"
				frappe.sendmail(
					recipients=[customer_doc.mobile_no],
					message=message,
					as_sms=True,
					subject="Membership Renewal Reminder"
				)
			
			# Send email if email available
			if customer_doc.email_id:
				frappe.sendmail(
					recipients=[customer_doc.email_id],
					subject="Spa Membership Renewal Reminder",
					template="spa_membership_renewal",
					args=self.as_dict()
				)
				
		except Exception as e:
			frappe.log_error(f"Failed to send renewal reminder: {str(e)}")

@frappe.whitelist()
def get_customer_active_membership(customer):
	"""Get customer's active membership"""
	membership = frappe.get_all("Spa Membership",
		filters={
			"customer": customer,
			"status": "Active",
			"end_date": [">=", today()]
		},
		fields=["*"],
		order_by="creation desc",
		limit=1
	)
	
	return membership[0] if membership else None

@frappe.whitelist()
def check_membership_benefits(customer, spa_service):
	"""Check what benefits customer gets for a service"""
	membership = get_customer_active_membership(customer)
	
	if not membership:
		return {"has_membership": False}
	
	membership_doc = frappe.get_doc("Spa Membership", membership["name"])
	
	return {
		"has_membership": True,
		"membership_type": membership_doc.membership_type,
		"discount_percentage": membership_doc.get_membership_discount(),
		"remaining_sessions": membership_doc.remaining_sessions,
		"priority_booking": membership_doc.is_priority_customer(),
		"membership_id": membership_doc.name
	}