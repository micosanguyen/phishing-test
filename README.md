# PhishGuard — Hệ thống Kiểm tra Nhận thức Phishing

Ứng dụng web đào tạo nhận thức an toàn thông tin cho khối tài chính. Người dùng thực hành nhận biết các kịch bản tấn công giả mạo (phishing) thông qua bài kiểm tra tương tác.

---

## Tính năng

### Người dùng
- Nhập họ tên và email để bắt đầu bài thi
- Nhận bộ câu hỏi ngẫu nhiên từ ngân hàng đề
- Mỗi câu hỏi hiển thị kịch bản thực tế (email giả, link độc hại, popup lừa đảo…)
- Chọn **Phishing** hoặc **Hợp lệ** — xem ngay đáp án và giải thích trước khi sang câu tiếp
- Xem kết quả cuối bài: điểm, trạng thái đạt/chưa đạt, chi tiết từng câu

### Admin
- Đăng nhập bằng secret key
- Soạn kịch bản phishing bằng **HTML editor** (CodeMirror) với xem trước trực tiếp
- Quản lý ngân hàng câu hỏi: thêm, sửa, xóa, ẩn/hiện
- Import hàng loạt câu hỏi từ file **CSV** hoặc **JSON**
- Cài đặt số câu hỏi mỗi bài thi (5 / 10 / 15 / 20)
- Xem thống kê: tổng lượt thi, điểm trung bình, tỉ lệ đạt

---

## Yêu cầu hệ thống

- Python 3.8+
- pip
- Git

---

## Cài đặt trên macOS

```bash
# 1. Clone repository
git clone https://github.com/micosanguyen/phishing-test.git
cd phishing-test

# 2. Tạo môi trường ảo
python3 -m venv venv
source venv/bin/activate

# 3. Cài dependencies
pip install -r requirements.txt

# 4. Tạo file cấu hình
cp .env.example .env
```

Mở file `.env` và điền giá trị thực:

```
ADMIN_KEY=mat-khau-admin-cua-ban
SECRET_KEY=mot-chuoi-bi-mat-ngau-nhien
EXAM_SIZE=10
```

```bash
# 5. Chạy ứng dụng
python app.py
```

Mở trình duyệt tại: **http://localhost:5000**

Lần đầu chạy, hệ thống tự tạo database và thêm 5 câu hỏi mẫu.

