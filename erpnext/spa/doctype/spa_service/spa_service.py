# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class SpaService(Document):
	def autoname(self):
		self.name = make_autoname(self.naming_series)

	def validate(self):
		self.validate_duration()
		self.validate_pricing()

	def validate_duration(self):
		if self.duration_minutes and self.duration_minutes < 15:
			frappe.throw("Service duration must be at least 15 minutes")

	def validate_pricing(self):
		if self.base_price and self.base_price < 0:
			frappe.throw("Base price cannot be negative")
		
		if self.discount_percentage and (self.discount_percentage < 0 or self.discount_percentage > 100):
			frappe.throw("Discount percentage must be between 0 and 100")

	def get_price_for_customer(self, customer=None, date=None):
		"""Get price considering customer category and any applicable discounts"""
		price = self.base_price or 0
		
		if customer:
			customer_doc = frappe.get_doc("Customer", customer)
			
			# VIP customers get 10% discount
			if customer_doc.customer_category == "VIP Customer":
				price = price * 0.9
			# Regular customers get 5% discount
			elif customer_doc.customer_category == "Regular Customer":
				price = price * 0.95
		
		return price