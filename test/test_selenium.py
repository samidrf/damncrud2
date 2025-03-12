import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def browser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options
    )
    driver.implicitly_wait(5)

    yield driver
    driver.quit()


def login(browser, username, password):
    """Fungsi login agar bisa digunakan ulang di berbagai test case."""
    browser.get("http://localhost/damncrud/login.php")
    browser.find_element(By.NAME, "username").send_keys(username)
    browser.find_element(By.NAME, "password").send_keys(password)
    browser.find_element(By.CLASS_NAME, "btn-danger").click()
    time.sleep(2)


def test_01_login_logout(browser):
    """TC1: Login dan logout dari sistem"""
    # 1. Buka halaman login
    browser.get("http://localhost/damncrud/login.php")
    
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


def test_02_add_new_contact(browser):
    """TC2: Menambahkan kontak baru"""
    # 1. Login ke sistem
    login(browser, "admin", "nimda666!")
    
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


def test_03_delete_contact(browser):
    """TC3: Menghapus kontak dari list"""
    # 1. Login ke sistem
    login(browser, "admin", "nimda666!")
    
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


def test_04_change_profile_picture(browser):
    """TC4: Mengubah foto profil"""
    # 1. Login ke sistem
    login(browser, "admin", "nimda666!")
    
    # 2. Klik tombol "profil"
    browser.find_element(By.CLASS_NAME, "btn-primary").click()
    
    # 3. Memilih file yang sudah disediakan
    file_input = browser.find_element(By.NAME, "image")
    file_path = r"C:\Storage\Apk\Database\MySQL\XAMPP\htdocs\damncrud\helper\pp_baru.jpg"
    file_input.send_keys(file_path)
    
    # 4. Klik tombol "Change"
    browser.find_element(By.CLASS_NAME, "btn-secondary").click()
    
    time.sleep(2)
    # Verifikasi: Halaman profil di-refresh dengan foto profil baru
    current_url = browser.current_url
    assert "profil.php" in current_url


def test_05_edit_contact(browser):
    """TC5: Mengedit kontak"""
    # 1. Login ke sistem
    login(browser, "admin", "nimda666!")
    
    # 2. Cari dan klik tombol edit dengan cara yang lebih spesifik
    # Cari bagian actions pada baris pertama
    actions_section = browser.find_element(By.XPATH, "//tr[@role='row'][1]//td[contains(@class, 'actions')]")
    # Cari tombol edit di dalam bagian actions tersebut
    update_button = actions_section.find_element(By.XPATH, ".//a[contains(@class, 'btn-success')]")
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