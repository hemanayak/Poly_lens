import unittest
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_factory import get_driver
from pages.login_page import LoginPage
from pages.welcome_modal_page import WelcomeModalPage
from pages.manage_page import ManagePage
import config


class TestManageDevices(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver()
        self.driver.get(config.BASE_URL)

        self.login_page = LoginPage(self.driver)
        self.welcome_modal = WelcomeModalPage(self.driver)
        self.manage_page = ManagePage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_login_and_manage_devices(self):

        # Login
        self.login_page.login(config.USERNAME, config.PASSWORD)

        # Handle welcome modal (safe even if it doesn't appear)
        try:
            self.welcome_modal.accept_welcome_modal()
        except Exception:
            print("Welcome modal not displayed, continuing...")

        # Open Manage section
        self.manage_page.open_manage()
        self.manage_page.open_device_users()

        # Short wait to allow devices to load (replace hard 5 min sleep)
        time.sleep(5)

        # Get all devices
        devices = self.manage_page.get_all_devices()

        if len(devices) == 0:
            print("No devices connected")
        else:
            print(f"Devices found ({len(devices)}):")
            for device in devices:
                print(device)

        # Assertion
        self.assertIsInstance(devices, list, "Device list should be a list")


if __name__ == "__main__":
    unittest.main()
