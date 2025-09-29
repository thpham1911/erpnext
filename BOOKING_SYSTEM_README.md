# Booking Calendar & Appointment Management

## 📅 Overview

This repository contains a comprehensive appointment booking and calendar management system for ERPNext, featuring three integrated solutions:

- **🎯 Interactive Booking Calendar** - Modern FullCalendar-based UI
- **📋 Traditional Appointment Booking** - Step-by-step public booking form  
- **💆 Professional Spa Management** - Complete spa service management system

## 🚀 Quick Start

### 1-Minute Setup
```bash
# Enable the feature
1. Go to: Setup > Appointment Booking Settings
2. Check: "Enable Scheduling"
3. Visit: https://your-site.com/booking_calendar
```

### Features at a Glance
✅ **Interactive Calendar UI** with drag & drop  
✅ **Public booking forms** for customers  
✅ **Spa & wellness management** with staff scheduling  
✅ **Multi-timezone support** for global businesses  
✅ **Mobile responsive** design  
✅ **Email verification** and notifications  
✅ **REST APIs** for integration  
✅ **Role-based permissions**  

## 📖 Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| [🇻🇳 Vietnamese User Guide](./USER_GUIDE_BOOKING_CALENDAR.md) | Complete feature guide in Vietnamese | End Users |
| [🇺🇸 English User Guide](./USER_GUIDE_BOOKING_CALENDAR_EN.md) | Complete feature guide in English | End Users |
| [⚡ Quick Setup Guide](./QUICK_SETUP_GUIDE.md) | 5-minute setup instructions | Administrators |
| [👨‍💻 Developer Guide](./DEVELOPER_GUIDE.md) | Technical implementation details | Developers |

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ERPNext Integration                      │
├─────────────────────┬─────────────────────┬─────────────────┤
│  Booking Calendar   │  Book Appointment   │  Spa Management │
│                     │                     │                 │
│ ╭─────────────────╮ │ ╭─────────────────╮ │ ╭─────────────╮ │
│ │ FullCalendar.js │ │ │ Multi-step Form │ │ │ Service Mgmt│ │
│ │ Interactive UI  │ │ │ Public Access   │ │ │ Staff Sched │ │
│ │ Real-time      │ │ │ Email Verify    │ │ │ Room Mgmt   │ │
│ ╰─────────────────╯ │ ╰─────────────────╯ │ ╰─────────────╯ │
└─────────────────────┴─────────────────────┴─────────────────┘
                              │
                    ╭─────────────────╮
                    │  Core Services  │
                    │                 │
                    │ • Appointments  │
                    │ • Notifications │
                    │ • Permissions   │
                    │ • API Layer     │
                    ╰─────────────────╯
```

## 🎯 Use Cases

### 🏥 Healthcare Clinics
- Patient appointment scheduling
- Doctor availability management
- Treatment room booking
- Medical service categorization

### 💆 Spa & Wellness Centers  
- Service booking (massage, facial, etc.)
- Staff and room assignments
- Customer membership management
- Automated billing integration

### 💼 Professional Services
- Consultation scheduling  
- Meeting room booking
- Client management
- Service package offerings

### 🏢 General Business
- Meeting scheduling
- Resource booking
- Customer appointments
- Staff calendar management

## 📱 Screenshots & UI

### Booking Calendar Interface
The modern calendar interface provides:
- Month/Week/Day views
- Color-coded appointment status
- Click-to-book functionality
- Real-time updates

### Traditional Booking Form
Step-by-step booking process:
1. Select date and timezone
2. Choose available time slot  
3. Enter customer information
4. Confirm and receive verification email

### Spa Management Dashboard
Professional spa features:
- Service catalog with pricing
- Staff availability scheduling
- Room assignment optimization
- Automated invoice generation

## 🔧 Configuration

### Basic Setup
```python
# Enable appointment booking
Appointment Booking Settings:
  - Enable Scheduling: ✓
  - Business Hours: 09:00 - 17:00
  - Working Days: Monday - Friday
  - Holiday List: [Select your holiday list]
```

### Advanced Configuration
```python
# Business hours customization
Business Hours:
  - Monday: 09:00 - 17:00
  - Tuesday: 09:00 - 17:00  
  - Wednesday: 09:00 - 17:00
  - Thursday: 09:00 - 17:00
  - Friday: 09:00 - 17:00
  - Saturday: 10:00 - 14:00  # Optional
  - Sunday: Closed

# Slot configuration
Default Settings:
  - Slot Duration: 30 minutes
  - Advance Booking: 30 days
  - Minimum Notice: 2 hours
