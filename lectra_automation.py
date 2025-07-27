import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager


class LectraTestAutomation:
    """
    Test automation class for Lectra website scenario testing.
    """
    
    def __init__(self, headless=False, timeout=10):
        """Initialize the test automation with configurable options."""
        self.timeout = timeout
        self.driver = None
        self.wait = None
        self.original_window = None
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Setup Chrome driver with options
        self._setup_driver(headless)
    
    def _setup_driver(self, headless):
        """Configure and initialize the Chrome WebDriver."""
        chrome_options = webdriver.ChromeOptions()
        
        # Anti-detection measures
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        if headless:
            chrome_options.add_argument("--headless")
        else:
            chrome_options.add_experimental_option("detach", True)
        
        try:
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), 
                options=chrome_options
            )
            self.wait = WebDriverWait(self.driver, self.timeout)
            
            # Remove webdriver property
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            
            self.driver.maximize_window()
            self.logger.info("Chrome driver initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Chrome driver: {str(e)}")
            raise
    
    def _safe_click(self, element, description="element"):
        """Safely click an element with retry logic."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Scroll element into view
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                time.sleep(0.5)
                
                # Try regular click first
                element.click()
                self.logger.info(f"Successfully clicked {description}")
                return True
                
            except ElementClickInterceptedException:
                if attempt < max_retries - 1:
                    self.logger.warning(f"Click intercepted for {description}, retrying with JavaScript...")
                    try:
                        self.driver.execute_script("arguments[0].click();", element)
                        self.logger.info(f"Successfully clicked {description} using JavaScript")
                        return True
                    except Exception as js_e:
                        self.logger.warning(f"JavaScript click failed: {str(js_e)}")
                        time.sleep(1)
                else:
                    self.logger.error(f"Failed to click {description} after {max_retries} attempts")
                    return False
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed for {description}: {str(e)}")
                if attempt == max_retries - 1:
                    return False
                time.sleep(1)
        return False
    
    def _find_element_by_selectors(self, selectors, description="element"):
        """Find element using multiple selector strategies."""
        for selector in selectors:
            try:
                if selector.startswith("#"):
                    element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                elif selector.startswith("//") or selector.startswith("."):
                    element = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                else:
                    element = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                
                self.logger.info(f"Found {description} using selector: {selector}")
                return element
            except TimeoutException:
                continue
        
        self.logger.warning(f"Could not find {description} with any provided selectors")
        return None
    
    def _human_like_delay(self, min_delay=1, max_delay=3):
        """Add human-like delay between actions."""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def _type_naturally(self, element, text):
        """Type text with natural human-like timing."""
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
    
    def step_1_open_google(self):
        """Step 1: Open Google Search page."""
        self.logger.info("=== Step 1: Opening Google Search ===")
        try:
            self.driver.get("https://www.google.com")
            return True
        except Exception as e:
            self.logger.error(f"Failed to open Google: {str(e)}")
            return False
    
    def step_2_handle_google_cookies(self):
        """Handle Google cookie consent if present."""
        self.logger.info("Checking for Google cookie consent...")
        
        selectors = [
            "//button[contains(text(), 'Accept all')]",
            "#L2AGLb"
        ]
        
        cookie_button = self._find_element_by_selectors(selectors, "Google cookie consent")
        if cookie_button:
            return self._safe_click(cookie_button, "Google cookie consent")
        else:
            self.logger.info("No Google cookie consent found or already handled")
            return True
    
    def step_3_search_lectra(self):
        """Step 2: Search for 'Lectra'."""
        self.logger.info("=== Step 2: Searching for Lectra ===")
        try:
            search_box = self.wait.until(EC.presence_of_element_located((By.NAME, "q")))
            self._type_naturally(search_box, "Lectra")
            self._human_like_delay(1, 2)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for search results
            self.wait.until(EC.presence_of_element_located((By.ID, "search")))
            self.logger.info("Search completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to search for Lectra: {str(e)}")
            return False
    
    def step_4_click_lectra_website(self):
        """Step 3: Navigate to Lectra website from search results."""
        self.logger.info("=== Step 3: Navigating to Lectra website ===")
        
        selectors = [
            "//a[contains(@href, 'lectra.com') and not(contains(@href, 'careers'))]",
            "//h3[contains(text(), 'Lectra')]/parent::a",
        ]
        
        lectra_link = self._find_element_by_selectors(selectors, "Lectra website link")
        if lectra_link and self._safe_click(lectra_link, "Lectra website link"):
            try:
                self.wait.until(EC.url_contains("lectra"))
                self.logger.info(f"Successfully navigated to: {self.driver.current_url}")
                return True
            except TimeoutException:
                self.logger.error("Failed to load Lectra website")
                return False
        return False
    
    def step_5_handle_lectra_cookies(self):
        """Step 4: Handle Lectra website cookies."""
        self.logger.info("=== Step 4: Handling Lectra cookies ===")
        self._human_like_delay()
        
        selectors = [
            "#ppms_cm_agree-to-all",
            "//button[contains(text(), 'Accept all')]"
        ]
        
        cookie_button = self._find_element_by_selectors(selectors, "Lectra cookie consent")
        if cookie_button:
            return self._safe_click(cookie_button, "Lectra cookie consent")
        else:
            self.logger.info("No Lectra cookie consent found or already handled")
            return True
    
    def step_6_switch_to_english(self):
        """Step 5: Switch language to English."""
        self.logger.info("=== Step 5: Switching to English ===")
        
        # # Check if already in English
        # if '/en/' in self.driver.current_url or '/en' in self.driver.current_url:
        #     self.logger.info("Site is already in English")
        #     return True
        
        # Click Languages button
        language_selectors = [
            '//*[@id="block-lectra-b5-languageswitcherinterfacetext-2"]/button',
            '//button[contains(text(), "Languages")]'
        ]
        
        language_button = self._find_element_by_selectors(language_selectors, "Languages button")
        if not language_button or not self._safe_click(language_button, "Languages button"):
            return False
        
        self._human_like_delay(0.5, 1.5)
        
        # Click English option
        english_selectors = [
            '//*[@id="block-lectra-b5-languageswitcherinterfacetext-2"]/div/ul/li[1]/a',
            '//a[@hreflang="en" and contains(text(), "English")]',
            '//a[@class="language-link" and @hreflang="en"]'
        ]
        
        english_link = self._find_element_by_selectors(english_selectors, "English language option")
        if english_link and self._safe_click(english_link, "English language"):
            self._human_like_delay()
            self.logger.info(f"Language switched. Current URL: {self.driver.current_url}")
            return True
        return False
    
    def step_7_navigate_fashion_menu(self):
        """Step 6: Navigate Fashion -> Lectra & Fashion."""
        self.logger.info("=== Step 6: Navigating Fashion menu ===")
        
        # Click Fashion button
        fashion_selectors = [
            '//*[@id="block-lectra-b5-mainnavigation"]/ul/li[1]/button',
            '//button[contains(text(), "Fashion")]'
        ]
        
        fashion_button = self._find_element_by_selectors(fashion_selectors, "Fashion button")
        if not fashion_button or not self._safe_click(fashion_button, "Fashion button"):
            return False
        
        self._human_like_delay()
        
        # Click Lectra & Fashion
        lectra_fashion_selectors = [
            '//*[@id="block-lectra-b5-mainnavigation"]/ul/li[1]/div/div/div[1]/ul/li[1]/a',
            '//a[@href="/en/fashion" and contains(text(), "Lectra")]'
        ]
        
        lectra_fashion_link = self._find_element_by_selectors(lectra_fashion_selectors, "Lectra & Fashion link")
        if lectra_fashion_link and self._safe_click(lectra_fashion_link, "Lectra & Fashion"):
            self._human_like_delay()
            self.logger.info(f"Navigated to Fashion page: {self.driver.current_url}")
            return True
        return False
    
    def step_8_click_automotive_furniture(self):
        """Step 7: Click Automotive and Furniture tabs."""
        self.logger.info("=== Step 7: Clicking Automotive and Furniture tabs ===")
        
        # Click Automotive
        automotive_selectors = [
            '//*[@id="block-lectra-b5-mainnavigation"]/ul/li[2]/button',
            '//button[contains(text(), "Automotive")]'
        ]
        
        automotive_button = self._find_element_by_selectors(automotive_selectors, "Automotive button")
        if automotive_button:
            self._safe_click(automotive_button, "Automotive tab")
        
        self._human_like_delay(0.3, 0.8)
        
        # Click Furniture
        furniture_selectors = [
            '//*[@id="block-lectra-b5-mainnavigation"]/ul/li[3]/button',
            '//button[contains(text(), "Furniture")]'
        ]
        
        furniture_button = self._find_element_by_selectors(furniture_selectors, "Furniture button")
        if furniture_button:
            self._safe_click(furniture_button, "Furniture tab")
        
        self._human_like_delay(0.3, 0.8)
        return True
    
    def step_9_navigate_about_us(self):
        """Step 8: Navigate About Us -> Discover Lectra."""
        self.logger.info("=== Step 8: Navigating About Us menu ===")
        
        # Click About Us
        about_selectors = [
            '//*[@id="block-lectra-b5-headersecondarynavigation-2"]/ul/li[1]/button',
            '//button[contains(text(), "About us")]'
        ]
        
        about_button = self._find_element_by_selectors(about_selectors, "About us button")
        if not about_button or not self._safe_click(about_button, "About us button"):
            return False
        
        self._human_like_delay()
        
        # Click Discover Lectra
        discover_selectors = [
            '//*[@id="block-lectra-b5-headersecondarynavigation-2"]/ul/li[1]/div/ul/li[1]/a',
            '//a[@href="/en/discover-lectra" and contains(text(), "Discover Lectra")]'
        ]
        
        discover_link = self._find_element_by_selectors(discover_selectors, "Discover Lectra link")
        if discover_link and self._safe_click(discover_link, "Discover Lectra"):
            self._human_like_delay()
            self.logger.info(f"Navigated to Discover Lectra: {self.driver.current_url}")
            return True
        return False
    
    def step_10_navigate_to_careers(self):
        """Step 9: Navigate to careers through View job openings."""
        self.logger.info("=== Step 9: Navigating to careers ===")
        
        # Scroll to find View job openings
        self.logger.info("Scrolling to find 'View job openings' button")
        for i in range(8):
            self.driver.execute_script("window.scrollBy(0, 1000);")
            self._human_like_delay(0.5, 1)
        
        view_job_selectors = [
            '//*[@id="block-lectra-b5-content"]//a[contains(text(), "View job openings")]',
            '//*[@id="block-lectra-b5-content"]/article/div/div[2]/div[7]/div/div/div/div/div[1]/div[2]/div[2]/a'
        ]
        
        view_job_button = self._find_element_by_selectors(view_job_selectors, "View job openings button")
        if not view_job_button or not self._safe_click(view_job_button, "View job openings"):
            return False
        
        self._human_like_delay()
        
        # Navigate to job opportunities
        return self._navigate_to_job_opportunities()
    
    def _navigate_to_job_opportunities(self):
        """Navigate to job opportunities page."""
        # Scroll to find Our job opportunities
        for i in range(2):
            self.driver.execute_script("window.scrollBy(0, 500);")
            self._human_like_delay(0.5, 1)
        
        job_opp_selectors = [
            '//a[@href="https://careers.lectra.com/" and contains(@class, "gtm-cta")]',
            '//a[contains(text(), "Our job opportunities")]',
            '//*[@id="block-lectra-b5-content"]/article/div/div[2]/div[1]/div/div/div/div/div/div[2]/div[2]/a'
        ]
        
        self.original_window = self.driver.current_window_handle
        
        job_opp_link = self._find_element_by_selectors(job_opp_selectors, "Our job opportunities link")
        if not job_opp_link or not self._safe_click(job_opp_link, "Our job opportunities"):
            return False
        
        # Handle potential new tab
        self._human_like_delay()
        return self._switch_to_careers_tab()
    
    def _switch_to_careers_tab(self):
        """Switch to careers tab if opened in new window."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            for window in all_windows:
                if window != self.original_window:
                    self.driver.switch_to.window(window)
                    break
        
        try:
            self.wait.until(EC.url_contains("careers.lectra.com"))
            self.logger.info("Successfully navigated to careers page")
            return True
        except TimeoutException:
            self.logger.error("Failed to load careers page")
            return False
    
    def step_11_handle_career_cookies(self):
        """Handle cookies on career page."""
        self.logger.info("=== Step 10: Handling career page cookies ===")
        
        career_cookie_selectors = [
            '#cookie-accept',
            '//button[@id="cookie-accept"]'
        ]
        
        cookie_button = self._find_element_by_selectors(career_cookie_selectors, "Career cookie button")
        if cookie_button:
            return self._safe_click(cookie_button, "Career cookie consent")
        else:
            self.logger.info("No career cookie consent found")
            return True
    
    def step_12_search_and_click_first_job(self):
        """Step 11: Search jobs and click first opportunity."""
        self.logger.info("=== Step 11: Searching jobs and clicking first opportunity ===")
        
        # Click Search jobs
        search_selectors = [
            '//*[@id="search-wrapper"]/div/form/div/div/div[2]/div[2]/div[1]/input',  
            '//input[@type="submit" and @class="btn keywordsearch-button" and @value="Search jobs"]',  
            '//input[@class="btn keywordsearch-button" and @value="Search jobs"]',  
            '//input[@type="submit" and @value="Search jobs"]' 
        ]
        
        search_button = self._find_element_by_selectors(search_selectors, "Search jobs button")
        if not search_button or not self._safe_click(search_button, "Search jobs"):
            return False
        
        # Wait for results and click first job
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, "searchresults")))
            self._human_like_delay()
            
            first_job_selectors = [
                '//table[@id="searchresults"]//tbody/tr[1]/td[@class="colTitle"]',
                '//td[@class="colTitle"]/span/a[@class="jobTitle-link"]'
            ]
            
            first_job = self._find_element_by_selectors(first_job_selectors, "First job opportunity")
            if first_job and self._safe_click(first_job, "First job opportunity"):
                self._human_like_delay()
                
                
                # Close job details tab and return to original
                self._human_like_delay()
                self.logger.info("Closing job details tab...")
                self.driver.close()
                self.driver.switch_to.window(self.original_window)
                self.logger.info("Returned to original tab")
                return True
                
        except Exception as e:
            self.logger.error(f"Error in job search: {str(e)}")
        
        return False
    
    def run_complete_scenario(self):
        """Execute the complete test scenario."""
        self.logger.info("Starting Lectra website automation scenario")
        
        steps = [
            ("Open Google", self.step_1_open_google),
            ("Handle Google Cookies", self.step_2_handle_google_cookies),
            ("Search for Lectra", self.step_3_search_lectra),
            ("Navigate to Lectra Website", self.step_4_click_lectra_website),
            ("Handle Lectra Cookies", self.step_5_handle_lectra_cookies),
            ("Switch to English", self.step_6_switch_to_english),
            ("Navigate Fashion Menu", self.step_7_navigate_fashion_menu),
            ("Click Automotive & Furniture", self.step_8_click_automotive_furniture),
            ("Navigate About Us", self.step_9_navigate_about_us),
            ("Navigate to Careers", self.step_10_navigate_to_careers),
            ("Handle Career Cookies", self.step_11_handle_career_cookies),
            ("Search Jobs & Click First", self.step_12_search_and_click_first_job)
        ]
        
        results = {}
        for step_name, step_function in steps:
            try:
                self.logger.info(f"Executing: {step_name}")
                result = step_function()
                results[step_name] = result
                
                if not result:
                    self.logger.warning(f"Step '{step_name}' failed, but continuing...")
                else:
                    self.logger.info(f"Step '{step_name}' completed successfully")
                    
            except Exception as e:
                self.logger.error(f"Step '{step_name}' encountered error: {str(e)}")
                results[step_name] = False
        
        # Print summary
        self.logger.info("=== EXECUTION SUMMARY ===")
        for step, result in results.items():
            status = "✓ PASSED" if result else "✗ FAILED"
            self.logger.info(f"{step}: {status}")
        
        return results
    
    def cleanup(self):
        """Clean up resources."""
        if self.driver:
            self.logger.info("Cleaning up - browser will remain open for review")
            # Uncomment next line if you want to close browser automatically
            # self.driver.quit()


def main():
    """Main execution function."""
    # Initialize and run the test
    test_automation = LectraTestAutomation(headless=False, timeout=10)
    
    try:
        results = test_automation.run_complete_scenario()
        print("\nTest execution completed. Check logs for details.")
        return results
    
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Test failed with error: {str(e)}")
    finally:
        test_automation.cleanup()


if __name__ == "__main__":
    main()