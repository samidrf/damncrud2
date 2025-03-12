import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

class TestLogin(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.binary_location = "C:\Storage\Apk\Google\Chrome\Application\chrome.exe"
        service = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=service, options=options)
        self.browser.maximize_window()
        
    def tearDown(self):
        self.browser.quit()

    def test_01_login_logout(self):
        """TC1: Login dan logout dari sistem"""
        # 1. Buka halaman login
        self.browser.get("http://localhost/damncrud/login.php")
        
        # 2. Masukkan username dan password valid
        self.browser.find_element(By.NAME, "username").send_keys("admin")
        self.browser.find_element(By.NAME, "password").send_keys("nimda666!")
        
        # 3. Klik tombol 'OK I'm sign in'
        self.browser.find_element(By.CLASS_NAME, "btn-danger").click()
        
        time.sleep(2)
        # 4. Pastikan sudah berada pada laman index.php
        current_url = self.browser.current_url
        self.assertIn("index.php", current_url)
        
        # 5. Klik tombol "Sign Out"
        self.browser.find_element(By.LINK_TEXT, "Sign out").click()
        
        time.sleep(2)
        # Verifikasi: Redirect ke login.php
        current_url = self.browser.current_url
        self.assertIn("login.php", current_url)
    
    def test_02_add_new_contact(self):
        """TC2: Menambahkan kontak baru"""
        # 1. Login ke sistem
        self.browser.get("http://localhost/damncrud/login.php")
        self.browser.find_element(By.NAME, "username").send_keys("admin")
        self.browser.find_element(By.NAME, "password").send_keys("nimda666!")
        self.browser.find_element(By.CLASS_NAME, "btn-danger").click()
        time.sleep(2)
        
        # 2. Klik tombol "Add New Contact"
        self.browser.find_element(By.LINK_TEXT, "Add New Contact").click()
        
        # 3. Mengisi form yang sudah disediakan
        self.browser.find_element(By.NAME, "name").send_keys("Dimas")
        self.browser.find_element(By.NAME, "email").send_keys("dimas.rifqi@example.com")
        self.browser.find_element(By.NAME, "phone").send_keys("123456789")
        self.browser.find_element(By.NAME, "title").send_keys("Developer")
        
        # 4. Klik tombol "save"
        self.browser.find_element(By.CLASS_NAME, "btn-primary").click()
        
        time.sleep(2)
        # Verifikasi: Redirect ke index.php
        current_url = self.browser.current_url
        self.assertIn("index.php", current_url)
    
    def test_03_delete_contact(self):
        """TC3: Menghapus kontak dari list"""
        # 1. Login ke sistem
        self.browser.get("http://localhost/damncrud/login.php")
        self.browser.find_element(By.NAME, "username").send_keys("admin")
        self.browser.find_element(By.NAME, "password").send_keys("nimda666!")
        self.browser.find_element(By.CLASS_NAME, "btn-danger").click()
        time.sleep(2)
        
        # 2. Klik tombol "delete" pada list row pertama
        # Menggunakan XPath untuk menargetkan tombol delete pada baris pertama
        delete_button = self.browser.find_element(By.XPATH, "//table/tbody/tr[1]//a[contains(@href, 'delete')]")
        delete_button.click()
        
        # 3. Konfirmasi alert dan klik OK
        alert = self.browser.switch_to.alert
        alert.accept()
        
        time.sleep(2)
        # Verifikasi: Redirect ke index.php
        current_url = self.browser.current_url
        self.assertIn("index.php", current_url)
    
    def test_04_change_profile_picture(self):
        """TC4: Mengubah foto profil"""
        # 1. Login ke sistem
        self.browser.get("http://localhost/damncrud/login.php")
        self.browser.find_element(By.NAME, "username").send_keys("admin")
        self.browser.find_element(By.NAME, "password").send_keys("nimda666!")
        self.browser.find_element(By.CLASS_NAME, "btn-danger").click()
        time.sleep(2)
        
        # 2. Klik tombol "profil"
        self.browser.find_element(By.CLASS_NAME, "btn-primary").click()
        
        # 3. Memilih file yang sudah disediakan
        file_input = self.browser.find_element(By.NAME, "image")
        file_path = r"C:\Storage\Apk\Database\MySQL\XAMPP\htdocs\damncrud\helper\pp_baru.jpg"
        file_input.send_keys(file_path)
        
        # 4. Klik tombol "Change"
        self.browser.find_element(By.CLASS_NAME, "btn-secondary").click()
        
        time.sleep(2)
        # Verifikasi: Halaman profil di-refresh dengan foto profil baru
        current_url = self.browser.current_url
        self.assertIn("profil.php", current_url)
        
        # Verifikasi tambahan bisa dilakukan dengan memeriksa element gambar profile
        # atau mencari pesan sukses jika ada
    
    def test_05_edit_contact(self):
        """TC5: Mengedit kontak"""
        # 1. Login ke sistem
        self.browser.get("http://localhost/damncrud/login.php")
        self.browser.find_element(By.NAME, "username").send_keys("admin")
        self.browser.find_element(By.NAME, "password").send_keys("nimda666!")
        self.browser.find_element(By.CLASS_NAME, "btn-danger").click()
        time.sleep(2)
        
        # 2. Cari dan klik tombol edit dengan cara yang lebih spesifik
        # Cari bagian actions pada baris pertama
        actions_section = self.browser.find_element(By.XPATH, "//tr[@role='row'][1]//td[contains(@class, 'actions')]")
        # Cari tombol edit di dalam bagian actions tersebut
        update_button = actions_section.find_element(By.XPATH, ".//a[contains(@class, 'btn-success')]")
        update_button.click()
        
        # Verifikasi: Sudah masuk ke halaman update.php
        time.sleep(1)
        current_url = self.browser.current_url
        self.assertIn("update.php", current_url)
        
        # 3. Mengisi form yang sudah disediakan
        # Membersihkan field terlebih dahulu
        name_field = self.browser.find_element(By.NAME, "name")
        name_field.clear()
        name_field.send_keys("Samid")
        
        email_field = self.browser.find_element(By.NAME, "email")
        email_field.clear()
        email_field.send_keys("samid.123@example.com")
        
        # Field phone tidak perlu di-clear karena di form memang kosong (value="")
        phone_field = self.browser.find_element(By.NAME, "phone")
        phone_field.send_keys("987654321")
        
        title_field = self.browser.find_element(By.NAME, "title")
        title_field.clear()
        title_field.send_keys("Programer")
        
        # 4. Klik tombol "update"
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        
        time.sleep(2)
        # Verifikasi: Redirect ke index.php
        current_url = self.browser.current_url
        self.assertIn("index.php", current_url)


if __name__ == "__main__":
    # Konfigurasi test runner
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLogin)
    runner = unittest.TextTestRunner(verbosity=2)
    
    print("\n============= MULAI TESTING =============\n")
    
    # Jalankan test
    result = runner.run(suite)
    
    print("\n========= DETAIL HASIL TESTING =========")
    test_cases = {
        'test_01_login_logout': ['TC1 - Login dan logout dari sistem', 'Redirect ke "login.php"'],
        'test_02_add_new_contact': ['TC2 - Menambahkan kontak baru', 'Redirect ke "index.php"'],
        'test_03_delete_contact': ['TC3 - Menghapus kontak dari list', 'Redirect ke "index.php"'],
        'test_04_change_profile_picture': ['TC4 - Mengubah foto profil', 'Halaman profil.php di-refresh dengan foto profil yang baru'],
        'test_05_edit_contact': ['TC5 - Mengedit kontak', 'Redirect ke "index.php"']
    }
    
    for test_name, (desc, expected) in test_cases.items():
        status = "✅ BERHASIL" if test_name not in [f[0] for f in result.failures] else "❌ GAGAL"
        print(f"\n{desc}")
        print(f"Status: {status}")
        print(f"Output yang diharapkan: {expected}")
    
    print("\n======================================")