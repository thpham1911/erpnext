# Example Code Snippets - Booking Calendar Integration

## Frontend Integration Examples

### 1. Embedding Booking Calendar in Custom Page

```html
<!-- custom_page.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Our Booking System</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/fullcalendar@6.1.8/index.global.min.css">
    <script src="https://cdn.jsdelivr.net/npm/fullcalendar@6.1.8/index.global.min.js"></script>
</head>
<body>
    <div id="custom-calendar"></div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            var calendarEl = document.getElementById('custom-calendar');
            var calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: 'dayGridMonth',
                events: '/api/method/erpnext.www.booking_calendar.index.get_booking_calendar_events',
                dateClick: function(info) {
                    bookAppointment(info.dateStr);
                }
            });
            calendar.render();
        });
        
        function bookAppointment(date) {
            // Custom booking logic
            window.location.href = `/booking_calendar?date=${date}`;
        }
    </script>
</body>
</html>
```

### 2. React Component Integration

```jsx
// BookingCalendar.jsx
import React, { useState, useEffect } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';

const BookingCalendar = () => {
    const [events, setEvents] = useState([]);
    
    useEffect(() => {
        fetchEvents();
    }, []);
    
    const fetchEvents = async () => {
        try {
            const response = await fetch('/api/method/erpnext.www.booking_calendar.index.get_booking_calendar_events', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    start: '2024-01-01T00:00:00Z',
                    end: '2024-12-31T23:59:59Z'
                })
            });
            const data = await response.json();
            setEvents(data.message);
        } catch (error) {
            console.error('Error fetching events:', error);
        }
    };
    
    const handleDateSelect = async (selectInfo) => {
        const title = prompt('Enter customer name:');
        const email = prompt('Enter customer email:');
        
        if (title && email) {
            try {
                const response = await fetch('/api/method/erpnext.www.booking_calendar.index.create_appointment_from_calendar', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        date: selectInfo.startStr.split('T')[0],
                        time: selectInfo.startStr.split('T')[1].substring(0, 5),
                        customer_name: title,
                        customer_email: email
                    })
                });
                
                if (response.ok) {
                    fetchEvents(); // Refresh events
                }
            } catch (error) {
                console.error('Error creating appointment:', error);
            }
        }
    };
    
    return (
        <div className="booking-calendar">
            <FullCalendar
                plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
                headerToolbar={{
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek'
                }}
                initialView="dayGridMonth"
                events={events}
                selectable={true}
                select={handleDateSelect}
                eventClick={(info) => {
                    alert(`Appointment: ${info.event.title}\nEmail: ${info.event.extendedProps.customer_email}`);
                }}
            />
        </div>
    );
};

export default BookingCalendar;
```

### 3. Vue.js Component

