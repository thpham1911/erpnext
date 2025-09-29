# Spa Management System - ERPNext

A comprehensive spa management system built for ERPNext that handles all aspects of spa operations including customer management, service booking, staff scheduling, and revenue tracking.

## Features

### 1. Customer Management (CRM & Profile Enhancement)
- **Enhanced Customer Profile**: Added date of birth, customer categories (New, Regular, VIP), preferences
- **Customer Service History**: Comprehensive tracking of all services used by customers
- **Automatic Customer Categorization**: Based on service history (New → Regular → VIP)
- **Birthday Reminders**: Automated SMS/email reminders with special offers
- **Marketing Preferences**: Opt-in/opt-out for promotional communications

### 2. Service Management
- **Spa Service Master**: Complete service catalog with categories (Massage, Skincare, Hair Care, etc.)
- **Dynamic Pricing**: Customer category-based pricing with automatic discounts
- **Service Duration Management**: Configurable service durations and staff requirements
- **Room Requirements**: Automatic room assignment based on service type

### 3. Appointment & Scheduling Management
- **Comprehensive Appointment Booking**: Full appointment lifecycle management
- **Real-time Availability Checking**: Staff and room availability validation
- **Status Tracking**: Scheduled → Confirmed → In Progress → Completed → Cancelled
- **Automated Notifications**: SMS and email confirmations and reminders
- **Online Booking Integration**: Web form for customer self-booking

### 4. Staff & Resource Management
- **Room Management**: Complete spa room tracking with status and maintenance
- **Equipment Tracking**: Equipment lists and maintenance schedules
- **Staff Assignment**: Skill-based staff assignment to services
- **Availability Management**: Real-time staff and room availability

### 5. Membership & Loyalty Programs
- **Flexible Membership Types**: Basic, Silver, Gold, Platinum, VIP, Couple, Family
- **Session-based Packages**: Track usage and remaining sessions
- **Automatic Benefits**: Discounts, priority booking, complimentary services
- **Renewal Management**: Automated renewal reminders

### 6. Billing & Payment Integration
- **Automatic Sales Invoice Creation**: When appointments are completed
- **Service Item Management**: Auto-creation of items for spa services
- **Multiple Payment Methods**: Cash, card, mobile payments, package credits
- **Vietnam E-Invoice Ready**: Structured for Vietnamese tax compliance

### 7. Reporting & Analytics
- **Revenue Analysis**: By service, staff, time periods
- **Customer Analytics**: Service history, frequency, lifetime value
- **Staff Performance**: Bookings, revenue generation, customer satisfaction
- **Room Utilization**: Occupancy rates and efficiency metrics

### 8. Customer Experience & Marketing
- **Automated Communication**: Birthday greetings, appointment reminders, promotions
- **Membership Benefits Tracking**: Automatic application of member discounts
- **Personalized Offers**: Based on service history and customer preferences
- **Online Presence**: Web-based booking system

## Module Structure

```
erpnext/spa/
├── doctype/
│   ├── spa_service/              # Service master data
│   ├── spa_appointment/          # Appointment management
│   ├── customer_service_history/ # Service usage tracking
│   ├── spa_room/                # Room and facility management
│   └── spa_membership/          # Membership and packages
├── report/
│   └── spa_revenue_summary/     # Revenue analysis report
├── workspace/
│   └── spa_management.json      # Dashboard and navigation
├── web_form/
│   └── spa_appointment_booking/ # Online booking form
├── utils.py                     # Utility functions
└── fixtures.py                 # Default data setup
```

## Installation & Setup

### 1. Enable Spa Module
The spa module is automatically added to ERPNext. No additional installation required.

### 2. Default Data Setup
Run the following to create default roles, services, and rooms:
```python
from erpnext.spa.fixtures import create_fixtures
create_fixtures()
```

### 3. Configure Scheduler Events
The system includes daily scheduler events for:
- Birthday reminders
- Appointment reminders  
- Membership renewal notifications
- Room status updates

### 4. Setup Roles & Permissions
Default roles created:
- **Spa Manager**: Full access to all spa operations
- **Spa Staff**: Service delivery and customer interaction
- **Spa Receptionist**: Booking and customer service

## Usage Guide

### Customer Management
1. **Adding Customers**: Enhanced customer form with spa-specific fields
2. **Service History**: Automatically tracked when appointments are completed
3. **Categories**: Automatically updated based on service frequency

### Service Management  
1. **Create Services**: Define services with pricing, duration, and requirements
2. **Pricing Rules**: Automatic discounts based on customer categories
3. **Room Assignment**: Services can require specific room types

### Appointment Booking
1. **Manual Booking**: Full appointment form with customer, service, and staff selection
2. **Online Booking**: Customer self-service booking through web form
3. **Availability Checking**: Real-time validation of staff and room availability

### Membership Management
1. **Create Memberships**: Define packages with session counts and benefits
2. **Usage Tracking**: Automatic deduction of sessions when services are used
3. **Benefits Application**: Automatic application of member discounts

### Billing Process
1. **Appointment Completion**: Mark appointments as completed
2. **Invoice Generation**: Sales invoices automatically created
3. **Payment Recording**: Standard ERPNext payment entry process

## Customization

### Adding New Service Categories
Update the `service_category` field options in the Spa Service doctype.

### Modifying Customer Categories  
Update the `customer_category` field options in the Customer doctype.

### Custom Pricing Rules
Extend the `get_price_for_customer()` method in Spa Service.

### Additional Reports
Create new reports in the `spa/report/` directory following the existing structure.

## API Integration

### Online Booking API
```javascript
frappe.call({
    method: 'erpnext.spa.web_form.spa_appointment_booking.spa_appointment_booking.submit_appointment_request',
    args: {
        data: {
            customer_name: 'John Doe',
            customer_mobile: '0912345678',
            spa_service: 'SPA-SRV-2024-00001',
            appointment_date: '2024-10-15',
            appointment_time: '14:00:00'
        }
    }
})
```

### Get Available Slots
```javascript
frappe.call({
    method: 'erpnext.spa.doctype.spa_appointment.spa_appointment.get_available_time_slots',
    args: {
        date: '2024-10-15',
        service: 'SPA-SRV-2024-00001'
    }
})
```

## Maintenance

### Daily Tasks (Automated)
- Birthday reminders sent at 9 AM
- Appointment reminders sent at 6 PM for next day
- Membership renewal reminders for expiring memberships
- Room status updates every hour

### Weekly Tasks
- Review customer categories and upgrade eligible customers
- Check for expired memberships
- Analyze service performance and adjust pricing

### Monthly Tasks  
- Generate comprehensive revenue reports
- Review staff performance metrics
- Plan promotional campaigns based on customer data

## Support

For technical support or feature requests, please refer to the ERPNext documentation or contact your system administrator.

## License

This spa management system is part of ERPNext and follows the same GNU General Public License v3.