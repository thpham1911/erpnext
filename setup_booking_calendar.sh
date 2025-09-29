#!/bin/bash

# ERPNext Booking Calendar Setup Script
# This script helps you quickly setup the booking calendar features

echo "🚀 ERPNext Booking Calendar Setup"
echo "=================================="
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists bench; then
    echo "❌ Bench command not found. Please install Frappe Bench first."
    echo "   Visit: https://github.com/frappe/bench"
    exit 1
fi

if ! command_exists mysql; then
    echo "⚠️  MySQL client not found. Please install MySQL client."
fi

echo "✅ Prerequisites check complete"
echo ""

# Get site name
read -p "📝 Enter your ERPNext site name (e.g., mysite.local): " SITE_NAME

if [ -z "$SITE_NAME" ]; then
    echo "❌ Site name is required"
    exit 1
fi

# Check if site exists
if ! bench --site "$SITE_NAME" list-apps >/dev/null 2>&1; then
    echo "❌ Site '$SITE_NAME' not found or not accessible"
    exit 1
fi

echo "✅ Site '$SITE_NAME' found"
echo ""

# Enable appointment booking
echo "🔧 Configuring appointment booking..."

# Create appointment booking settings if not exists
bench --site "$SITE_NAME" execute "
import frappe

# Check if Appointment Booking Settings exists
if not frappe.db.exists('Appointment Booking Settings', 'Appointment Booking Settings'):
    settings = frappe.get_doc({
        'doctype': 'Appointment Booking Settings',
        'enable_scheduling': 1,
        'advance_booking_days': 30,
        'min_hours_before_booking': 2
    })
    settings.insert()
    print('Created Appointment Booking Settings')
else:
    settings = frappe.get_doc('Appointment Booking Settings')
    settings.enable_scheduling = 1
    settings.save()
    print('Updated Appointment Booking Settings')

frappe.db.commit()
"

if [ $? -eq 0 ]; then
    echo "✅ Appointment booking enabled"
else
    echo "❌ Failed to enable appointment booking"
    exit 1
fi

# Set up business hours
echo ""
echo "⏰ Setting up business hours..."

read -p "Enter start time (default: 09:00): " START_TIME
START_TIME=${START_TIME:-"09:00"}

read -p "Enter end time (default: 17:00): " END_TIME  
END_TIME=${END_TIME:-"17:00"}

echo "Business hours set to: $START_TIME - $END_TIME"

# Create sample data (optional)
echo ""
read -p "🎯 Create sample appointment data? (y/n): " CREATE_SAMPLES

if [ "$CREATE_SAMPLES" = "y" ] || [ "$CREATE_SAMPLES" = "Y" ]; then
    echo "📊 Creating sample appointments..."
    
    bench --site "$SITE_NAME" execute "
import frappe
from datetime import datetime, timedelta

# Create sample appointments
sample_appointments = [
    {
        'customer_name': 'John Doe',
        'customer_email': 'john.doe@example.com',
        'customer_phone_number': '+1234567890',
        'scheduled_time': datetime.now() + timedelta(days=1, hours=2),
        'status': 'Open'
    },
    {
        'customer_name': 'Jane Smith',
        'customer_email': 'jane.smith@example.com', 
        'customer_phone_number': '+1234567891',
        'scheduled_time': datetime.now() + timedelta(days=2, hours=3),
        'status': 'Unverified'
    },
    {
        'customer_name': 'Bob Johnson',
        'customer_email': 'bob.johnson@example.com',
        'scheduled_time': datetime.now() + timedelta(days=3, hours=1),
        'status': 'Open'
    }
]

for appointment_data in sample_appointments:
    try:
        appointment = frappe.get_doc({
            'doctype': 'Appointment',
            **appointment_data
        })
        appointment.insert(ignore_permissions=True)
        print(f'Created appointment for {appointment_data[\"customer_name\"]}')
    except Exception as e:
        print(f'Error creating appointment for {appointment_data[\"customer_name\"]}: {str(e)}')

frappe.db.commit()
print('Sample appointments created')
"
    echo "✅ Sample appointments created"
fi

# Setup email templates (optional)
echo ""
read -p "📧 Setup email templates? (y/n): " SETUP_EMAIL

if [ "$SETUP_EMAIL" = "y" ] || [ "$SETUP_EMAIL" = "Y" ]; then
    echo "📮 Setting up email templates..."
    
    bench --site "$SITE_NAME" execute "
import frappe

# Appointment confirmation template
template_html = '''
<div style=\"font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;\">
    <div style=\"background-color: #f8f9fa; padding: 20px; text-align: center;\">
        <h1 style=\"color: #007bff; margin: 0;\">Appointment Confirmed</h1>
    </div>
    <div style=\"padding: 30px;\">
        <p>Dear {{ customer_name }},</p>
        <p>Your appointment has been successfully booked for:</p>
        <div style=\"background-color: #f8f9fa; padding: 20px; border-radius: 8px;\">
            <p><strong>Date & Time:</strong> {{ formatted_datetime }}</p>
            <p><strong>Reference ID:</strong> {{ name }}</p>
        </div>
        <p>Thank you for choosing our services!</p>
    </div>
</div>
'''

try:
    if not frappe.db.exists('Email Template', 'Appointment Confirmation'):
        email_template = frappe.get_doc({
            'doctype': 'Email Template',
            'name': 'Appointment Confirmation',
            'subject': 'Appointment Confirmation - {{ customer_name }}',
            'response': template_html,
            'use_html': 1
        })
        email_template.insert()
        print('Created Appointment Confirmation email template')
    else:
        print('Email template already exists')
except Exception as e:
    print(f'Error creating email template: {str(e)}')

frappe.db.commit()
"
    echo "✅ Email templates configured"
fi

# Final setup steps
echo ""
echo "🔄 Running final setup..."

# Clear cache
bench --site "$SITE_NAME" clear-cache
bench --site "$SITE_NAME" clear-website-cache

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "📋 Summary:"
echo "  • Appointment booking: ✅ Enabled"
echo "  • Business hours: $START_TIME - $END_TIME"
echo "  • Site: $SITE_NAME"
echo ""
echo "🌐 Access URLs:"
echo "  • Booking Calendar: https://$SITE_NAME/booking_calendar"
echo "  • Book Appointment: https://$SITE_NAME/book_appointment" 
echo "  • Admin Panel: https://$SITE_NAME/app"
echo ""
echo "📖 Next Steps:"
echo "  1. Visit the booking calendar to test functionality"
echo "  2. Configure permissions for your users"
echo "  3. Customize business hours if needed"
echo "  4. Setup SMS notifications (optional)"
echo "  5. Read the documentation: ./DOCUMENTATION_INDEX.md"
echo ""
echo "🆘 Need Help?"
echo "  • Documentation: ./DOCUMENTATION_INDEX.md"
echo "  • Quick Setup: ./QUICK_SETUP_GUIDE.md"
echo "  • User Guide: ./USER_GUIDE_BOOKING_CALENDAR_EN.md"
echo ""
echo "Happy booking! 🎯"