from threading import Thread

from inspect import getsource
from utils.download import download
from utils import get_logger
import scraper
import time

from urllib.parse import urlparse

# get the DOMAIN, not the subdomain
def get_base_domain(url):
    parsed = urlparse(url)  # [subdomain if applicable].domain.suffix
    # get rid of subdomain --> extract just domain.suffix
    host = parsed.netloc.lower()
    domains = ['ics.uci.edu', 'cs.uci.edu', 'informatics.uci.edu', 'stat.uci.edu']
    for d in domains:
        if host == d or host.endswith('.' + d):
            return d
    return host


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.BUFFER_DELAY = 0.01
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests in scraper.py"
        assert {getsource(scraper).find(req) for req in {"from urllib.request import", "import urllib.request"}} == {-1}, "Do not use urllib.request in scraper.py"
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break

            # politeness implementation
            # get domain
            domain = get_base_domain(tbd_url)
            wait = 0
            with self.frontier.lock:
                # get last time we accessed domain
                last_time = self.frontier.last_access.get(domain, 0)
                now = time.time()
                # find out what the next access time should be
                next_allowed = max(now, last_time + self.config.time_delay + self.BUFFER_DELAY)
                # update 
                self.frontier.next_available_time[domain] = next_allowed
                # compute wait time
                wait = next_allowed - now

            # sleep for however long is necessary
            if wait > 0:
                time.sleep(wait)
            
            # start download
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            scraped_urls = scraper.scraper(tbd_url, resp)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)

            # maybe can remove later bc we have sleep but keep for safety reasons
            # time.sleep(self.config.time_delay)
