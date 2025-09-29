# Hướng Dẫn Sử Dụng Tính Năng Booking Calendar và Appointment

## Tổng Quan

ERPNext đã được tích hợp các tính năng đặt lịch hẹn và quản lý appointment hiện đại, bao gồm:

1. **Booking Calendar UI** - Giao diện lịch tương tác để xem và đặt lịch hẹn
2. **Book Appointment System** - Hệ thống đặt lịch hẹn truyền thống 
3. **Spa Management System** - Quản lý lịch hẹn spa và dịch vụ chuyên nghiệp

---

## 1. Booking Calendar UI

### Mục đích
Giao diện lịch hiện đại sử dụng FullCalendar để hiển thị và quản lý các cuộc hẹn một cách trực quan.

### Cách truy cập
- URL: `https://your-domain.com/booking_calendar`
- Menu: Truy cập trực tiếp qua đường dẫn hoặc tích hợp vào menu chính

### Tính năng chính

#### 1.1 Xem Lịch Hẹn
- **Hiển thị lịch**: Lịch hiển thị theo tháng, tuần, hoặc ngày
- **Màu sắc phân loại**:
  - 🟢 **Xanh lá**: Lịch hẹn đã mở (Open)
  - 🟡 **Vàng**: Lịch hẹn chưa xác nhận (Unverified) 
  - ⚫ **Xám**: Lịch hẹn đã đóng (Closed)

#### 1.2 Đặt Lịch Hẹn Mới
**Cách 1: Click vào ngày/giờ trên lịch**
1. Click vào slot thời gian mong muốn trên lịch
2. Popup đặt lịch sẽ xuất hiện
3. Điền thông tin:
   - **Ngày & Giờ**: Tự động điền từ slot đã chọn
   - **Tên khách hàng**: Bắt buộc
   - **Email**: Bắt buộc
   - **Số điện thoại**: Tùy chọn
   - **Ghi chú**: Tùy chọn
4. Click "Book Appointment" để xác nhận

**Cách 2: Sử dụng nút "Book New Appointment"**
1. Click nút "Book New Appointment" ở sidebar
2. Làm theo các bước tương tự như cách 1

#### 1.3 Xem Chi Tiết Lịch Hẹn
1. Click vào một lịch hẹn đã tồn tại trên lịch
2. Popup chi tiết sẽ hiển thị:
   - Thông tin khách hàng
   - Thời gian hẹn
   - Trạng thái hiện tại
   - Các nút quản lý (nếu có quyền)

#### 1.4 Quản Lý Trạng Thái (Dành cho Admin)
Nếu có quyền quản lý, bạn có thể:
- **Mark Unverified**: Đánh dấu chưa xác nhận
- **Mark Open**: Đánh dấu mở
- **Mark Closed**: Đánh dấu đóng

### Cài Đặt và Cấu Hình

#### Kích hoạt tính năng
1. Truy cập **Appointment Booking Settings**
2. Bật "Enable Scheduling"
3. Cấu hình giờ làm việc (mặc định: 9:00-17:00, Thứ 2-6)

#### Tùy chỉnh giao diện
- File CSS: `erpnext/www/booking_calendar/index.css`
- File JS: `erpnext/www/booking_calendar/index.js`
- File HTML: `erpnext/www/booking_calendar/index.html`

---

## 2. Book Appointment System

### Mục đích
Hệ thống đặt lịch hẹn truyền thống với form step-by-step, phù hợp cho khách hàng bên ngoài.

### Cách truy cập
- URL: `https://your-domain.com/book_appointment`
- Thường được nhúng vào website hoặc chia sẻ link công khai

### Quy trình đặt lịch

#### Bước 1: Chọn Ngày và Múi Giờ
1. Chọn ngày mong muốn
2. Chọn múi giờ phù hợp
3. Hệ thống sẽ hiển thị các slot thời gian có sẵn

#### Bước 2: Chọn Thời Gian
1. Xem các slot thời gian khả dụng
2. Click chọn slot phù hợp
3. Click "Next" để tiếp tục

#### Bước 3: Điền Thông Tin
1. **Tên**: Bắt buộc
2. **Số điện thoại**: Tùy chọn
3. **Email**: Bắt buộc
4. **Skype**: Tùy chọn (cho cuộc hẹn online)
5. **Ghi chú**: Mô tả chi tiết về cuộc hẹn

#### Bước 4: Xác Nhận
1. Review thông tin đã nhập
2. Click "Book Appointment"
3. Hệ thống sẽ gửi email xác nhận

### Tính năng nâng cao

#### Tự động phân loại khách hàng
- Hệ thống tự động tìm kiếm Lead hoặc Customer hiện tại
- Tạo mới nếu chưa tồn tại
- Liên kết appointment với đúng contact

#### Xác thực email
- URL xác thực: `https://your-domain.com/book_appointment/verify`
- Email tự động gửi link xác thực
- Trạng thái chuyển từ "Unverified" sang "Open"

---

## 3. Spa Management System

### Mục đích  
Hệ thống quản lý lịch hẹn spa chuyên nghiệp với đầy đủ tính năng quản lý dịch vụ, nhân viên và thanh toán.

### Các DocType chính

#### 3.1 Spa Service
**Mục đích**: Quản lý các dịch vụ spa
**Thông tin chính**:
- Tên dịch vụ
- Mô tả
- Thời gian (phút)
- Giá cả
- Danh mục

