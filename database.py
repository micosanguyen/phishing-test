from models import db, Question


SAMPLE_QUESTIONS = [
    {
        "title": "Email giả mạo ngân hàng VCB",
        "scenario_type": "email",
        "content": """<div class="email-mockup">
  <div class="email-header">
    <div class="email-field"><span class="label">Từ:</span> <span class="value">security@vietcombank-alert.com</span></div>
    <div class="email-field"><span class="label">Đến:</span> <span class="value">__USER_EMAIL__</span></div>
    <div class="email-field"><span class="label">Tiêu đề:</span> <span class="value">⚠️ Tài khoản của bạn bị tạm khóa - Xác minh ngay!</span></div>
  </div>
  <div class="email-body">
    <p>Kính gửi Quý khách hàng,</p>
    <p>Chúng tôi phát hiện hoạt động <strong>đáng ngờ</strong> trên tài khoản của bạn. Để bảo vệ tài sản, tài khoản đã bị <span style="color:red;font-weight:bold">TẠM KHÓA</span>.</p>
    <p>Vui lòng xác minh danh tính trong <strong>24 giờ</strong> để tránh mất quyền truy cập vĩnh viễn:</p>
    <a href="#" onclick="return false;" style="background:#003087;color:white;padding:10px 20px;text-decoration:none;border-radius:4px;display:inline-block;margin:10px 0">Xác minh tài khoản ngay</a>
    <p style="color:#888;font-size:12px">Vietcombank © 2024 | support@vcb.com.vn</p>
  </div>
</div>""",
        "is_phishing": True,
        "explanation": "Đây là email PHISHING. Dấu hiệu nhận biết: (1) Địa chỉ email người gửi là 'vietcombank-alert.com' thay vì 'vietcombank.com.vn' chính thức. (2) Tạo cảm giác khẩn cấp với '24 giờ'. (3) Ngân hàng thật không bao giờ yêu cầu xác minh qua email. Hãy gọi hotline chính thức nếu nghi ngờ.",
    },
    {
        "title": "Link rút ngắn đến trang đăng nhập giả",
        "scenario_type": "link",
        "content": """<div class="link-scenario">
  <p>Bạn nhận được tin nhắn Zalo từ một người bạn:</p>
  <div class="chat-bubble">
    <p><strong>Nguyễn Văn A:</strong> "Ơi mày xem thử cái này đi, tao vừa trúng thưởng iPhone 15 từ Shopee nè, mày vào link này điền thông tin là nhận được luôn 🎁"</p>
    <code>https://bit.ly/shopee-giftxyz</code>
  </div>
  <p style="margin-top:12px">Link rút gọn dẫn đến: <code>http://shopee-gift.net/dang-nhap</code></p>
</div>""",
        "is_phishing": True,
        "explanation": "Đây là PHISHING. Dấu hiệu: (1) Domain 'shopee-gift.net' không phải shopee.vn chính thức. (2) Dùng link rút gọn để che địa chỉ thật. (3) Mồi nhử 'trúng thưởng' tạo hứng thú giả tạo. (4) Tài khoản bạn bè có thể đã bị chiếm. Không bao giờ đăng nhập qua link từ tin nhắn.",
    },
    {
        "title": "Thông báo cập nhật mật khẩu IT nội bộ",
        "scenario_type": "email",
        "content": """<div class="email-mockup">
  <div class="email-header">
    <div class="email-field"><span class="label">Từ:</span> <span class="value">it-support@congty.com.vn</span></div>
    <div class="email-field"><span class="label">Đến:</span> <span class="value">__USER_EMAIL__</span></div>
    <div class="email-field"><span class="label">Tiêu đề:</span> <span class="value">Lịch bảo trì hệ thống - Chủ nhật 22/12 từ 23:00-02:00</span></div>
  </div>
  <div class="email-body">
    <p>Xin chào các bạn,</p>
    <p>Phòng IT thông báo lịch bảo trì hệ thống định kỳ:</p>
    <ul>
      <li>Thời gian: Chủ nhật 22/12/2024, 23:00 – 02:00 thứ Hai</li>
      <li>Hệ thống bị ảnh hưởng: Email nội bộ, VPN, phần mềm chấm công</li>
      <li>Vui lòng lưu tài liệu đang làm việc trước 22:30</li>
    </ul>
    <p>Mọi thắc mắc liên hệ: <a href="mailto:it-support@congty.com.vn">it-support@congty.com.vn</a> hoặc máy nhánh 1234.</p>
    <p>Trân trọng,<br>Phòng IT</p>
  </div>
</div>""",
        "is_phishing": False,
        "explanation": "Đây là email HỢP LỆ từ phòng IT nội bộ. Dấu hiệu bình thường: (1) Domain email trùng với tên công ty. (2) Không yêu cầu click link hoặc nhập thông tin. (3) Cung cấp kênh liên hệ nội bộ rõ ràng (email + máy nhánh). (4) Nội dung thông báo hành chính bình thường.",
    },
    {
        "title": "Popup cảnh báo virus giả",
        "scenario_type": "text",
        "content": """<div class="popup-mockup" style="border:3px solid red;background:#fff3f3;padding:20px;max-width:450px;margin:auto;border-radius:8px;font-family:Arial">
  <div style="text-align:center;color:red;font-size:24px;margin-bottom:10px">⚠️ CẢNH BÁO BẢO MẬT</div>
  <p style="font-weight:bold">Máy tính của bạn bị nhiễm <span style="color:red">5 virus nguy hiểm!</span></p>
  <p>Windows đã phát hiện các mối đe dọa nghiêm trọng. Phần mềm độc hại đang đánh cắp thông tin ngân hàng của bạn.</p>
  <p><strong>Gọi ngay đường dây hỗ trợ Microsoft:</strong></p>
  <div style="font-size:22px;font-weight:bold;text-align:center;color:#0078d4;margin:10px 0">1800-xxx-xxxx</div>
  <button onclick="return false;" style="width:100%;background:red;color:white;padding:12px;border:none;font-size:16px;cursor:pointer;border-radius:4px">Quét virus ngay - MIỄN PHÍ</button>
</div>""",
        "is_phishing": True,
        "explanation": "Đây là PHISHING kiểu 'scareware'. Chiến thuật: (1) Tạo ra nỗi sợ bằng cảnh báo virus giả. (2) Số điện thoại giả mạo Microsoft — Microsoft không bao giờ hiển thị popup yêu cầu gọi điện. (3) Nếu gọi, kẻ tấn công sẽ lừa cài phần mềm điều khiển từ xa hoặc thu tiền. Đóng tab/cửa sổ ngay lập tức.",
    },
    {
        "title": "Email xác nhận đặt hàng Tiki hợp lệ",
        "scenario_type": "email",
        "content": """<div class="email-mockup">
  <div class="email-header">
    <div class="email-field"><span class="label">Từ:</span> <span class="value">no-reply@tiki.vn</span></div>
    <div class="email-field"><span class="label">Đến:</span> <span class="value">__USER_EMAIL__</span></div>
    <div class="email-field"><span class="label">Tiêu đề:</span> <span class="value">Xác nhận đơn hàng #TK20241215-88421</span></div>
  </div>
  <div class="email-body">
    <p>Xin chào, đơn hàng của bạn đã được xác nhận.</p>
    <table style="border-collapse:collapse;width:100%">
      <tr style="background:#f5f5f5"><td style="padding:8px"><strong>Sản phẩm</strong></td><td style="padding:8px">Laptop Asus VivoBook 15</td></tr>
      <tr><td style="padding:8px"><strong>Mã đơn</strong></td><td style="padding:8px">#TK20241215-88421</td></tr>
      <tr style="background:#f5f5f5"><td style="padding:8px"><strong>Tổng tiền</strong></td><td style="padding:8px">12.990.000đ</td></tr>
      <tr><td style="padding:8px"><strong>Giao hàng dự kiến</strong></td><td style="padding:8px">17/12/2024</td></tr>
    </table>
    <p style="margin-top:12px">Theo dõi đơn hàng tại <a href="#">tiki.vn/order</a> hoặc ứng dụng Tiki.</p>
    <p style="color:#888;font-size:12px">© 2024 Tiki Corporation. 52 Út Tịch, Phường 4, Q. Tân Bình, TP.HCM</p>
  </div>
</div>""",
        "is_phishing": False,
        "explanation": "Đây là email HỢP LỆ từ Tiki. Dấu hiệu: (1) Domain 'tiki.vn' chính thức. (2) Nội dung chỉ xác nhận thông tin đơn hàng, không yêu cầu thêm hành động hay nhập thông tin. (3) Có địa chỉ công ty thực tế. (4) Không tạo áp lực khẩn cấp.",
    },
]


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        if Question.query.count() == 0:
            seed_questions()


def seed_questions():
    for q in SAMPLE_QUESTIONS:
        question = Question(**q)
        db.session.add(question)
    db.session.commit()
