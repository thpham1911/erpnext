// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Spa Appointment', {
	refresh: function(frm) {
		frm.add_custom_button(__('Confirm Appointment'), function() {
			frm.set_value('status', 'Confirmed');
			frm.save();
		}).addClass('btn-primary');

		frm.add_custom_button(__('Start Service'), function() {
			frm.set_value('status', 'In Progress');
			frm.save();
		});

		frm.add_custom_button(__('Complete Service'), function() {
			frm.set_value('status', 'Completed');
			frm.save();
		});

		frm.add_custom_button(__('Cancel Appointment'), function() {
			frappe.confirm(__('Are you sure you want to cancel this appointment?'), function() {
				frm.set_value('status', 'Cancelled');
				frm.save();
			});
		});

		frm.add_custom_button(__('Send SMS Reminder'), function() {
			frappe.call({
				method: 'erpnext.spa.doctype.spa_appointment.spa_appointment.send_appointment_reminder',
				args: {
					appointment: frm.doc.name
				},
				callback: function(r) {
					if (r.message) {
						frappe.msgprint(__('SMS reminder sent successfully'));
					}
				}
			});
		});

		// Show available time slots
		if (frm.doc.appointment_date && frm.doc.spa_service) {
			frm.add_custom_button(__('Show Available Slots'), function() {
				show_available_slots(frm);
			});
		}
	},

	spa_service: function(frm) {
		if (frm.doc.spa_service) {
			frappe.db.get_doc('Spa Service', frm.doc.spa_service).then(service => {
				frm.set_value('duration_minutes', service.duration_minutes);
				frm.set_value('base_price', service.base_price);
				
				// Calculate final price based on customer category
				if (frm.doc.customer) {
					calculate_final_price(frm);
				}
			});
		}
	},

	customer: function(frm) {
		if (frm.doc.customer && frm.doc.spa_service) {
			calculate_final_price(frm);
		}
	},

	appointment_date: function(frm) {
		if (frm.doc.appointment_date && frm.doc.spa_service) {
			// Show available slots button
			frm.page.add_action_item(__('Show Available Slots'), function() {
				show_available_slots(frm);
			});
		}
	},

	status: function(frm) {
		// Update status-specific fields
		if (frm.doc.status === 'Completed' && !frm.doc.completed_at) {
			frm.set_value('completed_at', frappe.datetime.now_datetime());
		} else if (frm.doc.status === 'Cancelled' && !frm.doc.cancelled_at) {
			frm.set_value('cancelled_at', frappe.datetime.now_datetime());
		} else if (frm.doc.status === 'Confirmed' && !frm.doc.confirmed_at) {
			frm.set_value('confirmed_at', frappe.datetime.now_datetime());
		}
	}
});

function calculate_final_price(frm) {
	if (frm.doc.customer && frm.doc.spa_service) {
		frappe.call({
			method: 'erpnext.spa.doctype.spa_service.spa_service.get_price_for_customer',
			args: {
				service: frm.doc.spa_service,
				customer: frm.doc.customer
			},
			callback: function(r) {
				if (r.message) {
					frm.set_value('final_price', r.message);
					frm.set_value('discount_amount', (frm.doc.base_price || 0) - r.message);
				}
			}
		});
	}
}

function show_available_slots(frm) {
	frappe.call({
		method: 'erpnext.spa.doctype.spa_appointment.spa_appointment.get_available_time_slots',
		args: {
			date: frm.doc.appointment_date,
			service: frm.doc.spa_service,
			staff: frm.doc.assigned_staff
		},
		callback: function(r) {
			if (r.message && r.message.length > 0) {
				let slots_html = '<div class="row">';
				r.message.forEach(function(slot, index) {
					if (index % 4 === 0 && index > 0) {
						slots_html += '</div><div class="row">';
					}
					slots_html += `<div class="col-sm-3">
						<button class="btn btn-default btn-sm btn-block time-slot-btn" 
								data-time="${slot}" style="margin-bottom: 5px;">
							${slot}
						</button>
					</div>`;
				});
				slots_html += '</div>';

				let dialog = new frappe.ui.Dialog({
					title: __('Available Time Slots'),
					fields: [
						{
							fieldtype: 'HTML',
							fieldname: 'slots_html',
							options: slots_html
						}
					]
				});

				dialog.show();

				// Add click handlers for time slots
				dialog.$wrapper.find('.time-slot-btn').on('click', function() {
					let selected_time = $(this).data('time');
					frm.set_value('appointment_time', selected_time);
					dialog.hide();
				});
			} else {
				frappe.msgprint(__('No available time slots for this date and service.'));
			}
		}
	});
}