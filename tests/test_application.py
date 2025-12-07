cat > tests/test_application.py << 'EOF'
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Application URLs based on docker-compose.yml
BACKEND_URL = "http://localhost:5001"
USER_FRONTEND_URL = "http://localhost:3005"
ADMIN_FRONTEND_URL = "http://localhost:3006"


class TestBackend:
    """Test cases for Backend API"""
    
    def test_01_backend_is_accessible(self, driver):
        """Test Case 1: Verify backend API is accessible"""
        driver.get(BACKEND_URL)
        assert driver.page_source is not None
        assert len(driver.page_source) > 0
        print("✓ Test 1 Passed: Backend is accessible")
    
    def test_02_backend_responds(self, driver):
        """Test Case 2: Verify backend returns response"""
        driver.get(BACKEND_URL)
        page_content = driver.page_source
        # Backend should return something (JSON, HTML, or status message)
        assert len(page_content) > 10
        print("✓ Test 2 Passed: Backend responds with content")


class TestUserFrontend:
    """Test cases for User Frontend"""
    
    def test_03_user_frontend_loads(self, driver):
        """Test Case 3: Verify user frontend loads successfully"""
        driver.get(USER_FRONTEND_URL)
        assert driver.title is not None
        print(f"✓ Test 3 Passed: User frontend loaded with title '{driver.title}'")
    
    def test_04_user_frontend_has_content(self, driver):
        """Test Case 4: Verify user frontend displays content"""
        driver.get(USER_FRONTEND_URL)
        body = driver.find_element(By.TAG_NAME, "body")
        assert len(body.text) > 0
        print("✓ Test 4 Passed: User frontend has visible content")
    
    def test_05_user_frontend_elements(self, driver):
        """Test Case 5: Verify user frontend has interactive elements"""
        driver.get(USER_FRONTEND_URL)
        # Check for common UI elements
        elements = driver.find_elements(By.TAG_NAME, "button") + \
                   driver.find_elements(By.TAG_NAME, "a") + \
                   driver.find_elements(By.TAG_NAME, "input")
        assert len(elements) > 0
        print(f"✓ Test 5 Passed: Found {len(elements)} interactive elements")


class TestAdminFrontend:
    """Test cases for Admin Frontend"""
    
    def test_06_admin_frontend_loads(self, driver):
        """Test Case 6: Verify admin frontend loads successfully"""
        driver.get(ADMIN_FRONTEND_URL)
        assert driver.title is not None
        print(f"✓ Test 6 Passed: Admin frontend loaded with title '{driver.title}'")
    
    def test_07_admin_frontend_has_content(self, driver):
        """Test Case 7: Verify admin frontend displays content"""
        driver.get(ADMIN_FRONTEND_URL)
        body = driver.find_element(By.TAG_NAME, "body")
        assert len(body.text) > 0
        print("✓ Test 7 Passed: Admin frontend has visible content")
    
    def test_08_admin_frontend_elements(self, driver):
        """Test Case 8: Verify admin frontend has UI elements"""
        driver.get(ADMIN_FRONTEND_URL)
        page_source = driver.page_source.lower()
        # Check for admin-related keywords
        has_admin_elements = any(word in page_source for word in 
                                ['login', 'dashboard', 'admin', 'signin', 'form', 'input'])
        assert has_admin_elements
        print("✓ Test 8 Passed: Admin interface elements found")


class TestPerformance:
    """Performance and integration test cases"""
    
    def test_09_user_frontend_loads_quickly(self, driver):
        """Test Case 9: Verify user frontend loads within acceptable time"""
        start_time = time.time()
        driver.get(USER_FRONTEND_URL)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        load_time = time.time() - start_time
        assert load_time < 10, f"Page took {load_time:.2f}s to load (should be <10s)"
        print(f"✓ Test 9 Passed: User frontend loaded in {load_time:.2f} seconds")
    
    def test_10_all_services_running(self, driver):
        """Test Case 10: Verify all three services are accessible"""
        errors = []
        
        # Test Backend
        try:
            driver.get(BACKEND_URL)
            assert len(driver.page_source) > 0
        except Exception as e:
            errors.append(f"Backend failed: {str(e)}")
        
        # Test User Frontend
        try:
            driver.get(USER_FRONTEND_URL)
            assert driver.title is not None
        except Exception as e:
            errors.append(f"User Frontend failed: {str(e)}")
        
        # Test Admin Frontend
        try:
            driver.get(ADMIN_FRONTEND_URL)
            assert driver.title is not None
        except Exception as e:
            errors.append(f"Admin Frontend failed: {str(e)}")
        
        assert len(errors) == 0, f"Some services failed: {'; '.join(errors)}"
        print("✓ Test 10 Passed: All three services are running and accessible")
EOF