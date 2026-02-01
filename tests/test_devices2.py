import pytest
from playwright.async_api import async_playwright

@pytest.mark.asyncio
async def test_login_functionality():
    """
    Test the login functionality of The Internet demo application.
    This test validates successful login with valid credentials and verifies
    the user is redirected to the secure area.
    """
    async with async_playwright() as p:
        # Launch browser and create new page
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            # Navigate to the login page
            await page.goto("https://the-internet.herokuapp.com/login")
            
            # Verify page title and heading
            await page.wait_for_load_state("networkidle")
            page_title = await page.title()
            assert "The Internet" in page_title, f"Expected 'The Internet' in title, got: {page_title}"
            
            # Verify login page heading is visible
            login_heading = page.locator("h2")
            await login_heading.wait_for(state="visible")
            heading_text = await login_heading.text_content()
            assert "Login Page" in heading_text, f"Expected 'Login Page' heading, got: {heading_text}"
            
            # Locate form elements using stable locators
            # Using form ID as it's available and stable
            login_form = page.locator("#login")
            
            # Locate input fields by their labels (following best practices)
            username_field = page.get_by_label("Username")
            password_field = page.get_by_label("Password")
            
            # Locate login button by role and text
            login_button = page.get_by_role("button", name="Login")
            
            # Verify all elements are visible before interaction
            await username_field.wait_for(state="visible")
            await password_field.wait_for(state="visible")
            await login_button.wait_for(state="visible")
            
            # Fill in the login credentials
            # Using the test credentials provided on the page
            await username_field.fill("tomsmith")
            await password_field.fill("SuperSecretPassword!")
            
            # Verify fields are filled correctly
            username_value = await username_field.input_value()
            password_value = await password_field.input_value()
            assert username_value == "tomsmith", f"Username field not filled correctly: {username_value}"
            assert password_value == "SuperSecretPassword!", f"Password field not filled correctly: {password_value}"
            
            # Click the login button
            await login_button.click()
            
            # Wait for navigation and verify successful login
            await page.wait_for_url("**/secure")
            
            # Verify we're on the secure page
            current_url = page.url
            assert "/secure" in current_url, f"Expected to be on secure page, current URL: {current_url}"
            
            # Verify success message is displayed
            success_message = page.locator(".flash.success")
            await success_message.wait_for(state="visible")
            success_text = await success_message.text_content()
            assert "You logged into a secure area!" in success_text, f"Expected success message, got: {success_text}"
            
            # Verify secure area heading
            secure_heading = page.locator("h2")
            secure_heading_text = await secure_heading.text_content()
            assert "Secure Area" in secure_heading_text, f"Expected 'Secure Area' heading, got: {secure_heading_text}"
            
            # Verify logout button is present
            logout_button = page.get_by_role("link", name="Logout")
            await logout_button.wait_for(state="visible")
            
        finally:
            # Clean up - close browser
            await browser.close()

@pytest.mark.asyncio
async def test_invalid_login():
    """
    Test login functionality with invalid credentials.
    This test validates that appropriate error messages are shown
    when invalid credentials are provided.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            # Navigate to login page
            await page.goto("https://the-internet.herokuapp.com/login")
            await page.wait_for_load_state("networkidle")
            
            # Locate form elements
            username_field = page.get_by_label("Username")
            password_field = page.get_by_label("Password")
            login_button = page.get_by_role("button", name="Login")
            
            # Test with invalid credentials
            await username_field.fill("invaliduser")
            await password_field.fill("invalidpassword")
            await login_button.click()
            
            # Verify error message is displayed
            error_message = page.locator(".flash.error")
            await error_message.wait_for(state="visible")
            error_text = await error_message.text_content()
            assert "Your username is invalid!" in error_text, f"Expected error message, got: {error_text}"
            
            # Verify we're still on the login page
            current_url = page.url
            assert "/login" in current_url, f"Expected to remain on login page, current URL: {current_url}"
            
        finally:
            await browser.close()

@pytest.mark.asyncio
async def test_empty_credentials():
    """
    Test login functionality with empty credentials.
    This test validates form behavior when no credentials are provided.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            # Navigate to login page
            await page.goto("https://the-internet.herokuapp.com/login")
            await page.wait_for_load_state("networkidle")
            
            # Locate and click login button without filling fields
            login_button = page.get_by_role("button", name="Login")
            await login_button.click()
            
            # Verify error message for empty username
            error_message = page.locator(".flash.error")
            await error_message.wait_for(state="visible")
            error_text = await error_message.text_content()
            assert "Your username is invalid!" in error_text, f"Expected error message for empty credentials, got: {error_text}"
            
        finally:
            await browser.close()
