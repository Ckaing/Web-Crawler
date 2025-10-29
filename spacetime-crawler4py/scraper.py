import re
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse, urljoin, urldefrag
import tokenizer

#ISSUES 
# 2025-10-29 11:06:29,863 - Worker-0 - INFO - Downloaded https://www.stat.uci.edu/wp-content/uploads/Shujie-Ma-Abstract-5-5-22, status <200>, using cache ('styx.ics.uci.edu', 9002).
# encoding error : input conversion failed due to input error, bytes 0x90 0xFC 0x1F 0x6E

# globals for analysis
unique_pages = set()
longest_page = 0
longest_page_url = ""
word_freq = {}
subdomains = {}

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def analysis(url, content):
    global longest_page, longest_page_url, word_freq, subdomains, unique_pages

    # defragment URL
    url, _ = urldefrag(url)
    unique_pages.add(url)

    # parse text
    word_count, freq = tokenizer.compute_text_frequencies(content)

    # update longest page
    if word_count > longest_page:
        longest_page = word_count
        longest_page_url = url

    # update word frequencies
    word_freq = tokenizer.union_freq(word_freq, freq)

    # update subdomains
    parsed = urlparse(url)
    if "uci.edu" in parsed.netloc:
        subdomains[parsed.netloc] = subdomains.get(parsed.netloc, 0) + 1


def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    # if status code is not 200, error has occurred and we cannot extract content
    if resp.status != 200 or resp.raw_response is None or resp.raw_response.content is None:
        return []

    # get content of page
    html_content = resp.raw_response.content
    # parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'lxml')

    # do analysis
    text = soup.get_text(strip=True)
    analysis(url, text)

    # extract links
    links = []
    # for all <a href="web_link.com/...">web_title</a>
    for a in soup.find_all('a', href=True):
        # get the web_link.com/... part
        href = a['href']
        # handles absolute and relative links
        # if url is an absolute one, it leaves url unchanged
        # otherwise if it is relative, it appends the resp.url
        url = urljoin(resp.url, href)
        # remove fragment
        url, _ = urldefrag(url)
        # add link to list
        links.append(url)

    return links


def is_calendar_pattern(url):
    # Checks if the url is in the pattern of a calendar and returns bool
    calendar_pattern = re.compile(r'(?i)(\b(19|20)\d{2}[-/](0?[1-9]|1[0-2])\b)|month=|date=')
    decoded_url = unquote(url)
    decoded_url = unquote(decoded_url)
    return bool(calendar_pattern.search(decoded_url))


def ui_state_pattern(url):
    decoded_url = unquote(url)
    decoded_url = unquote(decoded_url)
    ui_states = ["do=media", "tab_", "view=", "image=", "ns=", "tribe_", "ical="]
    return any(u in url for u in ui_states)


def has_session(url):
    decoded_url = unquote(url)
    decoded_url = unquote(decoded_url)
    sid_keys = ["sid=", "session=", "phpsessid=", "jsessionid=", "session", "id=", "diff", "idx="]
    return any(k in url for k in sid_keys)


def is_page_pattern(url):
    PAGINATION_KEYS = ["page=", "p=", "start=", "offset=", "pageNumber=", "pageNo=", "page/"]
    return any(k in url for k in PAGINATION_KEYS)


def is_tracking_pattern(url):
    TRACKING_KEYS = ["utm_", "fbclid", "gclid", "ref=", "referrer=", "source=", "campaign=", "mc_"]
    decoded_url = unquote(url)
    decoded_url = unquote(decoded_url)
    return any(k in decoded_url.lower() for k in TRACKING_KEYS)


def is_faceted_nav(url):
    facets = ["color=", "size=", "style=", "brand=", "filter=", "sort="]
    return sum(p in url for p in facets) > 2 


def is_trap(url):
    if is_calendar_pattern(url):
        return True
    if ui_state_pattern(url):
        return True
    if has_session(url):
        return True
    if is_page_pattern(url):
        return True
    if is_tracking_pattern(url):
        return True
    if is_faceted_nav(url):
        return True
    return False


def is_valid(url):
    # Decide whether to crawl this url or not.
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        url, _ = urldefrag(url)
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if is_trap(url):
            return False

        # only links in domain should be valid
        domains = ['ics.uci.edu', 'cs.uci.edu', 'informatics.uci.edu', 'stat.uci.edu']
        # netloc returns the hostname/authority
        if not any(parsed.netloc.endswith(d) for d in domains):
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise

