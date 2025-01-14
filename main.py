import requests
from bs4 import BeautifulSoup
import time

# Step 1: Scrape search results to get links to business details
def get_business_links(search_url):
    print("Fetching business links...")
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Adjust the selector to match Yellow Pages' structure
    business_links = soup.find_all('a', class_='business-name')  # Adjust the class name
    links = [link['href'] for link in business_links if link.get('href')]
    
    print(f"Found {len(links)} business links.")
    return links

# Step 2: Scrape each business's detail page for data
def scrape_business_details(base_url, business_link):
    full_url = f"{base_url}{business_link}"  # Construct the full URL
    print(f"Scraping business details from: {full_url}")
    response = requests.get(full_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        # Extract business details (adjust selectors as needed)
        business_name = soup.find('h1', class_='business-title').text.strip()  # Adjust the class name
        business_phone = soup.find('a', class_='phone').text.strip()  # Adjust the class name
        business_website = soup.find('a', class_='website')['href'].strip()  # Adjust the class name
    except AttributeError:
        print("Some details are missing. Skipping...")
        return None
    
    return {
        'name': business_name,
        'phone': business_phone,
        'website': business_website
    }

# Main script
def main():
    base_url = "https://www.yellowpages.com"  # Base URL of the Yellow Pages site
    search_url = f"{base_url}/search?search_terms=clothing&geo_location_terms=Los+Angeles%2C+CA"  # Update for your query
    
    business_links = get_business_links(search_url)
    if not business_links:
        print("No business links found. Exiting.")
        return
    
    # Scrape details for each business
    all_data = []
    for link in business_links:
        data = scrape_business_details(base_url, link)
        if data:
            all_data.append(data)
        time.sleep(1)  # Be polite and avoid overloading the server
    
    print(f"Scraped {len(all_data)} businesses:")
    for business in all_data:
        print(business)

if __name__ == "__main__":
    main()
