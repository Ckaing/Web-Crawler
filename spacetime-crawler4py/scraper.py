import re
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse, urlunparse, parse_qs, urlencode, urljoin, urldefrag

from analyze import analysis



def scraper(url, resp):
    """ 
    Description: Scraper function to extract links from a page by calling extract_next_links
    and filter them with is_valid to guarantee only valid links are returned

    Input: a url and response object
    Output: list of valid links

    """
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def normalize_url(url):
    """
    Description: Normalize url by removing tracking params like share/utm_ 
    from the url so that we get base url, removes repeated reference to 
    nearly identical content

    Input: The url that we evaluate
    Output: Normalized url with share/utm_ removed if present
    """
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)

    # Remove tracking params
    for key in list(qs.keys()):
        if key.lower() == "share" or key.lower().startswith("utm_"):
            qs.pop(key)

    # Rebuild the query string
    new_query = urlencode(qs, doseq=True)
    normalized = parsed._replace(query=new_query)
    return urlunparse(normalized)


# TODO desc
def extract_next_links(url, resp):
    """ 
    Description: extract links from a page with a valid response code that
    are defragmented and normalized

    Input: a url and response object
    Output: return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    """
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

    # if page size less than 1000 bytes, most likely a low information page
    if len(resp.raw_response.content) < 1000:
        return []

    # get content of page
    html_content = resp.raw_response.content
    # do analysis
    analysis(url, html_content)

    # parse with BeautifulSoup for links
    soup = BeautifulSoup(html_content, 'lxml')
    links = []
    # extract links
    for a in soup.find_all('a', href=True):
        href = a['href']
        try:
            # handles absolute and relative
            next_url = urljoin(resp.url, href)
            # remove tracking params
            next_url = normalize_url(next_url) 
            # remove fragment
            next_url, _ = urldefrag(next_url)
            # add link to list
            links.append(next_url)
        except Exception as e:
            continue

    return links


def ui_state_pattern(url):
    """
    Description: Keywords that indicate images or other media, as well as
    user authetication which has low informational content

    Input: The url we want to evaluate
    Output: True/False

    """
    ui_states = ["do=", "tab_", "view=", "image=", "ns=", "tribe_", "ical=", "login", "signup"]
    return any(u in url for u in ui_states)


def has_session(url):
    """
    Description: Keywords that indicate different sessions/ids of a url
    while having the same if not similar content as other sessions

    Input: The url we want to evaluate
    Output: True/False

    """
    sid_keys = ["sid=", "session=", "phpsessid=", "jsessionid=", "session", "id=", "version="]
    return any(k in url for k in sid_keys)


def is_faceted_nav(url):
    """
    Description: Keywords that indicate different UI based on user preference
    (i.e. sort, filter) with the same content

    Input: The url we want to evaluate
    Output: True/False

    """
    facets = ["filter=", "sort=", "format=", "precision=second", "query=", "?q=", "?s=", "C=", "O="] 
    return any(p in url for p in facets)


def is_directory_listing(url):
    """
    Description: Keywords that are part of Apache / Nginx pages that
    auto-index which dynamically creates pages leading to infinite loops

    Input: The url we want to evaluate
    Output: True/False

    """
    # catches typical Apache / Nginx auto-index pages
    return "?c=" in url or "index of" in url


def trap_domain(url):
    """
    Description: Domains and paths that contain massive amounts of 
    low-information/repetitive content

    Input: The url that we evaluate
    Output: True/False 
    """
    trap_domains = ["gitlab", "ngs.ics"] 
    trap_paths = ["/event", "/events", "/~eppstein/pix", "/doku.php", "/photo"]
    parsed = urlparse(url)
    if any(parsed.path.startswith(d) for d in trap_paths):
        return True
    if any(parsed.netloc.startswith(d) for d in trap_domains):
        return True
    return False


def is_trap(url):
    """
    Description: Check url against various traps

    Input: The url that we evaluate
    Output: True if determined to be a trap; False otherwise
    """
    if trap_domain(url):
        return True

    # for double encoded links
    decoded_url = unquote(url)
    decoded_url = unquote(decoded_url)

    if ui_state_pattern(decoded_url):
        return True
    if has_session(decoded_url):
        return True
    if is_faceted_nav(decoded_url):
        return True
    if is_directory_listing(decoded_url):
        return True
    return False


def is_valid(url):
    """
    Description: Decide whether to crawl this url or not

    Input: The url that we evaluate
    Output: True if we decide to crawl; False otherwise
    """
    try:
        url, _ = urldefrag(url)
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if is_trap(url):
            return False

        # only links in select domains should be valid
        domains = ['ics.uci.edu', 'cs.uci.edu', 'informatics.uci.edu', 'stat.uci.edu']
        # netloc returns the hostname/authority, match against allowed domains
        if not any(parsed.netloc == d or parsed.netloc.endswith('.' + d) for d in domains):
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz"
            + r"|txt|odc$"
            + r"|mol|sdf)$", parsed.path.lower()) 

    except TypeError:
        print("TypeError for ", parsed)
        return False
    except ValueError:
        print("ValueError for ", parsed)
        return False