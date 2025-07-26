from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import requests, time

# Thông tin
TOKEN = '6658339242:AAGYz903ktLH_dMjU1csEI-9zsOkT0UOyKY'
CHAT_ID = '812138426'
URL = 'https://www.fahasa.com/su-tu-thang-3-tap-3-tai-ban-2025.html'

# Gửi thông báo Telegram
def notify(msg):
    try:
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        payload = {
            'chat_id': CHAT_ID,
            'text': msg,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, data=payload)
        
        if response.status_code != 200:
            print(f"[{datetime.now():%H:%M:%S}] ❌ Lỗi gửi Telegram: {response.text}")
        else:
            print(f"[{datetime.now():%H:%M:%S}] ✅ Đã gửi Telegram")
    except Exception as e:
        print(f"[LỖI TELEGRAM] {e}")

# Khởi tạo trình duyệt
options = Options()
# options.add_argument('--headless')  # Bật nếu muốn chạy ngầm
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)

# Kiểm tra trạng thái hàng
def check_stock():
    try:
        driver.get(URL)
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product_view_msg_mobile_content"))
        )
        text = el.get_attribute("innerText").strip()
        print(f"[{datetime.now():%H:%M:%S}] 🕵️ Nội dung: >>>{text}<<<")
        return "Sản phẩm tạm hết hàng" not in text
    except Exception as e:
        print(f"[{datetime.now():%H:%M:%S}] ⚠️ Lỗi kiểm tra: {e}")
        return False

# Vòng lặp chính
while True:
    try:
        if check_stock():
            notify(f"📦 <b>SẢN PHẨM CÓ HÀNG</b>!\n🔗 {URL}")
        else:
            print(f"[{datetime.now():%H:%M:%S}] ❌ Hết hàng (không gửi)")
    except Exception as e:
        print(f"[LỖI CHUNG] {e}")
    time.sleep(10)