#### 3.2 Spa Room
**Mục đích**: Quản lý phòng spa
**Thông tin chính**:
- Tên phòng
- Loại phòng
- Tình trạng
- Mô tả

#### 3.3 Spa Appointment
**Mục đích**: Lịch hẹn spa chi tiết
**Thông tin chính**:
- Khách hàng
- Dịch vụ
- Nhân viên phụ trách
- Phòng
- Thời gian
- Trạng thái
- Giá cuối cùng

### Quy trình sử dụng

#### Cài đặt ban đầu
1. **Tạo Spa Services**:
   - Vào "Spa Service" doctype
   - Tạo các dịch vụ: massage, facial, manicure, etc.
   - Cài đặt thời gian và giá

2. **Tạo Spa Rooms**:
   - Vào "Spa Room" doctype
   - Tạo các phòng spa
   - Phân loại theo dịch vụ

3. **Cài đặt Staff**:
   - Tạo User cho nhân viên
   - Phân quyền phù hợp

#### Tạo lịch hẹn spa
1. **Thông tin cơ bản**:
   - Customer: Chọn hoặc tạo mới
   - Service: Chọn dịch vụ spa
   - Date & Time: Chọn thời gian

2. **Phân công**:
   - Assigned Staff: Chọn nhân viên
   - Room: Chọn phòng (tùy chọn)

3. **Xác nhận và thanh toán**:
   - Review thông tin
   - Tự động tạo Sales Invoice
   - Theo dõi trạng thái

### Quản lý trạng thái

#### Các trạng thái chính:
- **Scheduled**: Đã lên lịch
- **Confirmed**: Đã xác nhận  
- **In Progress**: Đang thực hiện
- **Completed**: Hoàn thành
- **Cancelled**: Đã hủy

#### Workflow tự động:
1. **Scheduled → Confirmed**: Gửi SMS/Email xác nhận
2. **Confirmed → In Progress**: Bắt đầu dịch vụ
3. **In Progress → Completed**: Tự động tạo invoice, lưu lịch sử
4. **Any → Cancelled**: Ghi nhận thời gian hủy

### API và tích hợp

#### Lấy slot thời gian khả dụng
```python
# Gọi API
frappe.call({
    method: 'erpnext.spa.doctype.spa_appointment.spa_appointment.get_available_time_slots',
    args: {
        date: '2024-01-15',
        service: 'Massage Service',
        staff: 'staff@example.com'  // optional
    }
})
```

#### Tạo lịch hẹn qua API  
```python
# Tạo appointment mới
appointment = frappe.new_doc('Spa Appointment')
appointment.customer = 'Customer Name'
appointment.spa_service = 'Service Name'  
appointment.appointment_date = '2024-01-15'
appointment.appointment_time = '10:00:00'
appointment.assigned_staff = 'staff@example.com'
appointment.insert()
```

---

## 4. Tích Hợp và Tùy Chỉnh

### Tích hợp với calendar system
Tất cả các appointment từ 3 hệ thống đều xuất hiện trong:
- Desktop Calendar app
- Mobile calendar sync
- Booking Calendar UI

### Tùy chỉnh giao diện
```css
/* Tùy chỉnh màu sắc trong booking_calendar/index.css */
.fc-event.status-open {
    background-color: #28a745 !important;
}

.fc-event.status-unverified {
    background-color: #ffc107 !important;
}
```

### Webhook và notifications
```python
# Hook sau khi tạo appointment
def after_insert(self):
    # Gửi notification
    self.send_notifications_if_needed()
    
    # Webhook to external systems
    if self.status == 'Confirmed':
        send_webhook_notification(self)
```

---

## 5. Troubleshooting

### Các lỗi thường gặp

#### Lỗi: "Appointment Scheduling Disabled"
**Nguyên nhân**: Chưa bật tính năng trong settings
**Giải pháp**: 
1. Vào "Appointment Booking Settings"
2. Check "Enable Scheduling"

#### Lỗi: "No time slots available"  
**Nguyên nhân**: Cấu hình giờ làm việc hoặc holiday list
**Giải pháp**:
1. Kiểm tra Business Hours trong calendar settings
2. Kiểm tra Holiday List
3. Đảm bảo không có conflict với existing appointments

#### Calendar không hiển thị events
**Nguyên nhân**: Lỗi JavaScript hoặc quyền truy cập
**Giải pháp**:
1. Check browser console cho lỗi JS
2. Kiểm tra user permissions cho Appointment doctype
3. Verify API endpoints đang hoạt động

### Performance optimization
```python
# Thêm index cho queries nhanh hơn
frappe.db.add_index("Appointment", ["scheduled_time", "status"])
frappe.db.add_index("Spa Appointment", ["appointment_date", "assigned_staff"])
```

---

## 6. Kết Luận

Hệ thống booking calendar và appointment của ERPNext cung cấp:

✅ **3 giao diện linh hoạt** cho các use case khác nhau
✅ **Tự động hóa workflow** từ booking đến billing  
✅ **API đầy đủ** cho tích hợp external
✅ **Mobile responsive** cho mọi thiết bị
✅ **Multi-timezone support** cho khách hàng quốc tế
✅ **Permission system** bảo mật theo role

Hệ thống phù hợp cho:
- **Spa & Wellness centers**
- **Medical clinics**  
- **Consultancy services**
- **Any appointment-based business**

Để được hỗ trợ thêm, vui lòng liên hệ team phát triển hoặc tham khảo ERPNext documentation.