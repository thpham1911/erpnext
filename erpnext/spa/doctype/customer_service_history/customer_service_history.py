# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import today, get_datetime


class CustomerServiceHistory(Document):
	def autoname(self):
		self.name = make_autoname(self.naming_series)

	def before_insert(self):
		self.created_by = frappe.session.user
		self.created_on = today()

	def validate(self):
		self.update_customer_category()

	def update_customer_category(self):
		"""Update customer category based on service history"""
		if not self.customer:
			return
			
		# Get total completed services for this customer
		total_services = frappe.db.count("Customer Service History", 
			filters={"customer": self.customer})
		
		# Get customer document
		customer = frappe.get_doc("Customer", self.customer)
		
		# Update category based on service count
		if total_services >= 20:
			new_category = "VIP Customer"
		elif total_services >= 5:
			new_category = "Regular Customer"
		else:
			new_category = "New Customer"
		
		# Update customer category if it has changed
		if customer.customer_category != new_category:
			customer.db_set("customer_category", new_category)
			frappe.msgprint(f"Customer {customer.customer_name} has been upgraded to {new_category}")

	def after_insert(self):
		self.update_customer_loyalty_points()

	def update_customer_loyalty_points(self):
		"""Add loyalty points based on service value"""
		if self.price_paid and self.customer:
			# Award 1 point for every 100,000 VND spent
			points = int(self.price_paid / 100000)
			
			if points > 0:
				# Create loyalty point entry
				loyalty_entry = frappe.new_doc("Loyalty Point Entry")
				loyalty_entry.customer = self.customer
				loyalty_entry.loyalty_program = self.get_customer_loyalty_program()
				loyalty_entry.loyalty_points = points
				loyalty_entry.sales_invoice = self.sales_invoice_reference
				loyalty_entry.posting_date = self.service_date
				loyalty_entry.company = frappe.defaults.get_user_default("company")
				loyalty_entry.save(ignore_permissions=True)

	def get_customer_loyalty_program(self):
		"""Get the loyalty program for the customer"""
		customer = frappe.get_doc("Customer", self.customer)
		if customer.loyalty_program:
			return customer.loyalty_program
		
		# Get default spa loyalty program
		spa_program = frappe.db.get_value("Loyalty Program", 
			filters={"is_default": 1, "auto_opt_in": 1}, 
			fieldname="name")
		
		if spa_program:
			customer.db_set("loyalty_program", spa_program)
			return spa_program
		
		return None