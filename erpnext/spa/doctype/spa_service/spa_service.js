// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Spa Service', {
	refresh: function(frm) {
		frm.add_custom_button(__('Create Appointment'), function() {
			frappe.new_doc('Appointment', {
				appointment_with: 'Spa Service',
				party: frm.doc.name
			});
		});

		if (frm.doc.is_combo) {
			frm.set_df_property('duration_minutes', 'read_only', 1);
			frm.set_df_property('base_price', 'read_only', 1);
		}
	},

	service_category: function(frm) {
		// Set default duration based on service category
		if (frm.doc.service_category) {
			let default_durations = {
				'Massage': 60,
				'Skincare': 90,
				'Hair Care': 45,
				'Nail Care': 30,
				'Body Treatment': 120,
				'Facial': 75,
				'Combo Package': 180
			};
			
			if (!frm.doc.duration_minutes && default_durations[frm.doc.service_category]) {
				frm.set_value('duration_minutes', default_durations[frm.doc.service_category]);
			}
		}
	},

	is_combo: function(frm) {
		if (frm.doc.is_combo) {
			frm.set_value('service_category', 'Combo Package');
		}
	},

	base_price: function(frm) {
		if (frm.doc.base_price && frm.doc.base_price < 0) {
			frappe.msgprint(__('Base price cannot be negative'));
			frm.set_value('base_price', 0);
		}
	},

	discount_percentage: function(frm) {
		if (frm.doc.discount_percentage) {
			if (frm.doc.discount_percentage < 0 || frm.doc.discount_percentage > 100) {
				frappe.msgprint(__('Discount percentage must be between 0 and 100'));
				frm.set_value('discount_percentage', 0);
			}
		}
	}
});