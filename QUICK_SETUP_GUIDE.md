# Quick Setup Guide - Booking Calendar Features

## Prerequisites
- ERPNext v14+ installed
- Admin/System Manager permissions
- Web server access

## Quick Setup (5 minutes)

### 1. Enable Appointment Booking
```
1. Go to: Setup > Appointment Booking Settings
2. Check: "Enable Scheduling" 
3. Set Business Hours: 09:00 - 17:00
4. Select Holiday List (optional)
5. Save
```

### 2. Access Booking Calendar
```
Visit: https://your-site.com/booking_calendar
```

### 3. Test Booking Flow
```
1. Click on any date/time slot
2. Fill form:
   - Name: Test Customer
   - Email: test@example.com
   - Phone: +1234567890
3. Click "Book Appointment"
4. Verify in Appointment list
```

### 4. Setup Spa Features (Optional)
```
1. Create Spa Service:
   - Go to: Spa > Spa Service
   - Name: "60min Massage"
   - Duration: 60 minutes
   - Price: $100

2. Create Spa Room:
   - Go to: Spa > Spa Room  
   - Name: "Room A"
   - Type: "Treatment Room"

3. Test Spa Appointment:
   - Go to: Spa > Spa Appointment
   - Fill all fields and save
```

## URL Endpoints

| Feature | URL | Access Level |
|---------|-----|--------------|
| Booking Calendar | `/booking_calendar` | Public/Login Required |
| Book Appointment | `/book_appointment` | Public |
| Appointment Verify | `/book_appointment/verify` | Public |
| Spa Management | `/app/spa-appointment` | Login Required |

## Configuration Files

| Component | File Location |
|-----------|---------------|
| Calendar UI | `erpnext/www/booking_calendar/` |
| Booking Form | `erpnext/www/book_appointment/` |  
| Spa System | `erpnext/spa/doctype/` |
| Settings | `Appointment Booking Settings` doctype |

## Default Business Rules

- **Business Hours**: 9 AM - 5 PM, Monday-Friday
- **Slot Duration**: 30 minutes  
- **Advance Booking**: Up to 30 days
- **Minimum Notice**: 2 hours
- **Auto-verification**: Disabled (requires manual verification)

## Permissions Required

| Action | Role Required |
|--------|---------------|
| View Calendar | Guest (if public) or any role |
| Book Appointment | Guest |
| Manage Appointments | Appointment Manager |
| Spa Management | Spa Manager |
| System Settings | System Manager |

## Troubleshooting Checklist

- [ ] "Enable Scheduling" is checked
- [ ] Business Hours are configured  
- [ ] Holiday List exists and is selected
- [ ] User has proper permissions
- [ ] JavaScript console shows no errors
- [ ] API endpoints are accessible

## Next Steps

1. **Customize Colors**: Edit `booking_calendar/index.css`
2. **Add Business Logic**: Extend `booking_calendar/index.py`
3. **Setup Notifications**: Configure Email/SMS templates
4. **Integration**: Use APIs for external systems
5. **Mobile App**: Use Frappe mobile framework

## Support

- **Documentation**: Check ERPNext docs
- **Community**: ERPNext Community Forum
- **Issues**: GitHub repository
- **Professional**: Frappe Partner Network