import pytest
import time
import os
import socket
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Konfigurasi basis URL - penting untuk CI/CD
BASE_URL = "http://localhost/damncrud"

# Fungsi untuk memeriksa apakah server berjalan
def is_server_running():
    try:
        # Coba buka koneksi ke server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # timeout 2 detik
        sock.connect(('localhost', 80))
        sock.close()
        return True
    except:
        return False

# Skip semua test jika server tidak berjalan
pytestmark = pytest.mark.skipif(
    not is_server_running() or os.environ.get('CI') == 'true', 
    reason="Server tidak berjalan atau berjalan di lingkungan CI"
)

@pytest.fixture
def browser():
    # Setup untuk lingkungan CI/CD
    options = Options()
    options.add_argument('--headless')  # Penting untuk CI/CD
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    # Gunakan Chrome yang disediakan oleh GitHub Actions
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    
    yield driver
    
    # Teardown
    driver.quit()

def test_login_logout(browser):
    """TC1: Login dan logout dari sistem"""
    # 1. Buka halaman login
    browser.get(f"{BASE_URL}/login.php")
    
    # 2. Masukkan username dan password valid
    browser.find_element(By.NAME, "username").send_keys("admin")
    browser.find_element(By.NAME, "password").send_keys("nimda666!")
    
    # 3. Klik tombol 'OK I'm sign in'
    browser.find_element(By.CLASS_NAME, "btn-danger").click()
    
    time.sleep(2)
    # 4. Pastikan sudah berada pada laman index.php
    current_url = browser.current_url
    assert "index.php" in current_url
    
    # 5. Klik tombol "Sign Out"
    browser.find_element(By.LINK_TEXT, "Sign out").click()
    
    time.sleep(2)
    # Verifikasi: Redirect ke login.php
    current_url = browser.current_url
    assert "login.php" in current_url

def test_add_new_contact(browser):
    """TC2: Menambahkan kontak baru"""
    # 1. Login ke sistem
    browser.get(f"{BASE_URL}/login.php")
    browser.find_element(By.NAME, "username").send_keys("admin")
    browser.find_element(By.NAME, "password").send_keys("nimda666!")
    browser.find_element(By.CLASS_NAME, "btn-danger").click()
    time.sleep(2)
    
    # 2. Klik tombol "Add New Contact"
    browser.find_element(By.LINK_TEXT, "Add New Contact").click()
    
    # 3. Mengisi form yang sudah disediakan
    browser.find_element(By.NAME, "name").send_keys("Dimas")
    browser.find_element(By.NAME, "email").send_keys("dimas.rifqi@example.com")
    browser.find_element(By.NAME, "phone").send_keys("123456789")
    browser.find_element(By.NAME, "title").send_keys("Developer")
    
    # 4. Klik tombol "save"
    browser.find_element(By.CLASS_NAME, "btn-primary").click()
    
    time.sleep(2)
    # Verifikasi: Redirect ke index.php
    current_url = browser.current_url
    assert "index.php" in current_url

def test_delete_contact(browser):
    """TC3: Menghapus kontak dari list"""
    # 1. Login ke sistem
    browser.get(f"{BASE_URL}/login.php")
    browser.find_element(By.NAME, "username").send_keys("admin")
    browser.find_element(By.NAME, "password").send_keys("nimda666!")
    browser.find_element(By.CLASS_NAME, "btn-danger").click()
    time.sleep(2)
    
    # 2. Klik tombol "delete" pada list row pertama
    # Menggunakan XPath untuk menargetkan tombol delete pada baris pertama
    delete_button = browser.find_element(By.XPATH, "//table/tbody/tr[1]//a[contains(@href, 'delete')]")
    delete_button.click()
    
    # 3. Konfirmasi alert dan klik OK
    alert = browser.switch_to.alert
    alert.accept()
    
    time.sleep(2)
    # Verifikasi: Redirect ke index.php
    current_url = browser.current_url
    assert "index.php" in current_url

def test_change_profile_picture(browser):
    """TC4: Mengubah foto profil"""
    # 1. Login ke sistem
    browser.get(f"{BASE_URL}/login.php")
    browser.find_element(By.NAME, "username").send_keys("admin")
    browser.find_element(By.NAME, "password").send_keys("nimda666!")
    browser.find_element(By.CLASS_NAME, "btn-danger").click()
    time.sleep(2)
    
    # 2. Klik tombol "profil"
    browser.find_element(By.CLASS_NAME, "btn-primary").click()
    
    # 3. Memilih file yang sudah disediakan - Disesuaikan untuk CI/CD
    file_input = browser.find_element(By.NAME, "image")
    # Gunakan path relatif untuk file test di CI/CD
    file_path = "helper/pp_baru.jpg"
    file_input.send_keys(str(file_path))
    
    # 4. Klik tombol "Change"
    browser.find_element(By.CLASS_NAME, "btn-secondary").click()
    
    time.sleep(2)
    # Verifikasi: Halaman profil di-refresh
    current_url = browser.current_url
    assert "profil.php" in current_url

def test_edit_contact(browser):
    """TC5: Mengedit kontak"""
    # 1. Login ke sistem
    browser.get(f"{BASE_URL}/login.php")
    browser.find_element(By.NAME, "username").send_keys("admin")
    browser.find_element(By.NAME, "password").send_keys("nimda666!")
    browser.find_element(By.CLASS_NAME, "btn-danger").click()
    time.sleep(2)
    
    # 2. Cari dan klik tombol edit dengan cara yang lebih spesifik
    try:
        # Cari bagian actions pada baris pertama
        actions_section = browser.find_element(By.XPATH, "//tr[@role='row'][1]//td[contains(@class, 'actions')]")
        # Cari tombol edit di dalam bagian actions tersebut
        update_button = actions_section.find_element(By.XPATH, ".//a[contains(@class, 'btn-success')]")
    except:
        # Fallback jika struktur DOM berbeda
        update_button = browser.find_element(By.XPATH, "//a[contains(@href, 'edit')]")
    
    update_button.click()
    
    # Verifikasi: Sudah masuk ke halaman update.php
    time.sleep(1)
    current_url = browser.current_url
    assert "update.php" in current_url
    
    # 3. Mengisi form yang sudah disediakan
    # Membersihkan field terlebih dahulu
    name_field = browser.find_element(By.NAME, "name")
    name_field.clear()
    name_field.send_keys("Samid")
    
    email_field = browser.find_element(By.NAME, "email")
    email_field.clear()
    email_field.send_keys("samid.123@example.com")
    
    # Field phone tidak perlu di-clear karena di form memang kosong (value="")
    phone_field = browser.find_element(By.NAME, "phone")
    phone_field.send_keys("987654321")
    
    title_field = browser.find_element(By.NAME, "title")
    title_field.clear()
    title_field.send_keys("Programer")
    
    # 4. Klik tombol "update"
    browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    
    time.sleep(2)
    # Verifikasi: Redirect ke index.php
    current_url = browser.current_url
    assert "index.php" in current_url
