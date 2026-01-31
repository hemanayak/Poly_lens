import pytest
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

@pytest.mark.asyncio
async def test_poly_lens_login():
    """
    Test login functionality for Poly Lens Cloud website.
    Tests successful login with valid credentials and validates dashboard access.
    """
    async with async_playwright() as p:
        # Launch browser with visible mode for debugging (set headless=True for CI)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # Navigate to Poly Lens login page
            await page.goto("https://lens.poly.com/")
            
            # Wait for page to load completely (SPA with dynamic content)
            await page.wait_for_load_state("networkidle")
            
            # Wait for login form to appear and locate email field using hierarchy
            # Priority: data-testid > aria-label > role > name > id > visible text
            email_field = None
            try:
                email_field = page.get_by_test_id("email-input")
                await email_field.wait_for(timeout=5000)
            except PlaywrightTimeoutError:
                try:
                    email_field = page.get_by_label("Email")
                    await email_field.wait_for(timeout=5000)
                except PlaywrightTimeoutError:
                    try:
                        email_field = page.get_by_role("textbox", name="email")
                        await email_field.wait_for(timeout=5000)
                    except PlaywrightTimeoutError:
                        try:
                            email_field = page.locator('input[name="email"]')
                            await email_field.wait_for(timeout=5000)
                        except PlaywrightTimeoutError:
                            try:
                                email_field = page.locator('#email')
                                await email_field.wait_for(timeout=5000)
                            except PlaywrightTimeoutError:
                                # Fallback to generic email input
                                email_field = page.locator('input[type="email"]')
                                await email_field.wait_for(timeout=10000)
            
            # Locate password field using hierarchy
            password_field = None
            try:
                password_field = page.get_by_test_id("password-input")
                await password_field.wait_for(timeout=5000)
            except PlaywrightTimeoutError:
                try:
                    password_field = page.get_by_label("Password")
                    await password_field.wait_for(timeout=5000)
                except PlaywrightTimeoutError:
                    try:
                        password_field = page.get_by_role("textbox", name="password")
                        await password_field.wait_for(timeout=5000)
                    except PlaywrightTimeoutError:
                        try:
                            password_field = page.locator('input[name="password"]')
                            await password_field.wait_for(timeout=5000)
                        except PlaywrightTimeoutError:
                            try:
                                password_field = page.locator('#password')
                                await password_field.wait_for(timeout=5000)
                            except PlaywrightTimeoutError:
                                # Fallback to generic password input
                                password_field = page.locator('input[type="password"]')
                                await password_field.wait_for(timeout=10000)
            
            # Locate login button using hierarchy
            login_button = None
            try:
                login_button = page.get_by_test_id("login-button")
                await login_button.wait_for(timeout=5000)
            except PlaywrightTimeoutError:
                try:
                    login_button = page.get_by_role("button", name="Login")
                    await login_button.wait_for(timeout=5000)
                except PlaywrightTimeoutError:
                    try:
                        login_button = page.get_by_role("button", name="Sign In")
                        await login_button.wait_for(timeout=5000)
                    except PlaywrightTimeoutError:
                        try:
                            login_button = page.locator('button[type="submit"]')
                            await login_button.wait_for(timeout=5000)
                        except PlaywrightTimeoutError:
                            # Fallback to button containing login text
                            login_button = page.locator('button:has-text("Login"), button:has-text("Sign In")')
                            await login_button.wait_for(timeout=10000)
            
            # Fill login credentials (using test credentials)
            test_email = "test.user@polylens.com"
            test_password = "SecurePassword123!"
            
            await email_field.fill(test_email)
            await password_field.fill(test_password)
            
            # Click login button
            await login_button.click()
            
            # Wait for navigation or dashboard to load
            await page.wait_for_load_state("networkidle")
            
            # Validate successful login by checking for dashboard elements
            dashboard_loaded = False
            try:
                # Try to find dashboard indicators using hierarchy
                dashboard_element = None
                try:
                    dashboard_element = page.get_by_test_id("dashboard")
                    await dashboard_element.wait_for(timeout=15000)
                    dashboard_loaded = True
                except PlaywrightTimeoutError:
                    try:
                        dashboard_element = page.get_by_role("main")
                        await dashboard_element.wait_for(timeout=10000)
                        dashboard_loaded = True
                    except PlaywrightTimeoutError:
                        try:
                            dashboard_element = page.locator('.dashboard, .main-content, .home')
                            await dashboard_element.wait_for(timeout=10000)
                            dashboard_loaded = True
                        except PlaywrightTimeoutError:
                            # Check if URL changed to indicate successful login
                            current_url = page.url
                            if "dashboard" in current_url or "home" in current_url or "main" in current_url:
                                dashboard_loaded = True
            except Exception as e:
                print(f"Dashboard validation error: {e}")
            
            # Assert successful login
            assert dashboard_loaded, "Login failed - dashboard not loaded or URL did not change"
            
            # Additional validation: Check for user profile or logout option
            try:
                user_profile = None
                try:
                    user_profile = page.get_by_test_id("user-profile")
                    await user_profile.wait_for(timeout=5000)
                except PlaywrightTimeoutError:
                    try:
                        user_profile = page.get_by_role("button", name="Profile")
                        await user_profile.wait_for(timeout=5000)
                    except PlaywrightTimeoutError:
                        user_profile = page.locator('.user-menu, .profile-menu, [aria-label*="user"]')
                        await user_profile.wait_for(timeout=5000)
                
                assert user_profile.is_visible(), "User profile menu not visible after login"
                
            except PlaywrightTimeoutError:
                # If no user profile found, check for logout button as alternative validation
                try:
                    logout_button = page.get_by_role("button", name="Logout")
                    await logout_button.wait_for(timeout=5000)
                    assert logout_button.is_visible(), "Neither user profile nor logout button found"
                except PlaywrightTimeoutError:
                    print("Warning: Could not find user profile or logout button for additional validation")
            
        except Exception as e:
            # Capture screenshot on failure for debugging
            await page.screenshot(path="login_test_failure.png")
            raise e
        
        finally:
            # Clean up
            await browser.close()

