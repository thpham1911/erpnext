frappe.ready(() => {
    loadServices();
    setupEventListeners();
});

function setupEventListeners() {
    // Tab switching event handlers
    document.querySelectorAll('#spa-nav .nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            const targetTab = this.getAttribute('href').substring(1);
            
            switch(targetTab) {
                case 'services':
                    loadServices();
                    break;
                case 'rooms':
                    loadRooms();
                    break;
                case 'appointments':
                    loadAppointments();
                    break;
            }
        });
    });
}

function loadServices() {
    const container = document.getElementById('services-container');
    
    frappe.call({
        method: 'erpnext.www.spa.index.get_spa_services',
        callback: function(response) {
            if (response.message && response.message.length > 0) {
                displayServices(response.message, container);
            } else {
                container.innerHTML = `
                    <div class="text-center text-muted">
                        <p>${__('No spa services found.')}</p>
                        <p class="small">${__('Services will be displayed here once they are created.')}</p>
                    </div>
                `;
            }
        },
        error: function(error) {
            console.error('Error loading services:', error);
            container.innerHTML = `
                <div class="alert alert-warning" role="alert">
                    ${__('Unable to load spa services. Please try again later.')}
                </div>
            `;
        }
    });
}

function displayServices(services, container) {
    let html = '<div class="row">';
    
    const servicesByCategory = {};
    services.forEach(service => {
        const category = service.service_category || 'Other';
        if (!servicesByCategory[category]) {
            servicesByCategory[category] = [];
        }
        servicesByCategory[category].push(service);
    });
    
    Object.keys(servicesByCategory).forEach(category => {
        html += `
            <div class="col-lg-6 mb-4">
                <h6 class="text-primary mb-3">${category}</h6>
                <div class="list-group">
        `;
        
        servicesByCategory[category].forEach(service => {
            const price = service.base_price ? 
                new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(service.base_price) : 
                __('Contact for pricing');
                
            html += `
                <div class="list-group-item">
                    <div class="d-flex w-100 justify-content-between">
                        <h6 class="mb-1">${service.service_name}</h6>
                        <small class="text-success font-weight-bold">${price}</small>
                    </div>
                    <p class="mb-1 text-muted small">${service.description || ''}</p>
                    <small class="text-muted">${__('Duration')}: ${service.duration_minutes || 0} ${__('minutes')}</small>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

function loadRooms() {
    const container = document.getElementById('rooms-container');
    
    frappe.call({
        method: 'erpnext.www.spa.index.get_spa_rooms',
        callback: function(response) {
            if (response.message && response.message.length > 0) {
                displayRooms(response.message, container);
            } else {
                container.innerHTML = `
                    <div class="text-center text-muted">
                        <p>${__('No spa rooms found.')}</p>
                        <p class="small">${__('Rooms will be displayed here once they are created.')}</p>
                    </div>
                `;
            }
        },
        error: function(error) {
            console.error('Error loading rooms:', error);
            container.innerHTML = `
                <div class="alert alert-warning" role="alert">
                    ${__('Unable to load spa rooms. Please try again later.')}
                </div>
            `;
        }
    });
}

function displayRooms(rooms, container) {
    let html = '<div class="row">';
    
    rooms.forEach(room => {
        const statusClass = room.current_status === 'Available' ? 'success' : 
                           room.current_status === 'Occupied' ? 'danger' : 'warning';
        
        html += `
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h6 class="card-title d-flex justify-content-between">
                            ${room.room_name}
                            <span class="badge bg-${statusClass}">${room.current_status}</span>
                        </h6>
                        <p class="card-text">
                            <small class="text-muted">${__('Code')}: ${room.room_code}</small><br>
                            <small class="text-muted">${__('Type')}: ${room.room_type}</small><br>
                            <small class="text-muted">${__('Capacity')}: ${room.capacity} ${__('person(s)')}</small>
                        </p>
                        ${room.amenities ? `<p class="card-text small"><strong>${__('Amenities')}:</strong> ${room.amenities}</p>` : ''}
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

function loadAppointments() {
    const container = document.getElementById('appointments-container');
    
    // Get today and next 30 days
    const today = new Date();
    const nextMonth = new Date();
    nextMonth.setDate(today.getDate() + 30);
    
    frappe.call({
        method: 'erpnext.www.spa.index.get_spa_appointments',
        args: {
            start: today.toISOString().split('T')[0],
            end: nextMonth.toISOString().split('T')[0]
        },
        callback: function(response) {
            if (response.message && response.message.length > 0) {
                displayAppointments(response.message, container);
            } else {
                container.innerHTML = `
                    <div class="text-center text-muted">
                        <p>${__('No appointments found.')}</p>
                        <p class="small">${__('Recent appointments will be displayed here.')}</p>
                    </div>
                `;
            }
        },
        error: function(error) {
            console.error('Error loading appointments:', error);
            container.innerHTML = `
                <div class="alert alert-warning" role="alert">
                    ${__('Unable to load appointments. Please try again later.')}
                </div>
            `;
        }
    });
}

function displayAppointments(appointments, container) {
    let html = `
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>${__('Date')}</th>
                        <th>${__('Time')}</th>
                        <th>${__('Customer')}</th>
                        <th>${__('Service')}</th>
                        <th>${__('Room')}</th>
                        <th>${__('Status')}</th>
                        <th>${__('Amount')}</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    appointments.forEach(appointment => {
        const statusClass = appointment.status === 'Confirmed' ? 'success' : 
                           appointment.status === 'Cancelled' ? 'danger' : 'warning';
        
        const amount = appointment.total_amount ? 
            new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(appointment.total_amount) : 
            '-';
            
        html += `
            <tr>
                <td>${formatDate(appointment.appointment_date)}</td>
                <td>${appointment.start_time} - ${appointment.end_time}</td>
                <td>${appointment.customer}</td>
                <td>${appointment.service || '-'}</td>
                <td>${appointment.room || '-'}</td>
                <td><span class="badge bg-${statusClass}">${appointment.status}</span></td>
                <td>${amount}</td>
            </tr>
        `;
    });
    
    html += `
                </tbody>
            </table>
        </div>
    `;
    
    container.innerHTML = html;
}

function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

// Utility function for translations if not available
if (typeof __ === 'undefined') {
    window.__ = function(text) {
        return text;
    };
}