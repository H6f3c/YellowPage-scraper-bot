from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode
chrome_options.add_argument('--no-sandbox')  # Required in some restricted environments
chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
chrome_options.add_argument('--remote-debugging-port=9222')  # Avoid DevToolsActivePort issue

driver = webdriver.Chrome(options=chrome_options)

# Wait for content to load (if necessary)
driver.implicitly_wait(5)  # Adjust this as needed

# Get the page source after JavaScript has loaded
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Find and print business URLs
business_urls = []
for item in soup.find_all('a', class_='link-class'):  # Update 'link-class' with the actual class
    business_urls.append(item.get('href'))

print(f"Collected {len(business_urls)} business URLs.")
print(business_urls)

# Close the driver
driver.quit()
