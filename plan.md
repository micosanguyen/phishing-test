# Kế hoạch Dự án: PhishGuard - Hệ thống Kiểm tra Nhận thức Phishing

## Tổng quan

Xây dựng website đào tạo nhận thức an toàn thông tin cho khối tài chính. Người dùng trả lời các câu hỏi về kịch bản phishing theo trình tự, xem giải thích sau mỗi câu. Admin quản lý ngân hàng câu hỏi và xem thống kê kết quả.

---

## Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| Backend | Python 3 + Flask |
| Database | SQLite (via Flask-SQLAlchemy) |
| Frontend | HTML5 + Bootstrap 5 + Vanilla JS |
| HTML Editor | CodeMirror 5 (CDN) |
| Auth Admin | Secret Key (session cookie) |
| Upload ảnh | Werkzeug secure_filename |

---

## Cấu trúc dự án

```
phishing-test/
├── app.py                    # Flask app, toàn bộ routes
├── models.py                 # ORM models: Question, TestSession, TestAnswer
├── database.py               # Khởi tạo DB + seed 5 câu hỏi mẫu
├── config.py                 # Cấu hình: ADMIN_KEY, SECRET_KEY, EXAM_SIZE
├── requirements.txt          # Flask, Flask-SQLAlchemy, Werkzeug
├── plan.md                   # File này
├── README.md                 # Hướng dẫn sử dụng
├── static/
│   └── css/style.css         # Stylesheet chung
├── templates/
│   ├── base.html             # Layout chung (navbar, flash messages, footer)
│   ├── index.html            # Trang chủ: nhập tên + email
│   ├── test.html             # Trang làm bài: câu hỏi + nút trả lời + feedback
│   ├── result.html           # Trang kết quả: điểm + chi tiết từng câu
│   └── admin/
│       ├── base_admin.html   # Layout admin (navbar riêng)
│       ├── login.html        # Đăng nhập admin bằng key
│       ├── dashboard.html    # Thống kê + danh sách lượt thi
│       ├── questions.html    # Danh sách câu hỏi
│       ├── question_form.html # Form thêm/sửa câu hỏi (CodeMirror editor)
│       └── import.html       # Import CSV / JSON
└── uploads/                  # Hình ảnh đính kèm câu hỏi
```

---

## Database Schema

### Bảng `questions`

| Cột | Kiểu | Mô tả |
|---|---|---|
| id | Integer PK | |
| title | String(200) | Tên câu hỏi (hiển thị trong admin) |
| scenario_type | String(20) | `email` / `link` / `image` / `text` |
| content | Text | Nội dung HTML kịch bản |
| image_path | String nullable | Tên file ảnh trong /uploads |
| is_phishing | Boolean | Đáp án đúng |
| explanation | Text | Giải thích hiển thị sau khi trả lời |
| created_at | DateTime | |
| active | Boolean | Có trong pool thi hay không |

### Bảng `test_sessions`

| Cột | Kiểu | Mô tả |
|---|---|---|
| id | String(36) | UUID — session token |
| user_name | String(100) | Họ tên người dùng |
| user_email | String(200) | Email người dùng |
| question_ids | Text | JSON array thứ tự câu hỏi |
| current_index | Integer | Câu đang làm |
| score | Integer | Số câu đúng tích lũy |
| started_at | DateTime | |
| completed_at | DateTime nullable | Null nếu chưa hoàn thành |

### Bảng `test_answers`

| Cột | Kiểu | Mô tả |
|---|---|---|
| id | Integer PK | |
| session_id | FK → test_sessions | |
| question_id | FK → questions | |
| user_answer | Boolean | True=Phishing, False=Hợp lệ |
| is_correct | Boolean | |
| answered_at | DateTime | |

---

## Luồng xử lý

### Luồng người dùng

```
/ (index)
  └─[POST /start]──> Tạo TestSession (chọn N câu ngẫu nhiên từ pool)
                      └─[redirect]──> /test/<id>/q/0
                                        └─[POST AJAX /submit]──> Trả về {correct, explanation, next_url}
                                                                    └─[click Tiếp theo]──> /test/<id>/q/1
                                                                                            └─ ... /q/N-1
                                                                                                   └─ /test/<id>/result
```

### Luồng admin

```
/admin/login  ──[key đúng]──> session["admin_logged_in"] = True
/admin/       ──> Dashboard (thống kê + 50 lượt thi gần nhất)
/admin/questions ──> Danh sách + toggle/edit/delete
/admin/questions/add  ──> Form + CodeMirror editor
/admin/questions/import ──> CSV hoặc JSON paste
/admin/settings (POST) ──> Cập nhật số câu/bài vào Flask session
```

---

## Milestone

### Milestone 1 — Admin Interface ✅

- [x] Đăng nhập bằng secret key
- [x] Tạo / sửa / xóa / ẩn câu hỏi
- [x] HTML editor (CodeMirror) với syntax highlighting
- [x] Preview kịch bản trong iframe sandbox
- [x] 3 snippet template: Email / Link / Popup
- [x] Upload hình ảnh đính kèm
- [x] Cài đặt số câu/bài: 5 / 10 / 15 / 20
- [x] Dashboard: tổng lượt thi, điểm TB, tỉ lệ đạt
- [x] Import từ CSV và JSON

### Milestone 2 — User Test Interface ✅

- [x] Form nhập họ tên + email
- [x] Bắt đầu bài thi (chọn ngẫu nhiên N câu từ pool active)
- [x] Hiển thị câu hỏi tuần tự với progress bar
- [x] Submit từng câu bằng AJAX (không reload trang)
- [x] Hiện feedback màu (đúng/sai) + giải thích
- [x] Mở nút Tiếp theo sau khi xem giải thích
- [x] Trang kết quả: điểm, đạt/chưa đạt, chi tiết từng câu

---

## Hướng phát triển tiếp theo (Backlog)

### Tính năng có thể thêm

| # | Tính năng | Ưu tiên |
|---|---|---|
| 1 | Export kết quả ra Excel/CSV cho admin | Cao |
| 2 | Thêm thể loại câu hỏi: SMS, QR code | Trung bình |
| 3 | Hiển thị leaderboard / ranking | Thấp |
| 4 | Gửi email báo cáo kết quả cho người dùng | Trung bình |
| 5 | Phân tích câu hỏi nào bị sai nhiều nhất | Cao |
| 6 | Đặt thời gian giới hạn cho bài thi | Trung bình |
| 7 | Hỗ trợ multi-language (EN/VI) | Thấp |
| 8 | Đa quản trị viên với phân quyền | Thấp |
| 9 | AI tự động gợi ý/tạo kịch bản phishing | Thấp |
| 10 | API endpoint để tích hợp với hệ thống HR | Thấp |

### Cải thiện bảo mật

- Thêm rate limiting cho endpoint `/start` và `/admin/login`
- CSRF protection cho các form POST
- Thêm Content Security Policy header
- Migrate sang PostgreSQL cho môi trường production

---

## Cách chạy

```bash
# Cài dependencies
python -m pip install -r requirements.txt

# Chạy
python app.py
```

Truy cập `http://localhost:5000` — DB tự tạo và seed 5 câu hỏi mẫu khi lần đầu chạy.
