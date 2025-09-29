let calendar;
let selectedDate;
let selectedTime;

frappe.ready(() => {
    initializeCalendar();
    setupEventHandlers();
});

function initializeCalendar() {
    const calendarEl = document.getElementById('calendar');
    
    calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        selectable: true,
        selectMirror: true,
        select: function(selectionInfo) {
            // Handle date/time selection for booking
            selectedDate = selectionInfo.start;
            showAppointmentModal(selectionInfo.start);
        },
        eventClick: function(eventInfo) {
            // Show appointment details
            showAppointmentDetails(eventInfo.event);
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
                    if (response.message) {
                        successCallback(response.message);
                    } else {
                        failureCallback('Failed to load events');
                    }
                },
                error: function(error) {
                    console.error('Error loading events:', error);
                    failureCallback('Failed to load events');
                }
            });
        },
        eventDidMount: function(info) {
            // Add tooltip with appointment details
            const tooltip = `Customer: ${info.event.extendedProps.customer_name}
Email: ${info.event.extendedProps.customer_email}
Status: ${info.event.extendedProps.status}`;
            
            info.el.setAttribute('title', tooltip);
        },
        businessHours: {
            // Default business hours - can be customized
            daysOfWeek: [1, 2, 3, 4, 5], // Monday - Friday
            startTime: '09:00',
            endTime: '17:00'
        },
        slotMinTime: '08:00',
        slotMaxTime: '18:00',
        height: 'auto'
    });
    
    calendar.render();
}

function setupEventHandlers() {
    // Book appointment button
    document.getElementById('book-appointment-btn').addEventListener('click', function() {
        showAppointmentModal(new Date());
    });
    
    // Save appointment button
    document.getElementById('saveAppointment').addEventListener('click', function() {
        saveAppointment();
    });
    
    // Modal form validation
    const form = document.getElementById('appointmentForm');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        saveAppointment();
    });
}

function showAppointmentModal(date) {
    selectedDate = date;
    
    // Set the datetime input
    const datetimeInput = document.getElementById('appointmentDateTime');
    const localDate = new Date(date.getTime() - (date.getTimezoneOffset() * 60000));
    datetimeInput.value = localDate.toISOString().slice(0, 16);
    
    // Clear form
    document.getElementById('appointmentForm').reset();
    datetimeInput.value = localDate.toISOString().slice(0, 16);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('appointmentModal'));
    modal.show();
}

function saveAppointment() {
    const form = document.getElementById('appointmentForm');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const saveBtn = document.getElementById('saveAppointment');
    saveBtn.disabled = true;
    saveBtn.textContent = __('Saving...');
    
    const datetime = new Date(document.getElementById('appointmentDateTime').value);
    const dateStr = datetime.toISOString().split('T')[0];
    const timeStr = datetime.toTimeString().split(' ')[0];
    
    const appointmentData = {
        date: dateStr,
        time: timeStr,
        customer_name: document.getElementById('customerName').value,
        customer_email: document.getElementById('customerEmail').value,
        customer_phone: document.getElementById('customerPhone').value,
        customer_notes: document.getElementById('customerNotes').value,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
    };
    
    frappe.call({
        method: 'erpnext.www.booking_calendar.index.create_appointment_from_calendar',
        args: appointmentData,
        callback: function(response) {
            if (response.message) {
                frappe.show_alert({
                    message: __('Appointment booked successfully!'),
                    indicator: 'green'
                });
                
                // Close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('appointmentModal'));
                modal.hide();
                
                // Refresh calendar
                calendar.refetchEvents();
            } else {
                frappe.show_alert({
                    message: __('Failed to book appointment'),
                    indicator: 'red'
                });
            }
        },
        error: function(error) {
            console.error('Error booking appointment:', error);
            frappe.show_alert({
                message: __('Failed to book appointment'),
                indicator: 'red'
            });
        },
        always: function() {
            saveBtn.disabled = false;
            saveBtn.textContent = __('Book Appointment');
        }
    });
}

