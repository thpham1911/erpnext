# Booking Calendar and Appointment Management User Guide

## Overview

ERPNext has been integrated with modern appointment scheduling and calendar booking features, including:

1. **Booking Calendar UI** - Interactive calendar interface for viewing and booking appointments
2. **Book Appointment System** - Traditional appointment booking system
3. **Spa Management System** - Professional spa appointment and service management

---

## 1. Booking Calendar UI

### Purpose
Modern calendar interface using FullCalendar to display and manage appointments visually.

### Access
- URL: `https://your-domain.com/booking_calendar`
- Menu: Direct access via URL or integration into main menu

### Key Features

#### 1.1 View Appointments
- **Calendar Display**: Shows calendar in month, week, or day view
- **Color Coding**:
  - 🟢 **Green**: Open appointments
  - 🟡 **Yellow**: Unverified appointments  
  - ⚫ **Gray**: Closed appointments

#### 1.2 Book New Appointments
**Method 1: Click on date/time in calendar**
1. Click on desired time slot in the calendar
2. Booking popup will appear
3. Fill in information:
   - **Date & Time**: Auto-filled from selected slot
   - **Customer Name**: Required
   - **Email**: Required
   - **Phone**: Optional
   - **Notes**: Optional
4. Click "Book Appointment" to confirm

**Method 2: Use "Book New Appointment" button**
1. Click "Book New Appointment" button in sidebar
2. Follow same steps as Method 1

#### 1.3 View Appointment Details
1. Click on an existing appointment in the calendar
2. Details popup will display:
   - Customer information
   - Appointment time
   - Current status
   - Management buttons (if permitted)

#### 1.4 Manage Status (Admin only)
If you have management permissions, you can:
- **Mark Unverified**: Mark as unverified
- **Mark Open**: Mark as open
- **Mark Closed**: Mark as closed

### Setup and Configuration

#### Enable feature
1. Go to **Appointment Booking Settings**
2. Enable "Enable Scheduling"
3. Configure business hours (default: 9:00-17:00, Monday-Friday)

#### Customize interface
- CSS file: `erpnext/www/booking_calendar/index.css`
- JS file: `erpnext/www/booking_calendar/index.js`
- HTML file: `erpnext/www/booking_calendar/index.html`

---

## 2. Book Appointment System

### Purpose
Traditional appointment booking system with step-by-step form, suitable for external customers.

### Access
- URL: `https://your-domain.com/book_appointment`
- Usually embedded in website or shared as public link

### Booking Process

#### Step 1: Select Date and Timezone
1. Choose desired date
2. Select appropriate timezone
3. System will display available time slots

#### Step 2: Choose Time
1. View available time slots
2. Click to select preferred slot
3. Click "Next" to continue

#### Step 3: Enter Information
1. **Name**: Required
2. **Phone**: Optional
3. **Email**: Required
4. **Skype**: Optional (for online meetings)
5. **Notes**: Detailed description of appointment

#### Step 4: Confirm
1. Review entered information
2. Click "Book Appointment"
3. System will send confirmation email

### Advanced Features

#### Automatic customer classification
- System automatically searches for existing Lead or Customer
- Creates new if not found
- Links appointment to correct contact

#### Email verification
- Verification URL: `https://your-domain.com/book_appointment/verify`
- Automatic email with verification link
- Status changes from "Unverified" to "Open"

---

## 3. Spa Management System

### Purpose  
Professional spa appointment management system with complete features for service, staff, and payment management.

### Main DocTypes

#### 3.1 Spa Service
**Purpose**: Manage spa services
**Key Information**:
- Service name
- Description
- Duration (minutes)
- Price
- Category

#### 3.2 Spa Room
**Purpose**: Manage spa rooms
**Key Information**:
- Room name
- Room type
- Status
- Description

#### 3.3 Spa Appointment
**Purpose**: Detailed spa appointments
**Key Information**:
- Customer
- Service
- Assigned staff
- Room
- Time
- Status
- Final price

### Usage Workflow