```vue
<!-- BookingCalendar.vue -->
<template>
    <div class="booking-calendar">
        <FullCalendar
            :options="calendarOptions"
        />
        
        <!-- Booking Modal -->
        <div v-if="showBookingModal" class="modal-overlay" @click="closeModal">
            <div class="modal-content" @click.stop>
                <h3>Book Appointment</h3>
                <form @submit.prevent="submitBooking">
                    <div class="form-group">
                        <label>Date & Time:</label>
                        <input v-model="booking.datetime" type="datetime-local" required />
                    </div>
                    <div class="form-group">
                        <label>Name:</label>
                        <input v-model="booking.name" type="text" required />
                    </div>
                    <div class="form-group">
                        <label>Email:</label>
                        <input v-model="booking.email" type="email" required />
                    </div>
                    <div class="form-group">
                        <label>Phone:</label>
                        <input v-model="booking.phone" type="tel" />
                    </div>
                    <div class="form-actions">
                        <button type="button" @click="closeModal">Cancel</button>
                        <button type="submit">Book Appointment</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'

export default {
    name: 'BookingCalendar',
    components: {
        FullCalendar
    },
    data() {
        return {
            showBookingModal: false,
            booking: {
                datetime: '',
                name: '',
                email: '',
                phone: ''
            },
            calendarOptions: {
                plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek'
                },
                initialView: 'dayGridMonth',
                events: this.fetchEvents,
                selectable: true,
                select: this.handleDateSelect,
                eventClick: this.handleEventClick
            }
        }
    },
    methods: {
        async fetchEvents(fetchInfo) {
            try {
                const response = await fetch('/api/method/erpnext.www.booking_calendar.index.get_booking_calendar_events', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        start: fetchInfo.start.toISOString(),
                        end: fetchInfo.end.toISOString()
                    })
                });
                const data = await response.json();
                return data.message;
            } catch (error) {
                console.error('Error fetching events:', error);
                return [];
            }
        },
        
        handleDateSelect(selectInfo) {
            this.booking.datetime = selectInfo.startStr.substring(0, 16);
            this.showBookingModal = true;
        },
        
        handleEventClick(clickInfo) {
            const event = clickInfo.event;
            alert(`Appointment Details:\nCustomer: ${event.title}\nEmail: ${event.extendedProps.customer_email}\nStatus: ${event.extendedProps.status}`);
        },
        
        async submitBooking() {
            try {
                const [date, time] = this.booking.datetime.split('T');
                
                const response = await fetch('/api/method/erpnext.www.booking_calendar.index.create_appointment_from_calendar', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        date: date,
                        time: time,
                        customer_name: this.booking.name,
                        customer_email: this.booking.email,
                        customer_phone: this.booking.phone
                    })
                });
                
                if (response.ok) {
                    this.closeModal();
                    this.$refs.fullCalendar.getApi().refetchEvents();
                    alert('Appointment booked successfully!');
                } else {
                    alert('Error booking appointment. Please try again.');
                }
            } catch (error) {
                console.error('Error submitting booking:', error);
                alert('Error booking appointment. Please try again.');
            }
        },
        
        closeModal() {
            this.showBookingModal = false;
            this.booking = {
                datetime: '',
                name: '',
                email: '',
                phone: ''
            };
        }
    }
}
</script>

<style scoped>
.booking-calendar {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-content {
    background: white;
    padding: 30px;
    border-radius: 8px;
    width: 90%;
    max-width: 500px;
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

.form-group input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
}

.form-actions button {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.form-actions button[type="button"] {
    background-color: #6c757d;
    color: white;
}

.form-actions button[type="submit"] {
    background-color: #007bff;
    color: white;
}
</style>
```

## Backend Integration Examples

### 4. Custom Python Controller

