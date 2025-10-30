import multiprocessing
from configparser import ConfigParser
from argparse import ArgumentParser

from utils.server_registration import get_cache_server
from utils.config import Config
from crawler import Crawler


def main(config_file, restart):
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    config.cache_server = get_cache_server(config, restart)
    crawler = Crawler(config, restart)
    crawler.start()

    from scraper import unique_pages, longest_page, longest_page_url, word_freq, subdomains
  
    print()
    print("=" * 60)
    print("CRAWLER ANALYSIS RESULTS")
    print("=" * 60)
    print()
    
    # Q1 Number of unique pages
    print(f"Number of unique pages crawled: {len(unique_pages)}")
    print()
    
    # Q2 Longest page
    print(f"Longest page: {longest_page} words")
    print(f"URL: {longest_page_url}")
    print()
    
    # Q3 Top 50 most common words
    print("Top 50 most common words:")
    print("-" * 40)
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    for i, (word, freq) in enumerate(sorted_words[:50], 1):
        print(f"{i:2d}. {word:20s} {freq:,}")
    print()
    
    # Q4 Subdomain distribution (sorted alphabetically)
    print("Subdomain distribution under uci.edu:")
    print("-" * 40)
    sorted_subdomains = sorted(subdomains.items())
    for subdomain, count in sorted_subdomains:
        print(f"{subdomain}, {count}")
    print()
    print("=" * 60)


if __name__ == "__main__":
    multiprocessing.set_start_method('fork', force=True)
    parser = ArgumentParser()
    parser.add_argument("--restart", action="store_true", default=False)
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    main(args.config_file, args.restart)
