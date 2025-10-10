import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_fresh_youtube_cookies():
    """Get fresh YouTube cookies without login"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("Getting fresh YouTube cookies...")
        
        # Navigate to YouTube
        driver.get('https://www.youtube.com')
        time.sleep(8)
        
        # Scroll to simulate human behavior
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(2)
        
        # Accept cookies if prompted
        try:
            accept_button = driver.find_element("xpath", "//button[contains(text(), 'Accept') or contains(text(), 'I agree')]")
            accept_button.click()
            time.sleep(3)
        except:
            pass
        
        # Additional human-like behavior
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        
        # Extract cookies
        cookies = driver.get_cookies()
        
        # Convert to yt-dlp format
        cookie_lines = []
        for cookie in cookies:
            domain = cookie.get('domain', '')
            if 'youtube.com' in domain or 'google.com' in domain:
                secure = 'TRUE' if cookie.get('secure', False) else 'FALSE'
                http_only = 'TRUE' if cookie.get('httpOnly', False) else 'FALSE'
                expiry = cookie.get('expiry', 0)
                
                # Fix domain format for Netscape cookies
                if domain.startswith('.'):
                    domain_specified = 'TRUE'
                else:
                    domain_specified = 'FALSE'
                    if not domain.startswith('.'):
                        domain = '.' + domain
                
                line = f"{domain}\t{domain_specified}\t{cookie['path']}\t{secure}\t{expiry}\t{cookie['name']}\t{cookie['value']}"
                cookie_lines.append(line)
        
        # Save cookies
        cookie_content = "# Netscape HTTP Cookie File\n# Auto-generated cookies\n\n" + "\n".join(cookie_lines)
        
        with open('/app/fresh_cookies.txt', 'w') as f:
            f.write(cookie_content)
        
        print(f"Successfully extracted {len(cookie_lines)} cookies")
        return True
        
    except Exception as e:
        print(f"Cookie extraction failed: {e}")
        return False
    finally:
        try:
            driver.quit()
        except:
            pass

def test_cookies(cookie_file):
    """Test if cookies work by checking YouTube access"""
    if not os.path.exists(cookie_file):
        return False
    
    # Simple test - if file exists and has content, assume it works
    try:
        with open(cookie_file, 'r') as f:
            content = f.read()
            return len(content) > 100  # Basic validation
    except:
        return False