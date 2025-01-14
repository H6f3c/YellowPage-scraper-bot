from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep

# Set up the Selenium WebDriver (using Chrome in this case)
driver = webdriver.Chrome(executable_path='/path/to/chromedriver')  # Update with your chromedriver path

def get_business_urls(search_url):
    driver.get(search_url)
    sleep(2)  # Wait for the page to load
    
    # Scrape the business links (adjust the selector)
    business_links = driver.find_elements(By.CLASS_NAME, 'business-link-class')  # Adjust class name
    business_urls = [link.get_attribute('href') for link in business_links]
    
    return business_urls

def scrape_business_page(business_url):
    driver.get(business_url)
    sleep(2)  # Wait for the page to load
    
    # Extract business information
    business_name = driver.find_element(By.CLASS_NAME, 'business-name-class').text  # Adjust class name
    business_url = driver.find_element(By.CLASS_NAME, 'business-url-class').get_attribute('href')  # Adjust class name
    business_phone = driver.find_element(By.CLASS_NAME, 'phone-number-class').text  # Adjust class name
    
    return {
        'name': business_name,
        'url': business_url,
        'phone': business_phone
    }

def main():
    search_url = "https://www.yellowpages.com/search?search_terms=Abbigliamento&geo_location_terms=Moreno+Valley%2C+CA"
    business_urls = get_business_urls(search_url)
    
    for url in business_urls:
        data = scrape_business_page(url)
        print(data)

main()

driver.quit()  # Close the browser window
