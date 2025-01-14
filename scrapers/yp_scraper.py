from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Set up headless Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.paginebianche.it/aziende?qs=Abbigliamento')

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
