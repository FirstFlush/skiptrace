from playwright.sync_api import sync_playwright
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
from airbnb_buildings import building_addresses
from datetime import datetime
import time
import random
import csv
import os
import requests


class CraigslistHousingScraper:

    PRICE_LOWEST = 1000
    PRICE_HIGHEST = 20000
    SELECTORS = {
        'title'         : 'a.titlestring',  # URL is title's [href]
        'listing'       : '.gallery-card:not(.spacer)', # used to remove listings after <li class="nearby-separator">
        'bad_listing'   : 'gallery-card',
        'no_listings'   : 'li.nearby-separator',
        'price'         : '.priceinfo',
        'bedrooms'      : '.post-bedrooms',
        'sqft'          : '.post-sqft',
        'date'          : '.meta',
    }

    def __init__(self):

        shared_folder = os.getenv('SHARED_FOLDER')
        self.date_today = datetime.now().strftime('%m-%d-%Y')
        self.file_name = f"{shared_folder}/airbnb_leads/airbnb_results__{self.date_today}.csv"

        with open(self.file_name, 'w') as csv_file:
            writer = csv.writer(csv_file)
            headers = [
                'Date',
                'Address',
                'Title',
                'Price',
                'Bedrooms',
                'sqft',
                'URL',
            ]
            writer.writerow(headers)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            self.page = browser.new_page()
            self.page.goto('https://vancouver.craigslist.org/search/hhh/')

            for building_address in building_addresses:
                search_bar = self.page.get_by_placeholder('search housing')
                search_bar.fill(building_address)
                search_bar.press('Enter')
                try:
                    self.page.wait_for_selector(
                        selector=self.SELECTORS['listing'], timeout=5000)
                except PlaywrightTimeoutError:
                    print(f"[ No listings found ] {building_address}")
                    pass
                else:
                    self.current_address = building_address
                    self.scrape_listings()

                self.random_delay()

    def random_delay(self):
        """Random time delay. 
        To make us look more human :)
        """
        time.sleep(random.randint(3, 8))
        return

    # def is_nearby_separator(self) -> bool:
    #     """If no listings are found, sometimes Craigslist will simply return no listings.
    #     But other times Craigslist will instead show irrelevant listings that are very
    #     far away. When this happens, a <li> element will appear with the class of
    #     'nearby-separator'. The page is checked for this <li> and if its found, returns
    #     True.
    #     """
    #     nearby_separator = self.soup.select(self.SELECTORS['no_listings'])
    #     if nearby_separator:
    #         return True

    def truncate_nearby_results(self):
        """If no listings are found, sometimes Craigslist will simply return no listings. 
        But other times Craigslist will instead show irrelevant listings that are very 
        far away. When this happens, a <li> element will appear with the class of 
        'nearby-separator' and the irrelevant listings will follow. If this <li> tag is 
        found, all results after it are destroyed.
        """
        nearby_separator = self.soup.select_one(self.SELECTORS['no_listings'])
        try:
            nearby_results = nearby_separator.find_all_next(
                'div', {'class': self.SELECTORS['bad_listing']})
        except AttributeError:
            pass
        else:
            for result in nearby_results:
                result.extract()
        return

    def price_check(self, price) -> bool:
        """Checks to make sure the price is within the defined range."""
        if self.PRICE_LOWEST < price < self.PRICE_HIGHEST:
            return True
        else:
            return False

    def scrape_listings(self):
        """BeautifulSoup scrapes all listings on page."""
        self.soup = BeautifulSoup(markup=self.page.content(), features='lxml')
        self.truncate_nearby_results()
        listings = self.soup.select(self.SELECTORS['listing'])
        with open(self.file_name, 'a') as csv_file:
            for listing in listings:
                address     = self.current_address
                try:
                    title = listing.select_one(self.SELECTORS['title']).text
                except AttributeError:
                    title = 'none'
                try:
                    url = listing.select_one(self.SELECTORS['title'])['href']
                except (AttributeError, TypeError):
                    url = 'none'
                try:
                    date = listing.select_one(self.SELECTORS['date']).text.split('·')[0]
                except AttributeError:
                    date = 'none'
                try:
                    price_str   = listing.select_one(self.SELECTORS['price']).text
                    price       = int(price_str.replace('$', '').replace(',', '').strip())
                except AttributeError:
                    price   = 0
                try:
                    bedrooms = listing.select_one(
                        self.SELECTORS['bedrooms']).text
                except AttributeError:
                    bedrooms = '-'
                try:
                    sqft = int(listing.select_one(
                        self.SELECTORS['sqft']).text.replace('ft2', '').strip())
                except AttributeError:
                    sqft = '-'

                if self.price_check(price) == False:
                    continue
                else:
                    writer = csv.writer(csv_file)
                    row_list = [
                        date,
                        address,
                        title,
                        price,
                        bedrooms,
                        sqft,
                        url,
                    ]
                    writer.writerow(row_list)


    # def email_results(self):
    #     """Send the CSV file to recipients via MailGun's email API"""
    #     return requests.post(
    #         "https://api.mailgun.net/v3/YOUR_DOMAIN_NAME/messages",
    #         auth=("api", "493c391d02878792357d5f3552343762-7764770b-246822cb"),
    #         data={"from": "Excited User <mailgun@YOUR_DOMAIN_NAME>",
    #             "to": ["firstflush@protonmail.com"],
    #             "subject": "Hello",
    #             "text": "Testing some Mailgun awesomness!"})


def main():
    CraigslistHousingScraper()


if __name__ == '__main__':
    main()
