import unittest
import sys
import os
import time
 
# Ensure project root is in path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
 
from utils.driver_factory import get_driver
from pages.login_page import LoginPage
from pages.welcome_modal_page import WelcomeModalPage  # Assumed available per knowledge base
from pages.manage_page import ManagePage
import config
 
class TestDeviceUsers(unittest.TestCase):
 
    def setUp(self):
        # Step 1: Launch the browser and navigate to the application URL
        self.driver = get_driver()
        self.driver.get(config.BASE_URL)
 
        # Initialize page objects
        self.login_page = LoginPage(self.driver)
        self.welcome_modal = WelcomeModalPage(self.driver)
        self.manage_page = ManagePage(self.driver)
 
    def tearDown(self):
        # Close the browser after test
        self.driver.quit()
 
    def test_device_users_list(self):
        # Step 2: Enter valid username and password, then click Login
        self.login_page.login(config.USERNAME, config.PASSWORD)
 
        # Step 3: Handle the welcome modal if it appears
        try:
            self.welcome_modal.accept_welcome_modal()
        except Exception:
            print("Welcome modal not displayed, continuing...")
 
        # Step 4: Navigate to "Manage" section
        self.manage_page.open_manage()
 
        # Step 5: Open the "Device Users" section
        self.manage_page.open_device_users()
 
        # Step 6: Wait for devices to load
        time.sleep(5)  # Short wait to allow devices to load
 
        # Step 7: Retrieve all connected devices
        devices = self.manage_page.get_all_devices()
 
        # Step 8: Print all connected devices
        if len(devices) == 0:
            print("No devices connected")
        else:
            print(f"Devices found ({len(devices)}):")
            for device in devices:
                print(device)
 
        # Step 9: Validate that the devices are returned in a list
        self.assertIsInstance(devices, list, "Device list should be a list")
 
if __name__ == "__main__":
    unittest.main()