#### Initial Setup
1. **Create Spa Services**:
   - Go to "Spa Service" doctype
   - Create services: massage, facial, manicure, etc.
   - Set duration and price

2. **Create Spa Rooms**:
   - Go to "Spa Room" doctype
   - Create spa rooms
   - Categorize by service

3. **Setup Staff**:
   - Create User for staff
   - Assign appropriate permissions

#### Create spa appointments
1. **Basic Information**:
   - Customer: Select or create new
   - Service: Choose spa service
   - Date & Time: Select time

2. **Assignment**:
   - Assigned Staff: Choose staff member
   - Room: Choose room (optional)

3. **Confirm and Payment**:
   - Review information
   - Auto-create Sales Invoice
   - Track status

### Status Management

#### Main Statuses:
- **Scheduled**: Scheduled
- **Confirmed**: Confirmed  
- **In Progress**: In progress
- **Completed**: Completed
- **Cancelled**: Cancelled

#### Automatic Workflow:
1. **Scheduled → Confirmed**: Send SMS/Email confirmation
2. **Confirmed → In Progress**: Start service
3. **In Progress → Completed**: Auto-create invoice, save history
4. **Any → Cancelled**: Record cancellation time

### API and Integration

#### Get available time slots
```python
# API call
frappe.call({
    method: 'erpnext.spa.doctype.spa_appointment.spa_appointment.get_available_time_slots',
    args: {
        date: '2024-01-15',
        service: 'Massage Service',
        staff: 'staff@example.com'  // optional
    }
})
```

#### Create appointment via API  
```python
# Create new appointment
appointment = frappe.new_doc('Spa Appointment')
appointment.customer = 'Customer Name'
appointment.spa_service = 'Service Name'  
appointment.appointment_date = '2024-01-15'
appointment.appointment_time = '10:00:00'
appointment.assigned_staff = 'staff@example.com'
appointment.insert()
```

---

## 4. Integration and Customization

### Calendar system integration
All appointments from the 3 systems appear in:
- Desktop Calendar app
- Mobile calendar sync
- Booking Calendar UI

### Interface customization
```css
/* Customize colors in booking_calendar/index.css */
.fc-event.status-open {
    background-color: #28a745 !important;
}

.fc-event.status-unverified {
    background-color: #ffc107 !important;
}
```

### Webhooks and notifications
```python
# Hook after appointment creation
def after_insert(self):
    # Send notification
    self.send_notifications_if_needed()
    
    # Webhook to external systems
    if self.status == 'Confirmed':
        send_webhook_notification(self)
```

---

## 5. Troubleshooting

### Common Issues

#### Error: "Appointment Scheduling Disabled"
**Cause**: Feature not enabled in settings
**Solution**: 
1. Go to "Appointment Booking Settings"
2. Check "Enable Scheduling"

#### Error: "No time slots available"  
**Cause**: Business hours or holiday list configuration
**Solution**:
1. Check Business Hours in calendar settings
2. Check Holiday List
3. Ensure no conflicts with existing appointments

#### Calendar not showing events
**Cause**: JavaScript error or access permissions
**Solution**:
1. Check browser console for JS errors
2. Verify user permissions for Appointment doctype
3. Verify API endpoints are working

### Performance optimization
```python
# Add indexes for faster queries
frappe.db.add_index("Appointment", ["scheduled_time", "status"])
frappe.db.add_index("Spa Appointment", ["appointment_date", "assigned_staff"])
```

---

## 6. Conclusion

ERPNext's booking calendar and appointment system provides:

✅ **3 flexible interfaces** for different use cases
✅ **Automated workflow** from booking to billing  
✅ **Complete APIs** for external integration
✅ **Mobile responsive** for all devices
✅ **Multi-timezone support** for international customers
✅ **Permission system** secured by roles

The system is suitable for:
- **Spa & Wellness centers**
- **Medical clinics**  
- **Consultancy services**
- **Any appointment-based business**

For additional support, please contact the development team or refer to ERPNext documentation.