# -*- coding: utf-8 -*-
"""
Cập nhật button trong các kịch bản phishing để hiển thị link giả mạo thực tế khi hover.
Chạy: python patch_button_links.py
"""
import sys
import os
import re
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(__file__))

from app import app
from models import db, Question


def apply_patches(content, patches):
    changed = 0
    for old, new, use_regex in patches:
        if use_regex:
            new_content = re.sub(old, new, content, count=1, flags=re.DOTALL)
            if new_content != content:
                content = new_content
                changed += 1
        else:
            if old in content:
                content = content.replace(old, new, 1)
                changed += 1
    return content, changed


# ── Tuple: (title, [(old, new, use_regex), ...]) ────────────────────────────
PATCHES = [

    # ── Câu 1: Email VCB ─────────────────────────────────────────────────────
    ("Email giả mạo ngân hàng VCB", [
        (
            'href="#" onclick="return false;" style="background:#003087;color:white;padding:10px 20px;text-decoration:none;border-radius:4px;display:inline-block;margin:10px 0"',
            'href="https://vietcombank-alert.com/xac-minh?ref=email&token=VCB2024&step=verify" onclick="return false;" style="background:#003087;color:white;padding:10px 20px;text-decoration:none;border-radius:4px;display:inline-block;margin:10px 0"',
            False,
        ),
    ]),

    # ── Câu 2: Shopee link ───────────────────────────────────────────────────
    ("Link rút ngắn đến trang đăng nhập giả", [
        (
            '<code>http://shopee-gift.net/dang-nhap</code>',
            '<a href="http://shopee-gift.net/dang-nhap" onclick="return false;" style="font-family:monospace;color:#0070f3">http://shopee-gift.net/dang-nhap</a>',
            False,
        ),
    ]),

    # ── Câu 4: Popup virus giả ───────────────────────────────────────────────
    ("Popup cảnh báo virus giả", [
        (
            r'<button onclick="return false;" style="width:100%;background:red;[^"]*">[^<]*Quét virus ngay[^<]*</button>',
            '<a href="https://microsoft-support-secure.net/free-scan?threats=5&pc=infected&action=clean" onclick="return false;" style="display:block;text-align:center;text-decoration:none;background:red;color:white;padding:12px;font-size:16px;cursor:pointer;border-radius:4px;box-sizing:border-box">Quét virus ngay - MIỄN PHÍ</a>',
            True,
        ),
    ]),

    # ── Câu 6: Invoice malware ───────────────────────────────────────────────
    ("Email hoá đơn có file đính kèm độc hại", [
        (
            'href="#" onclick="return false;" style="background:#0078d4;color:white;padding:8px 18px;text-decoration:none;border-radius:4px;display:inline-block"',
            'href="https://cungcap-xanh.com/invoice/download?f=HoaDon_T12_2024.pdf.exe&confirm=sign2024" onclick="return false;" style="background:#0078d4;color:white;padding:8px 18px;text-decoration:none;border-radius:4px;display:inline-block"',
            False,
        ),
    ]),

    # ── Câu 7: ClickFix mshta.exe ────────────────────────────────────────────
    ("Fake CAPTCHA instructing mshta.exe (ClickFix)", [
        (
            r'<button onclick="return false;" style="width:100%;background:#34a853;[^"]*">[\s\S]*?</button>',
            '<a href="https://verify-captcha-cdn.net/complete?session=cap_ok&user=verified&redirect=1" onclick="return false;" style="display:block;text-align:center;text-decoration:none;background:#34a853;color:white;padding:10px;border-radius:4px;font-size:14px;cursor:pointer;box-sizing:border-box">✔ I have completed the steps — Continue</a>',
            True,
        ),
    ]),

    # ── Câu 9: BIDV SMS ──────────────────────────────────────────────────────
    ("SMS giả mạo ngân hàng BIDV yêu cầu OTP", [
        (
            'href="#" onclick="return false;" style="color:#0070f3;word-break:break-all"',
            'href="http://bidv-xacminh.net/chan-truy-cap?uid=XX8821&bank=BIDV&action=block-device" onclick="return false;" style="color:#0070f3;word-break:break-all"',
            False,
        ),
    ]),

    # ── Câu 10: Fake SharePoint ───────────────────────────────────────────────
    ("Fake SharePoint document share notification", [
        (
            'href="#" onclick="return false;" style="background:#0078d4;color:white;padding:9px 20px;text-decoration:none;border-radius:4px;display:inline-block"',
            'href="https://sharepoint-docshare.net/open?doc=Q4_Financial_Report_FINAL.xlsx&user=__USER_EMAIL__&auth=required" onclick="return false;" style="background:#0078d4;color:white;padding:9px 20px;text-decoration:none;border-radius:4px;display:inline-block"',
            False,
        ),
    ]),

    # ── Câu 12: HR lương ─────────────────────────────────────────────────────
    ("Email giả HR yêu cầu cập nhật thông tin lương", [
        (
            'href="#" onclick="return false;" style="background:#e53935;color:white;padding:10px 22px;text-decoration:none;border-radius:4px;display:inline-block;margin:10px 0;font-weight:bold"',
            'href="https://nhan-su-portal.com/cap-nhat-luong?user=__USER_EMAIL__&token=HR2024&redirect=bank-info" onclick="return false;" style="background:#e53935;color:white;padding:10px 22px;text-decoration:none;border-radius:4px;display:inline-block;margin:10px 0;font-weight:bold"',
            False,
        ),
    ]),

    # ── Câu 13: Fake DocuSign ─────────────────────────────────────────────────
    ("Fake DocuSign signature request", [
        (
            'href="#" onclick="return false;" style="background:#ffb300;color:white;padding:10px 24px;text-decoration:none;border-radius:4px;display:inline-block;font-weight:bold"',
            'href="https://docusign-secure-document.com/s/Employment_Contract_Amendment_2025?signer=__USER_EMAIL__&expires=20241231" onclick="return false;" style="background:#ffb300;color:white;padding:10px 24px;text-decoration:none;border-radius:4px;display:inline-block;font-weight:bold"',
            False,
        ),
    ]),

    # ── Câu 14: ClickFix PowerShell ──────────────────────────────────────────
    ("Fake browser update prompting PowerShell command", [
        (
            r'<button onclick="return false;" style="width:100%;background:#1a73e8;[^"]*">Update Complete[^<]*</button>',
            '<a href="https://chrome-patch.update-cdn.net/done?ver=131.0.6778&status=applied&next=continue" onclick="return false;" style="display:block;text-align:center;text-decoration:none;background:#1a73e8;color:white;padding:10px;border-radius:4px;font-size:14px;cursor:pointer;box-sizing:border-box">Update Complete — Click to Continue</a>',
            True,
        ),
    ]),

    # ── Câu 16: Fake IT VPN ──────────────────────────────────────────────────
    ("Email giả IT yêu cầu đặt lại mật khẩu VPN", [
        (
            'href="#" onclick="return false;" style="background:#1565c0;color:white;padding:10px 22px;text-decoration:none;border-radius:4px;display:inline-block"',
            'href="https://congty-support.net/vpn/renew?user=__USER_EMAIL__&expire=24h&token=IT2024renew" onclick="return false;" style="background:#1565c0;color:white;padding:10px 22px;text-decoration:none;border-radius:4px;display:inline-block"',
            False,
        ),
    ]),

    # ── Câu 17: GHN SMS ──────────────────────────────────────────────────────
    ("SMS giả mạo GHN thông báo giao hàng thất bại", [
        (
            'href="#" onclick="return false;" style="color:#e53935;word-break:break-all;font-size:13px"',
            'href="http://ghn-xacnhan.delivery-vn.net/GHN8821?order=GHN8821XXXX&fee=15000&action=confirm-address" onclick="return false;" style="color:#e53935;word-break:break-all;font-size:13px"',
            False,
        ),
    ]),

    # ── Câu 19: Tổng cục Thuế ────────────────────────────────────────────────
    ("Email giả mạo Tổng cục Thuế yêu cầu truy thu", [
        (
            'href="#" onclick="return false;" style="background:#c62828;color:white;padding:10px 20px;text-decoration:none;border-radius:4px;display:inline-block"',
            'href="https://tong-cuc-thue-gov.com/nop-thue?sotien=42800000&kytinh=2022-2024&user=__USER_EMAIL__&token=TCT2024" onclick="return false;" style="background:#c62828;color:white;padding:10px 20px;text-decoration:none;border-radius:4px;display:inline-block"',
            False,
        ),
    ]),

    # ── Câu 21: Fake Teams ───────────────────────────────────────────────────
    ("Fake Microsoft Teams missed messages notification", [
        (
            'href="#" onclick="return false;" style="background:#6264a7;color:white;padding:10px 24px;text-decoration:none;border-radius:4px;display:inline-block"',
            'href="https://ms-teams-alerts.com/auth?user=__USER_EMAIL__&redirect=teams-inbox&session=new" onclick="return false;" style="background:#6264a7;color:white;padding:10px 24px;text-decoration:none;border-radius:4px;display:inline-block"',
            False,
        ),
    ]),

    # ── Câu 22: Crypto pig butchering ────────────────────────────────────────
    ("Tin nhắn lừa đảo đầu tư crypto (pig butchering)", [
        (
            'href="#" onclick="return false;" style="color:#0070f3"',
            'href="https://cryptogold-pro.vip/register?ref=linh_nguyen&bonus=5m_vnd&affiliate=1" onclick="return false;" style="color:#0070f3"',
            False,
        ),
    ]),

    # ── Câu 23: Norton scareware ─────────────────────────────────────────────
    ("Popup giả mạo Norton diệt virus hết hạn", [
        (
            r'<button onclick="return false;" style="width:100%;background:#e53935;[^"]*font-weight:bold;[^"]*margin-bottom:8px">[^<]*Gia hạn ngay[^<]*</button>',
            '<a href="https://norton-renew-secure.com/checkout?product=360deluxe&plan=1yr&price=299000&curr=VND" onclick="return false;" style="display:block;text-align:center;text-decoration:none;background:#e53935;color:white;padding:12px;font-size:15px;font-weight:bold;cursor:pointer;border-radius:4px;margin-bottom:8px;box-sizing:border-box">⚡ Gia hạn ngay — Chỉ 299.000đ/năm</a>',
            True,
        ),
        (
            r'<button onclick="return false;" style="width:100%;background:transparent;[^"]*">Bỏ qua[^<]*</button>',
            '<a href="https://norton-renew-secure.com/risk-accepted?level=high&unprotected=true" onclick="return false;" style="display:block;text-align:center;text-decoration:none;background:transparent;color:#999;padding:8px;border:1px solid #ddd;font-size:12px;cursor:pointer;border-radius:4px;box-sizing:border-box">Bỏ qua (không được khuyến nghị)</a>',
            True,
        ),
    ]),

    # ── Câu 24: Spear phishing job offer ─────────────────────────────────────
    ("Spear phishing job offer with malicious PDF attachment", [
        (
            'href="#" onclick="return false;" style="background:#1565c0;color:white;padding:9px 20px;text-decoration:none;border-radius:4px;display:inline-block"',
            'href="https://financialcareers-apac.com/jd/JobDescription_SeniorAnalyst_DBS.pdf?track=email&ref=__USER_EMAIL__" onclick="return false;" style="background:#1565c0;color:white;padding:9px 20px;text-decoration:none;border-radius:4px;display:inline-block"',
            False,
        ),
    ]),
]


def run():
    ok, skip, miss = 0, 0, 0
    for title, patches in PATCHES:
        q = Question.query.filter_by(title=title).first()
        if not q:
            print(f"  [miss] Not found: '{title}'")
            miss += 1
            continue
        new_content, changed = apply_patches(q.content, patches)
        if changed:
            q.content = new_content
            db.session.add(q)
            print(f"  [ok]   {title}")
            ok += 1
        else:
            print(f"  [skip] Already patched: '{title}'")
            skip += 1
    db.session.commit()
    print(f"\nDone. Updated: {ok}, Skipped: {skip}, Not found: {miss}")


if __name__ == "__main__":
    with app.app_context():
        run()
