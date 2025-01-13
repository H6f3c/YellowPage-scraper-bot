import asyncio
import time
import csv
from scrapers.yp_scraper import all_business_urls, scrapeBusiness

async def scrapeMe_with_progress(bizz_urls):
    total = len(bizz_urls)
    results = []
    
    for idx, url in enumerate(bizz_urls, 1):
        print(f"Scraping {idx}/{total}: {url}")
        try:
            data = await scrapeBusiness(url)  # Assuming scrapeBusiness scrapes one business
            results.append(data)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    
    return results

async def main():
    url = input("Enter a searched business category url: ")
    print("Scraping Business URLs. Please wait...")
    bizz_urls = await all_business_urls(url)
    
    print("Scraping data for businesses. This may take some time...")
    scrape_datas = await scrapeMe_with_progress(bizz_urls)
    
    # Export to CSV
    with open("scraped_data.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = scrape_datas[0].keys()  # Assuming each entry is a dictionary
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scrape_datas)
    
    print("Data exported to 'scraped_data.csv'")
    return scrape_datas

if __name__ == "__main__":
    start_time = time.time()
    print(asyncio.run(main()))
    total_time = round(time.time() - start_time, 2)
    time_in_secs = round(total_time)
    time_in_mins = round(total_time / 60)
    print(f"Took {time_in_secs} seconds | {time_in_mins} minutes.")
