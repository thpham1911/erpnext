# Developer Guide - Booking Calendar & Appointment System

## Architecture Overview

The booking system consists of three main components:

```
┌─────────────────────┐    ┌──────────────────────┐    ┌─────────────────────┐
│   Booking Calendar  │    │   Book Appointment   │    │   Spa Management    │
│                     │    │                      │    │                     │
│ - FullCalendar.js   │    │ - Step-by-step form  │    │ - Professional mgmt │
│ - Interactive UI    │    │ - Public access      │    │ - Service & staff   │
│ - Real-time updates │    │ - Email verification │    │ - Billing integration│
└─────────────────────┘    └──────────────────────┘    └─────────────────────┘
           │                           │                           │
           └───────────────────────────┼───────────────────────────┘
                                       │
                              ┌──────────────────┐
                              │   Appointment    │
                              │     DocType      │
                              │                  │
                              │ - Core data      │
                              │ - Status mgmt    │
                              │ - Permissions    │
                              └──────────────────┘
```

## File Structure

```
erpnext/
├── www/
│   ├── booking_calendar/           # Interactive Calendar UI
│   │   ├── index.html             # Main calendar template
│   │   ├── index.js               # FullCalendar integration
│   │   ├── index.py               # Backend API methods
│   │   └── index.css              # Calendar styling
│   │
│   └── book_appointment/           # Traditional booking form
│       ├── index.html             # Multi-step form
│       ├── index.js               # Form handling
│       ├── index.py               # Booking logic
│       └── verify/                # Email verification
│           ├── index.html
│           └── index.py
│
├── crm/doctype/appointment/        # Core appointment system
│   ├── appointment.py             # Main appointment logic
│   ├── appointment.js             # Form customization
│   └── appointment_calendar.js    # Calendar view config
│
└── spa/                           # Spa management system
    ├── doctype/
    │   ├── spa_appointment/       # Spa-specific appointments
    │   ├── spa_service/          # Service definitions
    │   ├── spa_room/             # Room management
    │   └── spa_membership/       # Customer memberships
    └── web_form/                 # Public booking forms
```

## API Documentation

### Booking Calendar APIs

#### Get Events
```python
@frappe.whitelist(allow_guest=True)
def get_booking_calendar_events(start, end):
    """
    Get appointment events for calendar view
    
    Args:
        start (str): Start date in ISO format
        end (str): End date in ISO format
        
    Returns:
        list: Array of calendar events
    """
```

**Request:**
```javascript
frappe.call({
    method: 'erpnext.www.booking_calendar.index.get_booking_calendar_events',
    args: {
        start: '2024-01-01T00:00:00Z',
        end: '2024-01-31T23:59:59Z'
    }
})
```

**Response:**
```javascript
[
    {
        "id": "APPT-2024-00001",
        "title": "John Doe",
        "start": "2024-01-15T10:00:00",
        "backgroundColor": "#28a745",
        "extendedProps": {
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "status": "Open",
            "appointment_id": "APPT-2024-00001"
        }
    }
]
```

#### Create Appointment
```python
@frappe.whitelist(allow_guest=True)
def create_appointment_from_calendar(date, time, customer_name, customer_email, 
                                   customer_phone=None, customer_notes=None, timezone="UTC"):
    """
    Create appointment from calendar interface
    
    Args:
        date (str): Appointment date (YYYY-MM-DD)
        time (str): Appointment time (HH:MM)
        customer_name (str): Customer name
        customer_email (str): Customer email
        customer_phone (str, optional): Phone number
        customer_notes (str, optional): Additional notes
        timezone (str): Customer timezone
        
    Returns:
        dict: Created appointment details
    """
```

### Book Appointment APIs

#### Get Available Slots
```python
@frappe.whitelist(allow_guest=True)
def get_appointment_slots(date, timezone):
    """
    Get available time slots for a specific date
    
    Args:
        date (str): Date in YYYY-MM-DD format
        timezone (str): Customer timezone
        
    Returns:
        list: Available time slots
    """
```

#### Create Appointment
```python
@frappe.whitelist(allow_guest=True)
def create_appointment(date, time, tz, contact):
    """
    Create appointment from booking form
    
    Args:
        date (str): Appointment date
        time (str): Appointment time
        tz (str): Timezone
        contact (str): JSON string with contact details
        
    Returns:
        object: Created appointment document
    """
```

### Spa Management APIs

#### Get Available Time Slots
```python
@frappe.whitelist()
def get_available_time_slots(date, service, staff=None):
    """
    Get available time slots for spa services
    
    Args:
        date (str): Date in YYYY-MM-DD format
        service (str): Spa Service name
        staff (str, optional): Staff member filter
        
    Returns:
        list: Available time slots with staff assignments
    """
```

## Frontend Integration

### FullCalendar Configuration
```javascript
// booking_calendar/index.js
calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    selectable: true,
    selectMirror: true,
    businessHours: {
        daysOfWeek: [1, 2, 3, 4, 5], // Monday - Friday
        startTime: '09:00',
        endTime: '17:00'
    },
    events: function(fetchInfo, successCallback, failureCallback) {
        // Fetch events from server
        frappe.call({
            method: 'erpnext.www.booking_calendar.index.get_booking_calendar_events',
            args: {
                start: fetchInfo.start.toISOString(),
                end: fetchInfo.end.toISOString()
            },
            callback: function(response) {
                successCallback(response.message);
            }
        });
    }
});
```

