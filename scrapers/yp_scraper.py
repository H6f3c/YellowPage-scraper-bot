import re
import asyncio
import aiohttp
import requests
import pandas as pd
from lxml import etree
from time import sleep
from bs4 import BeautifulSoup

from tools.functionalities import userAgents, randomTime, verify_yellow, yaml_by_select, yp_lists, create_path

print(f"Scraping page: {url}")

# Extract business URLs from the Yellow Pages search results
async def yellowPages(yp_url):
    async with aiohttp.ClientSession() as session:
        scrape = yaml_by_select('selectors')
        total_page_urls = yp_lists(yp_url)
        total_business_urls = []

        for idx, url in enumerate(total_page_urls):
            try:
                async with session.get(url, headers={'User-Agent': userAgents()}) as response:
                    soup = etree.HTML(str(BeautifulSoup(await response.text(), 'lxml')))

                    global categories
                    categories = f"""{''.join(soup.xpath(scrape['categories']))}"""
                    page_content = ''.join(soup.xpath(scrape['page_content']))
                    print(f"Found business URLs: {business_links}")
                    
                    # Exit if no results found
                    if re.search("^No results found for.*", page_content):
                        print("No content. Please try again with a different keyword.")
                        break

                    business_links = [f"https://www.yellowpages.com{link}" for link in soup.xpath(scrape['business_urls'])]
                    total_business_urls.extend(business_links)
            except (requests.exceptions.ConnectTimeout, aiohttp.ClientError):
                print(f"Connection error. Skipping URL: {url}")
                continue

        return total_business_urls


# Fetch business details for a single business page
async def scrapeBusiness(url):
    scrape = yaml_by_select('selectors')
    yellow_in_dicts = []
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers={'User-Agent': userAgents()}) as response:
                soup = etree.HTML(str(BeautifulSoup(await response.text(), 'lxml')))
                business_names = ''.join(soup.xpath(scrape['business_name']))
                datas = {
                    "Business Name": business_names,
                    "Contact": ''.join(soup.xpath(scrape['contact'])),
                    "Email": ''.join(soup.xpath(scrape['email'])).replace("mailto:", ""),
                    "Address": ''.join(soup.xpath(scrape['address'])),
                    "Map and Direction": ''.join(f"https://www.yellowpages.com{soup.xpath(scrape['map_and_direction'])}"),
                    "Review": ''.join(soup.xpath(scrape['review'])).replace("rating-stars ", ""),
                    "Review Count": re.sub(r"[()]", "", ''.join(soup.xpath(scrape['review_count']))),
                    "Website": ''.join(soup.xpath(scrape['website'])),
                    "Hyperlink": url,
                }
                yellow_in_dicts.append(datas)
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    return yellow_in_dicts


# Process a list of URLs to fetch business details
async def scrapeMe(url_lists):
    yellow_in_dicts = []
    print(f"Scraping | {categories}. Number of businesses: {len(url_lists)}. Please wait.")

    tasks = []
    for url in url_lists:
        bizz_name = ' '.join(url.split("/")[-1].split("?")[0].split("-")[:-1])
        print(f"Scraping business: {bizz_name}")
        tasks.append(scrapeBusiness(url))

    results = await asyncio.gather(*tasks)
    for res in results:
        yellow_in_dicts.extend(res)

    # Save results to an Excel file
    create_path('Yellowpage database')
    df = pd.DataFrame(yellow_in_dicts)
    output_file = f'Yellowpage database/{categories}.xlsx'
    df.to_excel(output_file, index=False)
    print(f"Scraping complete. Data saved to {output_file}")


# Wrapper to initiate scraping
async def startScraping():
    search_link = input("Enter the Yellow Pages search URL: ")
    all_urls = await all_business_urls(search_link)
    if not all_urls:
        print("No business URLs found. Exiting.")
        return
    await scrapeMe(all_urls)


# Entry point for extracting all business URLs
async def all_business_urls(url):
    return await asyncio.create_task(yellowPages(url))
