# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random, scrapy, requests
from scrapy.exceptions import CloseSpider
from urllib.parse import urlencode



class ScrapeOpsFakeBrowserHeaderAgentMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = 'api-key'
        self.scrapeops_endpoint = 'http://headers.scrapeops.io/v1/browser-headers'
        self.scrapeops_fake_browser_headers_active = True
        self.scrapeops_num_results = 1
        self.headers_list = []
        self._get_headers_list()
        self._scrapeops_fake_browser_headers_enabled()

    def _get_headers_list(self):
        try:
            payload = {'api_key': self.scrapeops_api_key}
            if self.scrapeops_num_results is not None:
                payload['num_results'] = self.scrapeops_num_results
            response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
            response.raise_for_status()  # Raise an exception for non-2xx responses
            json_response = response.json()
            self.headers_list = json_response.get('result', [])
        except (requests.RequestException, ValueError) as e:
            self.headers_list = []  # Set empty list on failure
            scrapy.log.msg(f"Failed to fetch headers list: {e}", level=scrapy.log.ERROR)

    def _scrapeops_fake_browser_headers_enabled(self):
        if not self.scrapeops_api_key or not self.scrapeops_fake_browser_headers_active:
            self.scrapeops_fake_browser_headers_active = False

    def process_request(self, request, spider):
        if not self.scrapeops_fake_browser_headers_active or not self.headers_list:
            return  # Skip if headers are disabled or not fetched

        random_browser_header = random.choice(self.headers_list)

        for header_name, header_value in random_browser_header.items():
            request.headers[header_name] = header_value

        print("****************** NEW HEADER ATTACHED ****************")
        print(request.headers)