> **Lưu ý macOS:** Nếu máy chưa có Python 3, cài đặt qua [Homebrew](https://brew.sh):
> ```bash
> brew install python
> ```

---

## Cài đặt trên Windows

```cmd
# 1. Clone repository
git clone https://github.com/micosanguyen/phishing-test.git
cd phishing-test

# 2. Tạo môi trường ảo
python -m venv venv
venv\Scripts\activate

# 3. Cài dependencies
pip install -r requirements.txt

# 4. Tạo file cấu hình
copy .env.example .env
```

Mở file `.env` và điền giá trị thực, sau đó:

```cmd
# 5. Chạy ứng dụng
python app.py
```

> **Lưu ý Windows (PowerShell):** Nếu gặp lỗi `cannot be loaded because running scripts is disabled`, chạy lệnh sau rồi kích hoạt lại venv:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

---

## Cấu hình

Tất cả cấu hình được đặt trong file `.env` (tạo từ `.env.example`):

| Biến | Mô tả |
|---|---|
| `ADMIN_KEY` | Khóa đăng nhập admin |
| `SECRET_KEY` | Khóa bảo mật Flask session (đặt giá trị ngẫu nhiên dài) |
| `EXAM_SIZE` | Số câu hỏi mặc định mỗi bài thi (mặc định: `10`) |

---

## Hướng dẫn sử dụng

### Dành cho người dùng

1. Truy cập `http://localhost:5000`
2. Nhập **Họ và tên** và **Email công ty**
3. Nhấn **Bắt đầu kiểm tra**
4. Với mỗi câu hỏi:
   - Đọc kịch bản được hiển thị
   - Nhấn **Phishing** hoặc **Hợp lệ**
   - Xem kết quả và giải thích
   - Nhấn **Tiếp theo** để sang câu kế tiếp
5. Xem điểm kết quả sau khi hoàn thành tất cả câu hỏi

Điểm đạt yêu cầu: **≥ 70%**

---

### Dành cho Admin

#### Đăng nhập

Truy cập `http://localhost:5000/admin/login` và nhập Admin Key.

#### Thêm câu hỏi mới

1. Vào **Câu hỏi** → **Thêm câu hỏi**
2. Điền tiêu đề và chọn loại kịch bản
3. Soạn nội dung HTML trong editor — nhấn **Preview** để xem trước
4. Có thể dùng các snippet có sẵn: **Email template**, **Link template**, **Popup template**
5. Chọn đáp án đúng và điền giải thích
6. Nhấn **Thêm câu hỏi**

#### Import hàng loạt từ CSV

Tạo file CSV với các cột sau:

```
title,type,content,is_phishing,explanation
```

| Cột | Giá trị hợp lệ |
|---|---|
| `type` | `email` / `link` / `image` / `text` |
| `is_phishing` | `true` / `false` |

**Ví dụ:**
```csv
title,type,content,is_phishing,explanation
Email giả ngân hàng,email,"<div>Nội dung HTML...</div>",true,"Dấu hiệu nhận biết..."
Thông báo IT hợp lệ,text,"<div>Nội dung HTML...</div>",false,"Đây là hợp lệ vì..."
```

Vào **Import** → tải file CSV lên.

#### Import từ JSON

Vào **Import** → dán JSON array vào ô văn bản:

```json
[
  {
    "title": "Tên câu hỏi",
    "type": "email",
    "content": "<div>Nội dung HTML kịch bản</div>",
    "is_phishing": true,
    "explanation": "Giải thích tại sao đây là phishing..."
  }
]
```

#### Cài đặt số câu/bài thi

Trên Dashboard → chọn số câu (5 / 10 / 15 / 20) → nhấn **Lưu**.

---

## Cấu trúc thư mục

```
phishing-test/
├── app.py               # Ứng dụng Flask chính
├── models.py            # Định nghĩa database
├── database.py          # Khởi tạo DB và dữ liệu mẫu
├── config.py            # Cấu hình
├── requirements.txt     # Thư viện Python
├── plan.md              # Kế hoạch dự án
├── README.md            # File này
├── static/css/          # CSS
├── templates/           # HTML templates
│   ├── index.html       # Trang đăng ký thi
│   ├── test.html        # Trang làm bài
│   ├── result.html      # Trang kết quả
│   └── admin/           # Giao diện quản trị
└── uploads/             # Hình ảnh đính kèm câu hỏi
```

---

## Loại kịch bản hỗ trợ

| Loại | Mô tả | Ví dụ |
|---|---|---|
| `email` | Email giả mạo tổ chức | Email ngân hàng giả yêu cầu xác minh |
| `link` | Đường dẫn độc hại | Link rút gọn dẫn đến trang giả |
| `image` | Hình ảnh chứa thông tin đáng ngờ | Ảnh chụp màn hình tin nhắn lừa đảo |
| `text` | Văn bản / Popup cảnh báo giả | Popup "máy tính nhiễm virus" |

Admin có thể tạo kịch bản HTML tùy ý với đầy đủ CSS và JavaScript để mô phỏng tình huống thực tế.

---

## Bảo mật

- Chỉ admin được nhập HTML tự do (sau khi xác thực bằng key)
- Kịch bản hiển thị cho người dùng: link không thể click thật (`pointer-events: none`)
- Preview trong admin dùng `iframe sandbox` để cô lập JavaScript
- Tên file upload được làm sạch bằng `werkzeug.utils.secure_filename`

---

## Phát triển bởi

Nhóm An toàn Thông tin — Khối Tài chính  
Công cụ: Python, Flask, Bootstrap 5, CodeMirror