```python
# custom_booking_controller.py
import frappe
from frappe import _
from datetime import datetime, timedelta

class CustomBookingController:
    
    @frappe.whitelist(allow_guest=True)
    def get_custom_available_slots(self, date, service_type=None):
        """Get available slots with custom business logic"""
        
        # Custom business hours by service type
        business_hours = {
            'consultation': {'start': '09:00', 'end': '17:00'},
            'treatment': {'start': '10:00', 'end': '16:00'},
            'emergency': {'start': '08:00', 'end': '20:00'}
        }
        
        hours = business_hours.get(service_type, business_hours['consultation'])
        
        # Get existing appointments
        existing_appointments = frappe.get_all("Appointment",
            filters={
                "scheduled_time": ["between", [
                    f"{date} {hours['start']}:00",
                    f"{date} {hours['end']}:00"
                ]],
                "status": ["in", ["Open", "Confirmed"]]
            },
            fields=["scheduled_time"]
        )
        
        # Generate available slots
        available_slots = []
        start_time = datetime.strptime(f"{date} {hours['start']}:00", "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(f"{date} {hours['end']}:00", "%Y-%m-%d %H:%M:%S")
        
        current_time = start_time
        while current_time < end_time:
            # Check if slot is available
            if not any(apt['scheduled_time'] == current_time for apt in existing_appointments):
                available_slots.append({
                    'time': current_time.strftime("%H:%M"),
                    'datetime': current_time.isoformat(),
                    'available': True
                })
            
            current_time += timedelta(minutes=30)
        
        return available_slots
    
    @frappe.whitelist(allow_guest=True)
    def create_custom_appointment(self, **kwargs):
        """Create appointment with custom validation"""
        
        # Custom validation
        if kwargs.get('service_type') == 'vip' and not kwargs.get('phone'):
            frappe.throw(_("Phone number is required for VIP appointments"))
        
        # Create appointment
        appointment = frappe.new_doc("Appointment")
        appointment.customer_name = kwargs.get('customer_name')
        appointment.customer_email = kwargs.get('customer_email')
        appointment.customer_phone_number = kwargs.get('phone')
        appointment.scheduled_time = kwargs.get('scheduled_time')
        appointment.custom_service_type = kwargs.get('service_type')
        
        # Set priority based on service type
        if kwargs.get('service_type') == 'emergency':
            appointment.custom_priority = 'High'
        elif kwargs.get('service_type') == 'vip':
            appointment.custom_priority = 'Medium'
        else:
            appointment.custom_priority = 'Normal'
        
        appointment.insert(ignore_permissions=True)
        
        # Send custom notification
        self.send_custom_notification(appointment)
        
        return appointment
    
    def send_custom_notification(self, appointment):
        """Send custom email notification"""
        
        template = frappe.get_doc("Email Template", "Custom Appointment Confirmation")
        
        frappe.sendmail(
            recipients=[appointment.customer_email],
            subject=template.subject,
            message=frappe.render_template(template.response, {
                'customer_name': appointment.customer_name,
                'appointment_date': appointment.scheduled_time.strftime("%B %d, %Y"),
                'appointment_time': appointment.scheduled_time.strftime("%I:%M %p"),
                'service_type': appointment.custom_service_type
            })
        )
```

### 5. Custom Webhook Integration

```python
# webhook_handler.py
import frappe
import requests
import json
from frappe.utils import now

@frappe.whitelist()
def send_appointment_webhook(appointment_name, event_type):
    """Send appointment data to external webhook"""
    
    appointment = frappe.get_doc("Appointment", appointment_name)
    
    webhook_url = frappe.db.get_single_value("Booking Settings", "webhook_url")
    webhook_secret = frappe.db.get_single_value("Booking Settings", "webhook_secret")
    
    if not webhook_url:
        return
    
    payload = {
        'event': event_type,
        'timestamp': now(),
        'appointment': {
            'id': appointment.name,
            'customer_name': appointment.customer_name,
            'customer_email': appointment.customer_email,
            'scheduled_time': appointment.scheduled_time.isoformat(),
            'status': appointment.status
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
        'X-Webhook-Secret': webhook_secret
    }
    
    try:
        response = requests.post(webhook_url, 
                                data=json.dumps(payload), 
                                headers=headers,
                                timeout=30)
        
        # Log webhook response
        frappe.log_error(
            f"Webhook Response: {response.status_code} - {response.text}",
            "Appointment Webhook"
        )
        
    except Exception as e:
        frappe.log_error(str(e), "Appointment Webhook Error")

# Hook this function to appointment events
def on_appointment_update(doc, method):
    """Called when appointment is updated"""
    send_appointment_webhook(doc.name, "appointment.updated")

def on_appointment_insert(doc, method):
    """Called when appointment is created"""
    send_appointment_webhook(doc.name, "appointment.created")
```

### 6. Mobile App Integration

```javascript
// mobile_booking.js - For Frappe mobile app
frappe.ui.form.on('Appointment', {
    refresh: function(frm) {
        // Add custom mobile buttons
        if (frappe.is_mobile()) {
            frm.add_custom_button(__('Send SMS Reminder'), function() {
                send_sms_reminder(frm.doc);
            }, __('Actions'));
            
            frm.add_custom_button(__('Share Appointment'), function() {
                share_appointment(frm.doc);
            }, __('Actions'));
        }
    }
});

function send_sms_reminder(appointment) {
    frappe.call({
        method: 'custom_booking.mobile.send_sms_reminder',
        args: {
            appointment_id: appointment.name
        },
        callback: function(response) {
            if (response.message.success) {
                frappe.show_alert({
                    message: __('SMS reminder sent successfully'),
                    indicator: 'green'
                });
            }
        }
    });
}

function share_appointment(appointment) {
    if (navigator.share) {
        navigator.share({
            title: 'Appointment Details',
            text: `Appointment with ${appointment.customer_name} on ${appointment.scheduled_time}`,
            url: `/app/appointment/${appointment.name}`
        });
    }
}
```