function showAppointmentDetails(event) {
    const props = event.extendedProps;
    
    const detailsHtml = `
        <div class="row">
            <div class="col-sm-4"><strong>${__('Appointment ID')}</strong></div>
            <div class="col-sm-8">${props.appointment_id}</div>
        </div>
        <div class="row mt-2">
            <div class="col-sm-4"><strong>${__('Customer Name')}</strong></div>
            <div class="col-sm-8">${props.customer_name}</div>
        </div>
        <div class="row mt-2">
            <div class="col-sm-4"><strong>${__('Email')}</strong></div>
            <div class="col-sm-8">${props.customer_email}</div>
        </div>
        <div class="row mt-2">
            <div class="col-sm-4"><strong>${__('Status')}</strong></div>
            <div class="col-sm-8">
                <span class="badge ${getStatusBadgeClass(props.status)}">${props.status}</span>
            </div>
        </div>
        <div class="row mt-2">
            <div class="col-sm-4"><strong>${__('Scheduled Time')}</strong></div>
            <div class="col-sm-8">${formatDateTime(event.start)}</div>
        </div>
        ${props.appointment_with ? `
        <div class="row mt-2">
            <div class="col-sm-4"><strong>${__('Appointment With')}</strong></div>
            <div class="col-sm-8">${props.appointment_with}</div>
        </div>` : ''}
        <div class="row mt-3">
            <div class="col-12">
                <div class="btn-group w-100" role="group">
                    <a href="/app/appointment/${props.appointment_id}" class="btn btn-primary btn-sm" target="_blank">
                        ${__('View Full Details')}
                    </a>
                    ${canManageAppointments() ? `
                    <button type="button" class="btn btn-warning btn-sm" onclick="changeAppointmentStatus('${props.appointment_id}', 'Unverified')">
                        ${__('Mark Unverified')}
                    </button>
                    <button type="button" class="btn btn-success btn-sm" onclick="changeAppointmentStatus('${props.appointment_id}', 'Open')">
                        ${__('Mark Open')}
                    </button>
                    <button type="button" class="btn btn-secondary btn-sm" onclick="changeAppointmentStatus('${props.appointment_id}', 'Closed')">
                        ${__('Mark Closed')}
                    </button>
                    ` : ''}
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('appointmentDetailsContent').innerHTML = detailsHtml;
    
    const modal = new bootstrap.Modal(document.getElementById('appointmentDetailsModal'));
    modal.show();
}

function canManageAppointments() {
    // Check if user has permission to manage appointments
    // This is a simplified check - in real implementation, this should be based on user roles
    return frappe.user && frappe.user.name !== 'Guest';
}

function changeAppointmentStatus(appointmentId, newStatus) {
    if (!canManageAppointments()) {
        frappe.show_alert({
            message: __('You do not have permission to change appointment status'),
            indicator: 'red'
        });
        return;
    }
    
    frappe.call({
        method: 'erpnext.www.booking_calendar.index.update_appointment_status',
        args: {
            appointment_name: appointmentId,
            status: newStatus
        },
        callback: function(response) {
            if (response.message && response.message.success) {
                frappe.show_alert({
                    message: response.message.message,
                    indicator: 'green'
                });
                
                // Close modal and refresh calendar
                const modal = bootstrap.Modal.getInstance(document.getElementById('appointmentDetailsModal'));
                modal.hide();
                calendar.refetchEvents();
            } else {
                frappe.show_alert({
                    message: __('Failed to update appointment status'),
                    indicator: 'red'
                });
            }
        },
        error: function(error) {
            console.error('Error updating appointment status:', error);
            frappe.show_alert({
                message: __('Failed to update appointment status'),
                indicator: 'red'
            });
        }
    });
}

function getStatusBadgeClass(status) {
    const statusMap = {
        'Open': 'bg-success',
        'Unverified': 'bg-warning text-dark',
        'Closed': 'bg-secondary'
    };
    return statusMap[status] || 'bg-primary';
}

function formatDateTime(date) {
    return new Intl.DateTimeFormat('default', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(new Date(date));
}

// Utility function for translations if not available
if (typeof __ === 'undefined') {
    window.__ = function(text) {
        return text;
    };
}