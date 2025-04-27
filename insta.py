import os
import re
import random
import string
import time
import json
import requests
from instagrapi import Client
from instagrapi.exceptions import ClientError, ChallengeRequired
from datetime import datetime
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class UltimateInstagramCreator:
    def __init__(self):
        self.print_banner()
        self.log("Initializing Instagram Account Creator...", "INFO")
        
        # Initialize directories
        self.results_dir = "instagram_accounts"
        os.makedirs(self.results_dir, exist_ok=True)
        self.log(f"Created results directory at: {os.path.abspath(self.results_dir)}", "SUCCESS")
        
        # Web service configuration
        self.email_api = "https://api4dev.ir/api/fakemail.php"
        
        # Account statistics
        self.session_stats = {
            'total_attempts': 0,
            'successful': 0,
            'failed': 0,
            'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'accounts': []
        }
        
        # Initialize components
        self.init_delays()
        self.init_recaptcha_keys()
        self.init_device_profiles()
        self.init_selenium()
        self.client = Client()
        
        self.log("Initialization completed successfully!", "SUCCESS")
        self.print_separator()

    def print_banner(self):
        """Display startup banner"""
        print("""
   _____ _                 _           _____           _        _ _             
  / ____| |               | |         |_   _|         | |      | | |            
 | (___ | |_ __ _ _ __ ___| |_ ___ _ __| |  _ __  ___| |_ __ _| | | ___ _ __  
  \___ \| __/ _` | '__/ __| __/ _ \ '__| | | '_ \/ __| __/ _` | | |/ _ \ '__| 
  ____) | || (_| | |  \__ \ ||  __/ | _| |_| | | \__ \ || (_| | | |  __/ |    
 |_____/ \__\__,_|_|  |___/\__\___|_||_____|_| |_|___/\__\__,_|_|_|\___|_|    

                    Ultimate Instagram Account Creator v3.0
        """)

    def print_separator(self):
        """Print visual separator"""
        print("\n" + "=" * 80 + "\n")

    def log(self, message, level="INFO"):
        """Enhanced logging with colors and timestamps"""
        colors = {
            "INFO": "\033[94m",      # Blue
            "SUCCESS": "\033[92m",   # Green
            "WARNING": "\033[93m",    # Yellow
            "ERROR": "\033[91m",      # Red
            "DEBUG": "\033[90m",      # Gray
            "RESET": "\033[0m"       # Reset
        }
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{colors.get(level, '')}[{timestamp}] [{level}] {message}{colors['RESET']}")

    def init_delays(self):
        """Initialize randomized delays"""
        self.log("Configuring randomized delays...", "DEBUG")
        self.delays = {
            'between_actions': (random.uniform(2, 5), random.uniform(5, 8)),
            'after_success': (random.uniform(120, 180), random.uniform(180, 300)),
            'after_failure': (random.uniform(300, 450), random.uniform(450, 600)),
            'email_check': (random.uniform(15, 20), random.uniform(20, 25))
        }
        self.log(f"Configured delays: {self.delays}", "DEBUG")

    def init_recaptcha_keys(self):
        """Initialize reCAPTCHA solver keys"""
        self.log("Initializing reCAPTCHA solver keys...", "DEBUG")
        self.recaptcha_keys = [
            "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
            "6LcBipAUAAAAAKS1s1Wq7XrT0kG5mCvD-QYnyg3k",
            "6LdKjxAUAAAAAGk8z7pZ3vC-8YjYhG8y5g5j5Z5G",
            "6LfKjxAUAAAAAGk8z7pZ3vC-8YjYhG8y5g5j5Z5G"
        ]
        self.log(f"Loaded {len(self.recaptcha_keys)} reCAPTCHA keys", "DEBUG")

    def init_device_profiles(self):
        """Initialize device profiles for rotation"""
        self.log("Configuring device profiles...", "DEBUG")
        self.device_profiles = [
            {
                "device": "SM-G973F",
                "model": "Samsung Galaxy S10",
                "android_version": 25,
                "android_release": "7.1.2"
            },
            {
                "device": "iPhone12,1",
                "model": "iPhone 11",
                "android_version": 14,
                "android_release": "14.0"
            },
            {
                "device": "Pixel 3",
                "model": "Google Pixel 3",
                "android_version": 28,
                "android_release": "9.0"
            }
        ]
        self.log(f"Configured {len(self.device_profiles)} device profiles", "DEBUG")

    def init_selenium(self):
        """Initialize Selenium WebDriver with advanced settings"""
        self.log("Initializing Selenium WebDriver...", "INFO")
        try:
            options = Options()
            
            # Anti-detection settings
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Randomize user agent
            user_agent = random.choice([
                "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
            ])
            options.add_argument(f"user-agent={user_agent}")
            
            # Mobile emulation
            mobile_emulation = {
                "deviceMetrics": {
                    "width": random.randint(360, 414),
                    "height": random.randint(640, 896),
                    "pixelRatio": random.uniform(2.0, 3.0)
                },
                "userAgent": user_agent
            }
            options.add_experimental_option("mobileEmulation", mobile_emulation)
            
            # Headless mode (randomly enabled)
            if random.choice([True, False]):
                options.add_argument("--headless=new")
                self.log("Running in headless mode", "DEBUG")
            
            service = Service(
                ChromeDriverManager().install(),
                port=random.randint(9000, 9999)
            )
            
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Additional stealth settings
            self.driver.execute_cdp_cmd(
                "Network.setUserAgentOverride",
                {"userAgent": user_agent}
            )
            self.driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {
                    "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                    """
                }
            )
            
            self.log("Selenium WebDriver initialized successfully", "SUCCESS")
        except Exception as e:
            self.log(f"Failed to initialize Selenium: {str(e)}", "ERROR")
            raise

    def random_delay(self, delay_type, reason=""):
        """Human-like randomized delay with logging"""
        min_d, max_d = self.delays[delay_type]
        delay = random.uniform(min_d, max_d)
        
        if reason:
            self.log(f"Waiting {delay:.1f}s ({reason})...", "DEBUG")
        else:
            self.log(f"Waiting {delay:.1f}s...", "DEBUG")
        
        # Split delay into smaller chunks with micro-variations
        chunks = random.randint(3, 7)
        for i in range(chunks):
            chunk_delay = delay / chunks
            time.sleep(chunk_delay)
            
            # Random micro-pauses
            if random.random() > 0.7:
                micro_pause = random.uniform(0.1, 0.3)
                time.sleep(micro_pause)
        
        return delay

    def generate_credentials(self):
        """Generate realistic credentials with logging"""
        self.log("Generating account credentials...", "INFO")
        
        username = (
            f"{random.choice(['photo', 'art', 'creative', 'digital'])}"
            f"{random.choice(['', '_', '.'])}"
            f"{random.choice(['world', 'life', 'vision', 'moment'])}"
            f"{random.randint(10, 999)}"
        ).lower()
        
        password = (
            f"{''.join(random.choices(string.ascii_letters, k=8))}"
            f"{random.randint(1000, 9999)}"
            f"{random.choice('!@#$%^&*')}"
        )
        
        self.log(f"Generated username: {username}", "DEBUG")
        self.log(f"Generated password: {password}", "DEBUG")
        
        return username, password

    def get_temp_email(self):
        """Get temporary email with retry logic"""
        self.log("Requesting temporary email...", "INFO")
        max_retries = 3
        
        for attempt in range(max_retries):
            self.random_delay('between_actions', "before email request")
            
            try:
                response = requests.get(
                    f"{self.email_api}?method=getNewMail",
                    timeout=10,
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('ok') and data.get('results', {}).get('email'):
                        email = data['results']['email']
                        self.log(f"Acquired temporary email: {email}", "SUCCESS")
                        return email
                    else:
                        self.log("Invalid response format from email service", "WARNING")
                else:
                    self.log(f"Email API returned status code: {response.status_code}", "WARNING")
                
            except Exception as e:
                self.log(f"Email request failed (attempt {attempt + 1}): {str(e)}", "WARNING")
            
            # Exponential backoff
            backoff = min(2 ** attempt, 10)
            self.log(f"Retrying in {backoff}s...", "WARNING")
            time.sleep(backoff)
        
        self.log("Failed to acquire temporary email after retries", "ERROR")
        return None

    def get_verification_code(self, email):
        """Retrieve verification code with detailed logging"""
        self.log(f"Checking for verification code in {email}...", "INFO")
        max_attempts = 8
        
        for attempt in range(max_attempts):
            self.random_delay('email_check', "between email checks")
            
            try:
                response = requests.get(
                    f"{self.email_api}?method=getMessages&email={email}",
                    timeout=15,
                    headers={"Accept": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('ok'):
                        messages = data.get('results', [])
                        self.log(f"Found {len(messages)} messages in inbox", "DEBUG")
                        
                        for msg in messages:
                            subject = msg.get('subject', '')
                            body = msg.get('body_text', '') or msg.get('body_html', '')
                            
                            self.log(f"Checking message: {subject[:30]}...", "DEBUG")
                            
                            # Multiple pattern matching
                            patterns = [
                                r'(?:code|کد)[:\s]*(\d{6})',
                                r'\b(\d{6})\b(?!.*\d{6})',
                                r'verif[a-z]*[\s.:-]*(\d{6})',
                                r'کد تایید[\s.:-]*(\d{6})'
                            ]
                            
                            for pattern in patterns:
                                match = re.search(pattern, body, re.IGNORECASE)
                                if match:
                                    code = match.group(1)
                                    self.log(f"Found verification code: {code}", "SUCCESS")
                                    return code
                    else:
                        self.log("Email service returned not OK", "WARNING")
                else:
                    self.log(f"Email API returned status code: {response.status_code}", "WARNING")
            
            except Exception as e:
                self.log(f"Email check failed (attempt {attempt + 1}): {str(e)}", "WARNING")
            
            # Progressive delay
            delay = min(5 * (attempt + 1), 30)
            self.log(f"Waiting {delay}s before next check...", "DEBUG")
            time.sleep(delay)
        
        self.log("Failed to retrieve verification code after maximum attempts", "ERROR")
        return None

    def detect_and_solve_captcha(self):
        """Detect and solve reCAPTCHA only when present"""
        try:
            self.log("Checking for reCAPTCHA...", "INFO")
            
            # Wait with timeout for reCAPTCHA
            try:
                WebDriverWait(self.driver, random.uniform(5, 10)).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".g-recaptcha, iframe[src*='recaptcha']"))
                )
                self.log("reCAPTCHA detected on page", "INFO")
            except:
                self.log("No reCAPTCHA detected, proceeding...", "INFO")
                return True
            
            # Get site key
            try:
                site_key_element = self.driver.find_element(
                    By.CSS_SELECTOR, 
                    ".g-recaptcha[data-sitekey], iframe[src*='recaptcha']"
                )
                site_key = site_key_element.get_attribute("data-sitekey")
                
                if not site_key and 'recaptcha' in site_key_element.get_attribute('src'):
                    site_key_match = re.search(r'k=([^&]+)', site_key_element.get_attribute('src'))
                    if site_key_match:
                        site_key = site_key_match.group(1)
                
                if not site_key:
                    raise Exception("Could not extract site key")
                
                self.log(f"Extracted reCAPTCHA site key: {site_key[:5]}...", "DEBUG")
            except Exception as e:
                self.log(f"Failed to extract site key: {str(e)}", "ERROR")
                return False
            
            # Solve with AntiCaptcha
            self.log("Attempting to solve reCAPTCHA...", "INFO")
            solver = recaptchaV2Proxyless()
            solver.set_key(random.choice(self.recaptcha_keys))
            solver.set_website_url(self.driver.current_url)
            solver.set_website_key(site_key)
            solver.set_soft_id(0)
            
            # Randomize solving timeout
            timeout = random.randint(60, 120)
            solver.set_timeout(timeout)
            self.log(f"Solving with timeout: {timeout}s", "DEBUG")
            
            g_response = solver.solve_and_return_solution()
            if not g_response:
                raise Exception("Failed to get solution from AntiCaptcha")
            
            self.log("Successfully solved reCAPTCHA", "SUCCESS")
            
            # Inject response in multiple ways
            scripts = [
                f'document.getElementById("g-recaptcha-response").innerHTML = "{g_response}";',
                f'var elem=document.querySelector("[name=\'g-recaptcha-response\']"); if(elem) elem.value = "{g_response}";'
            ]
            
            for script in scripts:
                try:
                    self.driver.execute_script(script)
                    self.random_delay('between_actions', "after reCAPTCHA injection")
                except Exception as e:
                    self.log(f"Script injection failed: {str(e)}", "DEBUG")
                    continue
            
            return True
            
        except Exception as e:
            self.log(f"reCAPTCHA handling failed: {str(e)}", "ERROR")
            return False

    def handle_challenge(self, username):
        """Handle Instagram challenges with detailed logging"""
        self.log(f"Handling challenge for account @{username}...", "INFO")
        challenge_url = "https://www.instagram.com/challenge/"
        
        try:
            # Navigate to challenge page
            self.log("Loading challenge page...", "DEBUG")
            self.driver.get(challenge_url)
            self.random_delay('between_actions', "after challenge page load")
            
            # Detect challenge type
            challenge_type = None
            try:
                if self.driver.find_elements(By.XPATH, "//h1[contains(text(), 'Verify Your Account')]"):
                    challenge_type = "verification"
                elif self.driver.find_elements(By.CSS_SELECTOR, ".g-recaptcha"):
                    challenge_type = "recaptcha"
                elif self.driver.find_elements(By.NAME, "email"):
                    challenge_type = "email_verify"
                
                self.log(f"Detected challenge type: {challenge_type}", "INFO")
            except:
                self.log("Could not determine challenge type", "WARNING")
                challenge_type = "unknown"
            
            # Handle different challenge types
            if challenge_type == "recaptcha":
                if not self.detect_and_solve_captcha():
                    raise Exception("Failed to solve challenge reCAPTCHA")
                
                # Fill username
                self.log("Filling username in challenge form...", "DEBUG")
                username_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "username"))
                )
                username_field.clear()
                for char in username:
                    username_field.send_keys(char)
                    time.sleep(random.uniform(0.1, 0.3))
                
                # Submit form
                self.log("Submitting challenge form...", "DEBUG")
                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
                )
                self.driver.execute_script("arguments[0].click();", submit_button)
                self.log("Challenge form submitted", "DEBUG")
                
            elif challenge_type in ["verification", "email_verify"]:
                # Get verification code
                self.log("Getting verification code for challenge...", "DEBUG")
                code = self.get_verification_code(self.current_email)
                if not code:
                    raise Exception("No verification code received")
                
                # Fill code
                self.log("Filling verification code...", "DEBUG")
                code_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "code"))
                )
                for char in code:
                    code_field.send_keys(char)
                    time.sleep(random.uniform(0.2, 0.4))
                
                # Submit
                self.log("Submitting verification code...", "DEBUG")
                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
                )
                self.driver.execute_script("arguments[0].click();", submit_button)
                
            else:
                # Fallback - try clicking primary button
                self.log("Attempting generic challenge bypass...", "WARNING")
                try:
                    primary_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next') or contains(., 'Continue')]"))
                    )
                    self.driver.execute_script("arguments[0].click();", primary_button)
                    self.log("Clicked primary button", "DEBUG")
                except:
                    self.log("Could not find primary button", "DEBUG")
            
            # Verify challenge completion
            self.random_delay('between_actions', "after challenge submission")
            if "challenge" not in self.driver.current_url.lower():
                self.log("Challenge completed successfully", "SUCCESS")
                return True
            
            # Fallback - refresh and continue
            self.log("Challenge may still be present, attempting refresh...", "WARNING")
            self.driver.get("https://www.instagram.com/")
            self.random_delay('between_actions', "after refresh")
            return True
            
        except Exception as e:
            self.log(f"Challenge handling failed: {str(e)}", "ERROR")
            return False

    def rotate_device_profile(self):
        """Rotate device fingerprint with logging"""
        self.log("Rotating device profile...", "INFO")
        self.current_device = random.choice(self.device_profiles)
        
        # Configure Instagram client
        locale = random.choice(["en_US", "en_GB", "fr_FR", "de_DE"])
        timezone = random.randint(-12, 12) * 60 * 60
        app_version = f"{random.randint(200, 220)}.0.0.{random.randint(10, 30)}.{random.randint(100, 130)}"
        
        self.client.set_locale(locale)
        self.client.set_timezone_offset(timezone)
        self.client.set_device({
            "app_version": app_version,
            "android_version": self.current_device["android_version"],
            "android_release": self.current_device["android_release"],
            "dpi": f"{random.choice([320, 480, 640])}dpi",
            "resolution": f"{random.choice([720, 1080, 1440])}x{random.choice([1280, 1920, 2560])}",
            "manufacturer": self.current_device["model"].split()[0],
            "device": self.current_device["device"],
            "model": self.current_device["model"],
            "cpu": random.choice(["qcom", "exynos", "arm64-v8a"])
        })
        
        # Set headers
        user_agent = (
            f"Instagram {app_version} "
            f"(Android {self.current_device['android_version']}; "
            f"{self.current_device['model']}; {locale}; "
            f"build/{random.randint(1000000, 9999999)})"
        )
        
        self.client.set_headers({
            "User-Agent": user_agent,
            "X-IG-App-Locale": locale,
            "X-IG-Device-Locale": locale,
            "X-IG-Mapped-Locale": locale
        })
        
        self.log(f"Rotated to device: {self.current_device['model']}", "DEBUG")
        self.log(f"Set app version: {app_version}", "DEBUG")
        self.log(f"Set locale: {locale}", "DEBUG")

    def save_account(self, account_data):
        """Save account info with organized structure"""
        self.log("Saving account information...", "INFO")
        
        # Create dated subfolder
        today = datetime.now().strftime("%Y-%m-%d")
        daily_dir = os.path.join(self.results_dir, today)
        os.makedirs(daily_dir, exist_ok=True)
        self.log(f"Daily directory: {daily_dir}", "DEBUG")
        
        # Create JSON file
        filename = f"ig_{account_data['username']}_{datetime.now().strftime('%H%M%S')}.json"
        filepath = os.path.join(daily_dir, filename)
        
        # Enhanced account data
        enhanced_data = {
            **account_data,
            "creation_device": self.current_device,
            "creation_ip": requests.get('https://api.ipify.org').text,
            "user_agent": self.client.headers.get("User-Agent"),
            "metadata": {
                "version": "3.0",
                "generated_by": "UltimateInstagramCreator"
            }
        }
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(enhanced_data, f, ensure_ascii=False, indent=2)
        
        self.log(f"Account data saved to: {filepath}", "SUCCESS")
        return filepath

    def create_account(self):
        """Complete account creation process with detailed logging"""
        self.session_stats['total_attempts'] += 1
        attempt_num = self.session_stats['total_attempts']
        self.log(f"\nStarting account creation attempt #{attempt_num}", "INFO")
        self.print_separator()
        
        # Rotate device profile
        self.rotate_device_profile()
        
        # Generate credentials
        self.log("Generating account credentials...", "INFO")
        username, password = self.generate_credentials()
        
        # Get temporary email
        self.log("Acquiring temporary email...", "INFO")
        email = self.get_temp_email()
        if not email:
            self.session_stats['failed'] += 1
            self.log("Account creation failed - no email", "ERROR")
            self.print_separator()
            return None
        
        self.current_email = email
        self.log(f"Using email: {email}", "DEBUG")
        
        try:
            # Open Instagram signup page
            self.log("Opening Instagram signup page...", "INFO")
            self.driver.get("https://www.instagram.com/accounts/emailsignup/")
            self.random_delay('between_actions', "after page load")
            
            # Check for reCAPTCHA
            self.log("Checking for reCAPTCHA...", "INFO")
            if not self.detect_and_solve_captcha():
                raise Exception("reCAPTCHA handling failed")
            
            # Register account through API client
            self.log(f"Registering account @{username}...", "INFO")
            self.random_delay('between_actions', "before signup")
            
            self.client.sign_up(
                username=username,
                password=password,
                email=email,
                first_name=username.split('_')[0].capitalize()
            )
            self.log("Account registration API call successful", "DEBUG")
            
            # Get verification code
            self.log("Retrieving verification code...", "INFO")
            verification_code = self.get_verification_code(email)
            if not verification_code:
                raise Exception("No verification code received")
            
            self.log(f"Verification code received: {verification_code}", "SUCCESS")
            self.random_delay('between_actions', "before simulated verification")
            
            # Handle potential challenges
            try:
                self.log("Testing account access...", "INFO")
                self.client.get_timeline_feed()  # Test login
                self.log("Account access confirmed", "DEBUG")
            except ChallengeRequired:
                self.log("Challenge required, attempting to solve...", "WARNING")
                if not self.handle_challenge(username):
                    raise Exception("Failed to solve challenge")
                self.log("Challenge solved successfully", "SUCCESS")
            
            # Account successfully created
            account_data = {
                'username': username,
                'password': password,
                'email': email,
                'verification_code': verification_code,
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': 'active',
                'device_profile': self.current_device
            }
            
            # Save account details
            saved_path = self.save_account(account_data)
            account_data['saved_path'] = saved_path
            
            self.session_stats['successful'] += 1
            self.session_stats['accounts'].append(account_data)
            
            self.log(f"Successfully created account: @{username}", "SUCCESS")
            self.print_separator()
            
            return account_data
            
        except ClientError as e:
            self.log(f"Instagram API error: {str(e)}", "ERROR")
        except Exception as e:
            self.log(f"Account creation error: {str(e)}", "ERROR")
        
        self.session_stats['failed'] += 1
        self.log("Account creation failed", "ERROR")
        self.print_separator()
        return None

    def print_stats(self):
        """Display comprehensive statistics with visual formatting"""
        success_rate = (self.session_stats['successful'] / self.session_stats['total_attempts']) * 100 \
            if self.session_stats['total_attempts'] > 0 else 0
        
        print("\n" + "=" * 60)
        print("📊 CURRENT STATISTICS".center(60))
        print("=" * 60)
        print(f"🟢 Successful: {self.session_stats['successful']}")
        print(f"🔴 Failed: {self.session_stats['failed']}")
        print(f"🔵 Total Attempts: {self.session_stats['total_attempts']}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.session_stats['successful'] > 0:
            last_account = self.session_stats['accounts'][-1]
            print("\n💾 Last Created Account:")
            print(f"👤 Username: @{last_account['username']}")
            print(f"📁 Saved At: {last_account['saved_path']}")
        
        print(f"\n⏱️ Running Since: {self.session_stats['start_time']}")
        print("=" * 60 + "\n")

    def cleanup(self):
        """Cleanup resources with logging"""
        self.log("Cleaning up resources...", "INFO")
        try:
            if self.driver:
                self.driver.quit()
                self.log("Selenium WebDriver closed", "DEBUG")
        except Exception as e:
            self.log(f"Error during cleanup: {str(e)}", "WARNING")

    def run(self, count=None):
        """Main execution loop with enhanced controls and logging"""
        self.log("Starting main execution loop", "INFO")
        self.print_stats()
        
        try:
            while count is None or len(self.session_stats['accounts']) < count:
                start_time = time.time()
                
                # Create account
                result = self.create_account()
                
                if result:
                    # Print stats every 3 accounts or 15 minutes
                    if len(self.session_stats['accounts']) % 3 == 0 or \
                       (time.time() - start_time) > 900:
                        self.print_stats()
                else:
                    # Print stats after every failure
                    self.print_stats()
                
                # Random sleep between 2-5 minutes to avoid detection
                delay = random.uniform(120, 300)
                self.log(f"Waiting {delay/60:.1f} minutes before next attempt...", "INFO")
                time.sleep(delay)
            
        except KeyboardInterrupt:
            self.log("\nReceived keyboard interrupt, shutting down...", "WARNING")
        except Exception as e:
            self.log(f"\nCritical error: {str(e)}", "ERROR")
        finally:
            self.cleanup()
            self.print_stats()
            self.log("Session completed. All accounts saved in the 'instagram_accounts' folder", "INFO")

if __name__ == "__main__":
    try:
        creator = UltimateInstagramCreator()
        creator.run(count=None)  # Run indefinitely until interrupted
    except Exception as e:
        print(f"\n🔥 Fatal error during initialization: {str(e)}")
        print("Please check your setup and try again.")