## Configuration Examples

### 7. Custom Business Hours Configuration

```python
# business_hours_config.py
BUSINESS_HOURS_CONFIG = {
    'default': {
        'monday': {'start': '09:00', 'end': '17:00', 'break_start': '12:00', 'break_end': '13:00'},
        'tuesday': {'start': '09:00', 'end': '17:00', 'break_start': '12:00', 'break_end': '13:00'},
        'wednesday': {'start': '09:00', 'end': '17:00', 'break_start': '12:00', 'break_end': '13:00'},
        'thursday': {'start': '09:00', 'end': '17:00', 'break_start': '12:00', 'break_end': '13:00'},
        'friday': {'start': '09:00', 'end': '17:00', 'break_start': '12:00', 'break_end': '13:00'},
        'saturday': {'start': '10:00', 'end': '14:00'},
        'sunday': {'closed': True}
    },
    'spa': {
        'monday': {'start': '08:00', 'end': '20:00'},
        'tuesday': {'start': '08:00', 'end': '20:00'},
        'wednesday': {'start': '08:00', 'end': '20:00'},
        'thursday': {'start': '08:00', 'end': '20:00'},
        'friday': {'start': '08:00', 'end': '20:00'},
        'saturday': {'start': '09:00', 'end': '18:00'},
        'sunday': {'start': '10:00', 'end': '16:00'}
    },
    'medical': {
        'monday': {'start': '07:00', 'end': '19:00'},
        'tuesday': {'start': '07:00', 'end': '19:00'},
        'wednesday': {'start': '07:00', 'end': '19:00'},
        'thursday': {'start': '07:00', 'end': '19:00'},
        'friday': {'start': '07:00', 'end': '19:00'},
        'saturday': {'start': '08:00', 'end': '12:00'},
        'sunday': {'closed': True}
    }
}
```

### 8. Email Templates

```html
<!-- appointment_confirmation_template.html -->
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <div style="background-color: #f8f9fa; padding: 20px; text-align: center;">
        <h1 style="color: #007bff; margin: 0;">Appointment Confirmed</h1>
    </div>
    
    <div style="padding: 30px;">
        <p>Dear {{ customer_name }},</p>
        
        <p>Your appointment has been successfully booked. Here are the details:</p>
        
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="margin-top: 0; color: #495057;">Appointment Details</h3>
            <p><strong>Date:</strong> {{ appointment_date }}</p>
            <p><strong>Time:</strong> {{ appointment_time }}</p>
            <p><strong>Service:</strong> {{ service_type }}</p>
            <p><strong>Reference ID:</strong> {{ appointment_id }}</p>
        </div>
        
        <div style="background-color: #d4edda; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #28a745;">
            <p style="margin: 0; color: #155724;">
                <strong>Please save this email for your records.</strong>
                You may need the reference ID for any future communication.
            </p>
        </div>
        
        <p>If you need to reschedule or cancel this appointment, please contact us at least 24 hours in advance.</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{{ booking_url }}" style="background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">
                View Appointment Details
            </a>
        </div>
        
        <p>Thank you for choosing our services!</p>
        
        <hr style="border: none; border-top: 1px solid #dee2e6; margin: 30px 0;">
        
        <div style="color: #6c757d; font-size: 14px;">
            <p>This is an automated message. Please do not reply to this email.</p>
            <p>If you have any questions, please contact us at support@yourcompany.com</p>
        </div>
    </div>
</div>
```

These examples provide practical implementation patterns that developers can use to integrate and extend the booking calendar system according to their specific requirements.