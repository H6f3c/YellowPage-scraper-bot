import asyncio
import time
import os
import csv
from scrapers.yp_scraper import all_business_urls, scrapeBusiness

if __name__ == "__main__":
    start_time = time.time()

    async def main():
        # Prompt user for input URL
        url = input("Enter a searched business category URL (e.g., Yellow Pages): ")
        if not url.startswith("http"):
            print("Please provide a valid URL starting with http or https.")
            return
        
        print("Scraping Business URLs. Please wait...")
        # Step 1: Scrape all business URLs
        bizz_urls = await all_business_urls(url)
        print(f"Collected {len(bizz_urls)} business URLs.")

        if not bizz_urls:
            print("No business URLs found. Please check the input URL or scraper logic.")
            return

        # Step 2: Scrape details for each business
        print("Scraping data for businesses. This may take some time...")
        business_data = await scrapeBusinessDetails(bizz_urls)

        if not business_data:
            print("No data found. Please verify the scraper logic.")
            return

        # Step 3: Save data to a CSV file
        csv_file = "scraped_business_data.csv"
        fieldnames = ["Name", "Website", "Phone", "Email"]
        with open(csv_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(business_data)

        print(f"Data successfully saved to {csv_file}")

    # Run the async main function
    asyncio.run(main())

    # Display total execution time
    total_time = round(time.time() - start_time, 2)
    time_in_secs = round(total_time)
    time_in_mins = round(total_time / 60)

    print(f"Took {time_in_secs} seconds | {time_in_mins} minutes.")