### Modal Integration
```javascript
// Show booking modal
function showAppointmentModal(date) {
    const modal = new bootstrap.Modal(document.getElementById('appointmentModal'));
    modal.show();
}

// Save appointment
function saveAppointment() {
    frappe.call({
        method: 'erpnext.www.booking_calendar.index.create_appointment_from_calendar',
        args: {
            date: selectedDate,
            time: selectedTime,
            customer_name: customerName,
            customer_email: customerEmail
        },
        callback: function(response) {
            calendar.refetchEvents();
        }
    });
}
```

## Database Schema

### Appointment DocType
```python
class Appointment(Document):
    # Core fields
    customer_name: DF.Data
    customer_email: DF.Data  
    customer_phone_number: DF.Data
    scheduled_time: DF.Datetime
    status: DF.Literal["Open", "Unverified", "Closed"]
    
    # Linking fields
    appointment_with: DF.Link
    party: DF.DynamicLink
    calendar_event: DF.Link
    
    # Additional info
    customer_details: DF.LongText
    customer_skype: DF.Data
```

### Spa Appointment DocType
```python
class SpaAppointment(Document):
    # Basic info
    customer: DF.Link
    spa_service: DF.Link
    appointment_date: DF.Date
    appointment_time: DF.Time
    
    # Assignment
    assigned_staff: DF.Link
    spa_room: DF.Link
    
    # Pricing
    service_price: DF.Currency
    discount_amount: DF.Currency
    final_price: DF.Currency
    
    # Status tracking
    status: DF.Literal["Scheduled", "Confirmed", "In Progress", "Completed", "Cancelled"]
    confirmed_at: DF.Datetime
    completed_at: DF.Datetime
    cancelled_at: DF.Datetime
```

## Customization Examples

### Adding Custom Fields
```python
# In hooks.py
doc_events = {
    "Appointment": {
        "validate": "custom_app.appointment.validate_custom_fields"
    }
}

# In custom_app/appointment.py
def validate_custom_fields(doc, method):
    if doc.custom_department:
        # Custom validation logic
        pass
```

### Custom Calendar Colors
```css
/* In booking_calendar/index.css */
.fc-event.priority-high {
    background-color: #dc3545 !important;
    border-color: #dc3545 !important;
}

.fc-event.priority-medium {
    background-color: #ffc107 !important;
    border-color: #ffc107 !important;
}
```

### Email Templates
```html
<!-- Appointment Confirmation Email -->
<div>
    <h2>Appointment Confirmed</h2>
    <p>Dear {{ customer_name }},</p>
    <p>Your appointment has been confirmed for:</p>
    <ul>
        <li><strong>Date:</strong> {{ formatted_date }}</li>
        <li><strong>Time:</strong> {{ formatted_time }}</li>
        <li><strong>Service:</strong> {{ service_name }}</li>
    </ul>
</div>
```

## Performance Optimization

### Database Indexes
```sql
-- Add indexes for faster queries
ALTER TABLE `tabAppointment` ADD INDEX `scheduled_time_status` (`scheduled_time`, `status`);
ALTER TABLE `tabSpa Appointment` ADD INDEX `appointment_date_staff` (`appointment_date`, `assigned_staff`);
```

### Caching Strategy
```python
# Cache available slots
@frappe.whitelist()
def get_available_slots_cached(date, service):
    cache_key = f"spa_slots_{date}_{service}"
    cached_slots = frappe.cache().get(cache_key)
    
    if not cached_slots:
        cached_slots = get_available_time_slots(date, service)
        frappe.cache().set(cache_key, cached_slots, expires_in_sec=300)
    
    return cached_slots
```

## Security Considerations

### Permission Control
```python
# In appointment.py
def has_permission(doc, user=None, permission_type=None):
    if permission_type == "read":
        # Allow customers to read their own appointments
        if doc.customer_email == frappe.session.user:
            return True
    
    # Default permission check
    return False
```

### Input Validation
```python
def validate_appointment_data(data):
    # Sanitize inputs
    data['customer_name'] = frappe.utils.sanitize_html(data.get('customer_name', ''))
    data['customer_email'] = frappe.utils.validate_email_address(data.get('customer_email'))
    
    # Check for required fields
    if not data.get('customer_name') or not data.get('customer_email'):
        frappe.throw(_("Name and Email are required"))
    
    return data
```

## Testing

### Unit Tests
```python
# In test_appointment.py
class TestAppointment(unittest.TestCase):
    def test_create_appointment(self):
        appointment = frappe.get_doc({
            "doctype": "Appointment",
            "customer_name": "Test Customer",
            "customer_email": "test@example.com",
            "scheduled_time": "2024-01-15 10:00:00"
        })
        appointment.insert()
        
        self.assertEqual(appointment.status, "Open")
        self.assertTrue(appointment.name)
```

### Integration Tests
```python
def test_booking_calendar_api():
    # Test API endpoint
    response = frappe.call(
        "erpnext.www.booking_calendar.index.get_booking_calendar_events",
        start="2024-01-01T00:00:00Z",
        end="2024-01-31T23:59:59Z"
    )
    
    assert isinstance(response, list)
```

## Deployment Checklist

- [ ] Enable appointment booking in settings
- [ ] Configure business hours
- [ ] Set up holiday list  
- [ ] Configure email templates
- [ ] Set appropriate permissions
- [ ] Test all booking flows
- [ ] Verify mobile responsiveness
- [ ] Check API endpoints
- [ ] Monitor performance
- [ ] Setup backup procedures