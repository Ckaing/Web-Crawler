import re
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse, urljoin, urldefrag
from analyze import analysis


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


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

    # if page size less than 1000 bytes, skip 
        # most likely low-information page (1000 bytes is a pretty short page)
        # fyi 500 bytes is like basically empty (i.e. a 404 not found page)
    if len(resp.raw_response.content) < 1000:
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
        try:
            url = urljoin(resp.url, href)
            # remove fragment
            url, _ = urldefrag(url)
            # add link to list
            links.append(url)
        except Exception as e:
            continue

    return links


def ui_state_pattern(url):
    decoded_url = unquote(url)
    decoded_url = unquote(decoded_url)
    ui_states = ["do=", "tab_", "view=", "image=", "ns=", "tribe_", "ical=", "login", "signup"]
    return any(u in url for u in ui_states)


def has_session(url):
    decoded_url = unquote(url)
    decoded_url = unquote(decoded_url)
    sid_keys = ["sid=", "session=", "phpsessid=", "jsessionid=", "session", "id=", "version="]
    return any(k in decoded_url for k in sid_keys)


def is_faceted_nav(url):
    decoded_url = unquote(url)
    decoded_url = unquote(decoded_url)
    facets = ["filter=", "sort=", "format=", "precision=second", "query=", "?q=", "?s="]
    return any(p in decoded_url for p in facets)


def trap_domain(url):
    trap_domains = ["physics", "gitlab", "ngs.ics"] 
    trap_paths = ["/event", "/events", "/~eppstein/pix", "/doku.php", "/photo"]
    parsed = urlparse(url)
    if any(parsed.path.startswith(d) for d in trap_paths):
        return True
    if any(parsed.netloc.startswith(d) for d in trap_domains):
        return True
    return False


def is_trap(url):
    if ui_state_pattern(url):
        return True
    if trap_domain(url):
        return True
    if has_session(url):
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
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        return False
    except ValueError:
        print("ValueError for ", parsed)
        return False