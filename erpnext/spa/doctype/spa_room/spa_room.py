# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_days, today, get_datetime, now


class SpaRoom(Document):
	def validate(self):
		self.update_maintenance_schedule()

	def update_maintenance_schedule(self):
		if not self.next_maintenance and self.maintenance_frequency_days:
			self.next_maintenance = add_days(today(), self.maintenance_frequency_days)

	def is_available(self, start_datetime, end_datetime):
		"""Check if room is available for the given time period"""
		if not self.is_active or self.current_status != "Available":
			return False
		
		# Check for existing bookings
		existing_bookings = frappe.get_all("Spa Appointment",
			filters={
				"room_assigned": self.name,
				"appointment_date": start_datetime.date(),
				"status": ["in", ["Scheduled", "Confirmed", "In Progress"]]
			},
			fields=["appointment_time", "duration_minutes"]
		)
		
		for booking in existing_bookings:
			booking_start = get_datetime(f"{start_datetime.date()} {booking.appointment_time}")
			booking_end = booking_start + frappe.utils.timedelta(minutes=booking.duration_minutes or 60)
			
			# Add cleaning time buffer
			booking_end = booking_end + frappe.utils.timedelta(minutes=self.cleaning_time_minutes or 30)
			
			# Check for overlap
			if (start_datetime < booking_end and end_datetime > booking_start):
				return False
		
		return True

	def mark_as_occupied(self):
		"""Mark room as occupied"""
		self.db_set("current_status", "Occupied")

	def mark_as_cleaning(self):
		"""Mark room as cleaning"""
		self.db_set("current_status", "Cleaning")

	def mark_as_available(self):
		"""Mark room as available and update last cleaned"""
		self.db_set("current_status", "Available")
		self.db_set("last_cleaned", now())

	def mark_for_maintenance(self):
		"""Mark room for maintenance"""
		self.db_set("current_status", "Maintenance")

@frappe.whitelist()
def get_available_rooms(date, start_time, duration_minutes, room_type=None):
	"""Get available rooms for a specific date and time"""
	if not date or not start_time or not duration_minutes:
		return []
	
	# Build filters
	filters = {
		"is_active": 1,
		"current_status": "Available"
	}
	
	if room_type:
		filters["room_type"] = room_type
	
	# Get all potentially available rooms
	rooms = frappe.get_all("Spa Room", filters=filters, 
		fields=["name", "room_name", "room_type", "capacity", "cleaning_time_minutes"])
	
	available_rooms = []
	start_datetime = get_datetime(f"{date} {start_time}")
	end_datetime = start_datetime + frappe.utils.timedelta(minutes=int(duration_minutes))
	
	for room in rooms:
		room_doc = frappe.get_doc("Spa Room", room.name)
		if room_doc.is_available(start_datetime, end_datetime):
			available_rooms.append(room)
	
	return available_rooms