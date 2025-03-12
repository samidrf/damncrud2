import unittest, os
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

class TestContactManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        option = webdriver.FirefoxOptions()
        option.add_argument('--headless')
        cls.browser = webdriver.Firefox(options=option)
        try:
            cls.url = os.environ['URL']
        except:
            cls.url = "http://localhost/damncrud"

    def login(self):
        self.browser.get(f"{self.url}/login.php")
        self.browser.find_element(By.NAME, "username").send_keys("admin")
        self.browser.find_element(By.NAME, "password").send_keys("nimda666!")
        self.browser.find_element(By.CLASS_NAME, "btn-danger").click()
        time.sleep(2)

    def wait_for_url(self, url, timeout=10):
        WebDriverWait(self.browser, timeout).until(
            lambda driver: driver.current_url == url
        )

    def test_1_login_logout(self):
        """TC1: Login dan logout dari sistem"""
        # 1. Buka halaman login
        self.browser.get(f"{self.url}/login.php")
        
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

    def test_2_add_new_contact(self):
        """TC2: Menambahkan kontak baru"""
        self.login()
        
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

    def test_3_delete_contact(self):
        """TC3: Menghapus kontak dari list"""
        self.login()
        
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

    def test_4_change_profile_picture(self):
        """TC4: Mengubah foto profil"""
        self.login()
        
        # 2. Klik tombol "profil"
        self.browser.find_element(By.CLASS_NAME, "btn-primary").click()
        
        # 3. Memilih file yang sudah disediakan
        file_input = self.browser.find_element(By.NAME, "image")
        # Gunakan path relatif untuk file test di CI/CD
        file_path = os.path.join(os.getcwd(), 'helper', 'pp_baru.jpg')
        file_input.send_keys(file_path)
        
        # 4. Klik tombol "Change"
        self.browser.find_element(By.CLASS_NAME, "btn-secondary").click()
        
        time.sleep(2)
        # Verifikasi: Halaman profil di-refresh
        current_url = self.browser.current_url
        self.assertIn("profil.php", current_url)

    def test_5_edit_contact(self):
        """TC5: Mengedit kontak"""
        self.login()
        
        try:
            # Cari bagian actions pada baris pertama
            actions_section = self.browser.find_element(By.XPATH, "//tr[@role='row'][1]//td[contains(@class, 'actions')]")
            # Cari tombol edit di dalam bagian actions tersebut
            update_button = actions_section.find_element(By.XPATH, ".//a[contains(@class, 'btn-success')]")
        except:
            # Fallback jika struktur DOM berbeda
            update_button = self.browser.find_element(By.XPATH, "//a[contains(@href, 'edit')]")
        
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

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')
