# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# Spa module fixtures

# Create default spa roles
spa_roles = [
    {
        "doctype": "Role",
        "role_name": "Spa Manager",
        "home_page": "spa-management",
        "desk_access": 1
    },
    {
        "doctype": "Role", 
        "role_name": "Spa Staff",
        "home_page": "spa-management",
        "desk_access": 1
    },
    {
        "doctype": "Role",
        "role_name": "Spa Receptionist", 
        "home_page": "spa-management",
        "desk_access": 1
    }
]

# Default spa services
default_spa_services = [
    {
        "doctype": "Spa Service",
        "naming_series": "SPA-SRV-.YYYY.-",
        "service_name": "Swedish Massage",
        "service_category": "Massage", 
        "duration_minutes": 60,
        "base_price": 800000,  # 800,000 VND
        "description": "Classic Swedish massage for relaxation"
    },
    {
        "doctype": "Spa Service",
        "naming_series": "SPA-SRV-.YYYY.-",
        "service_name": "Deep Tissue Massage",
        "service_category": "Massage",
        "duration_minutes": 90,
        "base_price": 1200000,  # 1,200,000 VND
        "description": "Therapeutic deep tissue massage"
    },
    {
        "doctype": "Spa Service", 
        "naming_series": "SPA-SRV-.YYYY.-",
        "service_name": "Anti-Aging Facial",
        "service_category": "Facial",
        "duration_minutes": 75,
        "base_price": 1500000,  # 1,500,000 VND
        "description": "Anti-aging facial treatment"
    },
    {
        "doctype": "Spa Service",
        "naming_series": "SPA-SRV-.YYYY.-", 
        "service_name": "Manicure & Pedicure",
        "service_category": "Nail Care",
        "duration_minutes": 45,
        "base_price": 600000,  # 600,000 VND
        "description": "Complete nail care service"
    },
    {
        "doctype": "Spa Service",
        "naming_series": "SPA-SRV-.YYYY.-",
        "service_name": "Hair Spa Treatment", 
        "service_category": "Hair Care",
        "duration_minutes": 60,
        "base_price": 800000,  # 800,000 VND
        "description": "Nourishing hair spa treatment"
    }
]

# Default spa rooms
default_spa_rooms = [
    {
        "doctype": "Spa Room",
        "room_name": "Massage Room 1",
        "room_code": "MR01",
        "room_type": "Individual Treatment",
        "capacity": 1,
        "floor_number": 1,
        "current_status": "Available"
    },
    {
        "doctype": "Spa Room", 
        "room_name": "Massage Room 2",
        "room_code": "MR02", 
        "room_type": "Individual Treatment",
        "capacity": 1,
        "floor_number": 1,
        "current_status": "Available"
    },
    {
        "doctype": "Spa Room",
        "room_name": "VIP Suite",
        "room_code": "VIP01",
        "room_type": "VIP Suite", 
        "capacity": 2,
        "floor_number": 2,
        "current_status": "Available",
        "amenities": "Private bathroom, mini fridge, sound system"
    },
    {
        "doctype": "Spa Room",
        "room_name": "Facial Treatment Room",
        "room_code": "FR01",
        "room_type": "Individual Treatment",
        "capacity": 1, 
        "floor_number": 1,
        "current_status": "Available"
    }
]


def create_fixtures():
    """Create default fixtures for spa module"""
    import frappe
    
    # Create roles
    for role_data in spa_roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.new_doc("Role")
            role.update(role_data)
            role.insert(ignore_permissions=True)
    
    # Create default services
    for service_data in default_spa_services:
        if not frappe.db.exists("Spa Service", {"service_name": service_data["service_name"]}):
            service = frappe.new_doc("Spa Service")
            service.update(service_data)
            service.insert(ignore_permissions=True)
    
    # Create default rooms  
    for room_data in default_spa_rooms:
        if not frappe.db.exists("Spa Room", room_data["room_name"]):
            room = frappe.new_doc("Spa Room")
            room.update(room_data)
            room.insert(ignore_permissions=True)
    
    frappe.db.commit()