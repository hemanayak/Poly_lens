from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")   # New headless mode
    options.add_argument("--no-sandbox")     # Required in CI
    options.add_argument("--disable-dev-shm-usage")  # Prevents /dev/shm issues
    options.add_argument("--disable-gpu")    # GPU not available in CI
    options.add_argument("--window-size=1920,1080") # Optional: set window size

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

