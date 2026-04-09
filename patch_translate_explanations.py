# -*- coding: utf-8 -*-
"""Dịch toàn bộ giải thích tiếng Anh sang tiếng Việt."""
import sys, os
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(__file__))
from app import app
from models import db, Question

VI_EXPLANATIONS = {
    "Fake CAPTCHA instructing mshta.exe (ClickFix)":
        "Đây là tấn công ClickFix PHISHING dùng kỹ thuật Living-off-the-Land (LOTL). Dấu hiệu: (1) CAPTCHA thật không bao giờ yêu cầu chạy lệnh thủ công — reCAPTCHA thật hoạt động hoàn toàn trong trình duyệt. (2) mshta.exe là công cụ Windows tích hợp bị lạm dụng để tải và chạy file .hta từ máy chủ của kẻ tấn công. (3) Kỹ thuật này qua mặt phần mềm diệt virus vì dùng file hệ thống Windows được ký số chính thức. (4) Chạy lệnh sẽ cài mã độc âm thầm — đóng tab ngay và báo cáo IT.",

    "Fake Microsoft 365 login portal":
        "Đây là trang PHISHING giả mạo đăng nhập Microsoft 365. Dấu hiệu: (1) URL là 'microsoft-365-login.auth-verify.com' — trang đăng nhập Microsoft thật là 'login.microsoftonline.com'. (2) Trang dùng tên miền nhái để đánh cắp thông tin đăng nhập. (3) Mọi thông tin nhập vào đều gửi trực tiếp cho kẻ tấn công. Luôn kiểm tra thanh địa chỉ trước khi nhập mật khẩu — dùng trình quản lý mật khẩu vì nó sẽ không tự điền trên trang giả.",

    "Fake SharePoint document share notification":
        "Đây là email PHISHING giả mạo Microsoft SharePoint. Dấu hiệu: (1) Domain người gửi là 'sharepoint-docshare.net' — thông báo SharePoint thật đến từ '@microsoft.com' hoặc domain SharePoint của công ty. (2) Nhấn 'Mở trong SharePoint' chuyển hướng đến trang đăng nhập giả để đánh cắp thông tin Microsoft 365. (3) Cảnh giác với các chia sẻ file bất ngờ dù tên người gửi quen thuộc — tên người gửi có thể bị giả mạo. Xác minh trực tiếp với người gửi qua Teams hoặc điện thoại.",

    "Fake DocuSign signature request":
        "Đây là email PHISHING giả mạo DocuSign. Dấu hiệu: (1) Domain người gửi là 'docusign-secure-document.com' — DocuSign thật dùng '@docusign.com' hoặc '@docusign.net'. (2) Nút 'XEM TÀI LIỆU' dẫn đến trang đăng nhập giả để đánh cắp thông tin Microsoft hoặc Google. (3) Luôn truy cập trực tiếp docusign.com để kiểm tra hộp thư thay vì nhấn link trong email. Liên hệ HR trực tiếp để xác minh xem có hợp đồng thật được gửi không.",

    "Fake browser update prompting PowerShell command":
        "Đây là tấn công ClickFix PHISHING dùng PowerShell theo kỹ thuật Living-off-the-Land. Dấu hiệu: (1) Chrome và mọi trình duyệt đều tự cập nhật âm thầm — không bao giờ yêu cầu chạy lệnh PowerShell. (2) Lệnh dùng '-ep bypass' để vô hiệu hoá kiểm tra chính sách bảo mật, sau đó tải và chạy script từ máy chủ kẻ tấn công. (3) Kỹ thuật này được dùng để phát tán infostealer (RedLine, Lumma) và trojan điều khiển từ xa. Đóng trang ngay và báo cáo IT.",

    "Legitimate GitHub security vulnerability alert":
        "Đây là cảnh báo bảo mật HỢP LỆ từ GitHub. Dấu hiệu bình thường: (1) Gửi từ domain chính thức '@github.com'. (2) Không chứa link có thể nhấn trong nội dung — hướng dẫn truy cập trực tiếp github.com. (3) Tham chiếu đến CVE thật và repository của bạn. (4) Đây là định dạng chuẩn của cảnh báo Dependabot. Luôn xác minh bằng cách tự đăng nhập vào github.com.",

    "Malicious macro-enabled Excel attachment (Q4 report)":
        "Đây là email PHISHING phát tán mã độc qua file Excel có macro. Dấu hiệu: (1) Người gửi không phải nhóm phân tích nội bộ — domain 'business-reports-online.com' là bên ngoài và không quen thuộc. (2) Phần mở rộng .xlsm là file Excel có macro, có thể thực thi mã tuỳ ý. (3) Hướng dẫn 'Bật Nội dung' là bước kích hoạt mã độc của kẻ tấn công — macro bị tắt mặc định chính vì lý do này. (4) Báo cáo nội bộ thật không được gửi bất ngờ từ nguồn bên ngoài không quen biết. Không bao giờ bật macro trên file không mong đợi.",

    "Fake Microsoft Teams missed messages notification":
        "Đây là email PHISHING giả mạo thông báo Microsoft Teams. Dấu hiệu: (1) Domain người gửi là 'ms-teams-alerts.com' — email Teams thật đến từ '@microsoft.com'. (2) Tin nhắn giả từ 'IT Support' về tài khoản bị tạm khóa là chiến thuật tạo khẩn cấp điển hình. (3) Nhấn 'Mở Teams Messages' dẫn đến trang đăng nhập Microsoft giả để đánh cắp thông tin. (4) Thông báo Teams thật dẫn đến 'teams.microsoft.com'. Luôn mở Teams trực tiếp qua ứng dụng hoặc gõ teams.microsoft.com.",

    "Legitimate GitHub security vulnerability alert":
        "Đây là cảnh báo bảo mật HỢP LỆ từ GitHub. Dấu hiệu bình thường: (1) Gửi từ domain chính thức '@github.com'. (2) Không chứa link có thể nhấn — hướng dẫn truy cập github.com trực tiếp. (3) Tham chiếu CVE thật và repository của bạn. (4) Đây là định dạng chuẩn của cảnh báo Dependabot. Luôn xác minh bằng cách tự đăng nhập vào github.com.",

    "Spear phishing job offer with malicious PDF attachment":
        "Đây là email Spear Phishing nhắm vào chuyên gia tài chính bằng lời mời việc giả. Dấu hiệu: (1) Domain nhà tuyển dụng 'financialcareers-apac.com' không phải công ty tuyển dụng uy tín đã xác minh — kiểm tra trên LinkedIn trước khi phản hồi. (2) File PDF đính kèm có thể khai thác lỗ hổng Adobe Reader hoặc dùng JavaScript để đánh cắp thông tin hoặc cài mã độc khi mở. (3) Mức lương hấp dẫn bất thường kết hợp thời hạn khẩn cấp ('48 giờ') là mồi nhử điển hình cho mục tiêu giá trị cao. (4) Nhà tuyển dụng thật tại công ty uy tín dùng domain đã xác minh. Không bao giờ mở file đính kèm từ lời mời việc chưa xác minh.",
}


def run():
    ok = skip = 0
    for title, new_exp in VI_EXPLANATIONS.items():
        q = Question.query.filter_by(title=title).first()
        if not q:
            print(f"  [miss] {title}")
            continue
        if q.explanation == new_exp:
            print(f"  [skip] {title}")
            skip += 1
            continue
        q.explanation = new_exp
        db.session.add(q)
        print(f"  [ok]   {title}")
        ok += 1
    db.session.commit()
    print(f"\nDone. Updated: {ok}, Skipped: {skip}")


if __name__ == "__main__":
    with app.app_context():
        run()
