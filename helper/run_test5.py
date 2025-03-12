import unittest
from testcase import TestLogin

if __name__ == "__main__":
    # Membuat suite yang hanya berisi test_05_edit_contact
    suite = unittest.TestSuite()
    suite.addTest(TestLogin('test_05_edit_contact'))
    
    # Konfigurasi test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    print("\n============= MULAI TESTING TEST CASE 5 =============\n")
    
    # Jalankan test
    result = runner.run(suite)
    
    print("\n========= DETAIL HASIL TESTING =========")
    status = "✅ BERHASIL" if len(result.failures) == 0 and len(result.errors) == 0 else "❌ GAGAL"
    print(f"\nTC5 - Mengedit kontak")
    print(f"Status: {status}")
    print(f"Output yang diharapkan: Redirect ke 'index.php'")
    
    print("\n======================================") 