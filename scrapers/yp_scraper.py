from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run without GUI
chrome_options.add_argument('--no-sandbox')  # Disable sandboxing (required in Colab)
chrome_options.add_argument('--disable-dev-shm-usage')  # Avoid shared memory issues
chrome_options.add_argument('--disable-gpu')  # Disable GPU usage
chrome_options.binary_location = '/usr/bin/chromium-browser'

# Initialize the driver
service = Service('/usr/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)


# Automatically download and set up ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


# Specify ChromeDriver path if necessary (e.g., Service for explicit path)
service = Service('/path/to/chromedriver')  # Update the path if needed

# Initialize the driver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Load the target URL
    url = input("Enter a business category URL (e.g., https://www.example.com): ").strip()
    driver.get(url)

    # Wait for elements to load (adjust timeout and locator as needed)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'link-class'))  # Update 'link-class' to the actual class name
    )

    # Get the page source after JavaScript has loaded
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Find and collect business URLs
    business_urls = []
    for item in soup.find_all('a', class_='link-class'):  # Update 'link-class' to the actual class
        business_urls.append(item.get('href'))

    print(f"Collected {len(business_urls)} business URLs:")
    for link in business_urls:
        print(link)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the driver
    driver.quit()