```

## 🔌 API Reference

### REST Endpoints

#### Get Available Slots
```http
GET /api/method/erpnext.www.booking_calendar.index.get_available_slots_for_date
```

#### Create Appointment
```http
POST /api/method/erpnext.www.booking_calendar.index.create_appointment_from_calendar
```

#### Get Calendar Events
```http
GET /api/method/erpnext.www.booking_calendar.index.get_booking_calendar_events
```

### JavaScript Integration
```javascript
// Get available slots
frappe.call({
    method: 'erpnext.www.booking_calendar.index.get_available_slots_for_date',
    args: {
        date: '2024-01-15',
        timezone: 'Asia/Ho_Chi_Minh'
    },
    callback: function(response) {
        console.log('Available slots:', response.message);
    }
});
```

## 🎨 Customization

### Theme Customization
```css
/* Custom colors for appointment status */
.fc-event.status-open {
    background-color: #28a745 !important;
    border-color: #28a745 !important;
}

.fc-event.status-unverified {
    background-color: #ffc107 !important;
    border-color: #ffc107 !important;
}

.fc-event.status-closed {
    background-color: #6c757d !important;
    border-color: #6c757d !important;
}
```

### Business Logic Extension
```python
# Custom validation hooks
def validate_appointment(doc, method):
    # Add custom business rules
    if doc.appointment_type == "VIP":
        doc.priority = "High"
    
    # Custom pricing logic
    if doc.customer_type == "Member":
        doc.discount_percentage = 10
```

## 🔒 Security & Permissions

### Role-Based Access Control
| Role | Permissions |
|------|-------------|
| Guest | View public calendar, book appointments |
| Customer | View own appointments, book new appointments |
| Staff | Manage assigned appointments, update status |
| Manager | Full appointment management, reports |
| System Manager | System configuration, all permissions |

### Data Protection
- ✅ Input sanitization on all forms
- ✅ Email validation and verification  
- ✅ Permission-based data access
- ✅ Audit trail for all changes
- ✅ GDPR compliance ready

## 📊 Reporting & Analytics

### Built-in Reports
- Appointment Summary by Status
- Staff Utilization Report  
- Revenue by Service Type
- Customer Booking Patterns
- Cancellation Analysis

### Custom Dashboards
Create custom dashboards to track:
- Daily/Weekly/Monthly bookings
- Staff performance metrics
- Room utilization rates
- Revenue trends
- Customer satisfaction scores

## 🧪 Testing

### Automated Testing
```bash
# Run appointment tests
bench --site your-site run-tests erpnext.crm.doctype.appointment

# Run spa management tests  
bench --site your-site run-tests erpnext.spa
```

### Manual Testing Checklist
- [ ] Book appointment via calendar UI
- [ ] Book appointment via traditional form
- [ ] Verify email confirmation flow
- [ ] Test appointment status changes
- [ ] Validate business hours restrictions
- [ ] Check mobile responsiveness
- [ ] Test permission restrictions

## 🚀 Deployment

### Production Checklist
- [ ] Configure proper business hours
- [ ] Set up email templates and SMTP
- [ ] Configure holiday lists
- [ ] Set appropriate user permissions
- [ ] Test all booking flows
- [ ] Monitor server performance
- [ ] Setup backup procedures
- [ ] Configure SSL certificates
- [ ] Test mobile experience

### Performance Optimization
```python
# Database indexes
frappe.db.add_index("Appointment", ["scheduled_time", "status"])
frappe.db.add_index("Spa Appointment", ["appointment_date", "assigned_staff"])

# Caching configuration
CACHE_CONFIG = {
    "available_slots": 300,  # 5 minutes
    "business_hours": 3600,  # 1 hour  
    "holiday_list": 86400,   # 24 hours
}
```

## 🆘 Troubleshooting

### Common Issues

**Calendar not loading**
- Check "Enable Scheduling" in settings
- Verify user permissions
- Check browser console for JavaScript errors

**No time slots available** 
- Verify business hours configuration
- Check holiday list settings
- Ensure no conflicting appointments

**Email notifications not working**
- Configure SMTP settings
- Check email templates
- Verify email queue processing

### Support Resources
- 📚 [ERPNext Documentation](https://docs.erpnext.com)
- 💬 [Community Forum](https://discuss.erpnext.com)  
- 🐛 [GitHub Issues](https://github.com/frappe/erpnext/issues)
- 📧 Professional Support: Contact Frappe Partners

## 📝 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](../license.txt) file for details.

## 🤝 Contributing

We welcome contributions! Please read our contributing guidelines and submit pull requests for any improvements.

### Development Setup
```bash
# Clone repository
git clone https://github.com/thpham1911/erpnext.git

# Setup development environment
cd erpnext
pip install -e .

# Run development server
bench start
```

## 📞 Support

For technical support or customization requests:

- **Community Support**: ERPNext Forum
- **Professional Services**: Frappe Partner Network
- **Custom Development**: Contact project maintainers

---

Made with ❤️ for the ERPNext community