@pytest.mark.asyncio
async def test_poly_lens_login_invalid_credentials():
    """
    Test login functionality with invalid credentials.
    Validates that appropriate error messages are displayed.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # Navigate to login page
            await page.goto("https://lens.poly.com/")
            await page.wait_for_load_state("networkidle")
            
            # Locate form elements (using simplified approach for negative test)
            email_field = page.locator('input[type="email"], input[name="email"], #email')
            password_field = page.locator('input[type="password"], input[name="password"], #password')
            login_button = page.locator('button[type="submit"], button:has-text("Login"), button:has-text("Sign In")')
            
            # Wait for elements to be available
            await email_field.first.wait_for(timeout=10000)
            await password_field.first.wait_for(timeout=10000)
            await login_button.first.wait_for(timeout=10000)
            
            # Fill with invalid credentials
            await email_field.first.fill("invalid@example.com")
            await password_field.first.fill("wrongpassword")
            await login_button.first.click()
            
            # Wait for error message to appear
            error_message = None
            try:
                error_message = page.get_by_test_id("error-message")
                await error_message.wait_for(timeout=10000)
            except PlaywrightTimeoutError:
                try:
                    error_message = page.get_by_role("alert")
                    await error_message.wait_for(timeout=5000)
                except PlaywrightTimeoutError:
                    error_message = page.locator('.error, .alert-danger, [role="alert"]')
                    await error_message.wait_for(timeout=10000)
            
            # Assert error message is displayed
            assert error_message.is_visible(), "Error message not displayed for invalid credentials"
            
            # Verify we're still on login page (not redirected)
            current_url = page.url
            assert "lens.poly.com" in current_url, "Unexpected redirect after failed login"
            
        except Exception as e:
            await page.screenshot(path="invalid_login_test_failure.png")
            raise e
        
        finally:
            await browser.close()

@pytest.mark.asyncio
async def test_poly_lens_empty_credentials():
    """
    Test login form validation with empty credentials.
    Validates that form validation prevents submission with empty fields.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # Navigate to login page
            await page.goto("https://lens.poly.com/")
            await page.wait_for_load_state("networkidle")
            
            # Locate login button
            login_button = page.locator('button[type="submit"], button:has-text("Login"), button:has-text("Sign In")')
            await login_button.first.wait_for(timeout=10000)
            
            # Try to submit without filling any fields
            await login_button.first.click()
            
            # Check for validation messages or that form wasn't submitted
            validation_error = False
            try:
                # Look for HTML5 validation or custom validation messages
                validation_message = page.locator(':invalid, .validation-error, .field-error')
                await validation_message.first.wait_for(timeout=5000)
                validation_error = True
            except PlaywrightTimeoutError:
                # Check if we're still on the same page (form didn't submit)
                current_url = page.url
                if "lens.poly.com" in current_url and "dashboard" not in current_url:
                    validation_error = True
            
            assert validation_error, "Form validation should prevent submission with empty credentials"
            
        except Exception as e:
            await page.screenshot(path="empty_credentials_test_failure.png")
            raise e
        
        finally:
            await browser.close()
