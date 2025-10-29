import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
import tokenizer
import requests


def scraper(url, resp):
    links = extract_next_links(url, resp)
    validLinks = []
    # list of subDomains of uci.edu
    subDomains = {}
    unique_Pages = []
    # cycles through every link extracted
    for link in links:
        # only keeps and looks at valid links
        if is_valid(link):
            # appends all valid links to return list
            validLinks.append(link)

            # extracts domain and path for subdomain counting
            parsed = urlparse(link)
            domain = parsed.netloc
            path = parsed.path
            domain_path = domain + path

            # counts unique pages in uci.edu subdomains
            if ("uci.edu" in domain):
                if domain_path not in unique_Pages:
                    unique_Pages.append(domain_path)
                    if domain in subDomains:
                        subDomains[domain] += 1
                    else:
                        subDomains[domain] = 1

    # puts dict in alphabetical order for subdomains | Question 4
    sorted_items = sorted(subDomains.items(), key=lambda item: item[1], reverse=True)
    # number of unique pages | Question 1
    num_of_unique_pages = len(unique_Pages)

    print(validLinks)
    return validLinks

    # return [link for link in links if is_valid(link)]


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
    if resp.status != 200:
        return []

    # get content of page
    html_content = resp.raw_response.content
    # parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'lxml')

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


def is_valid(url):
    # Decide whether to crawl this url or not.
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        url, _ = urldefrag(url)
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
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


# longest page in terms of number of words | Question 2
def find_longest_page(links):
    # Argument is the list of links to parse and check the length of
    # words within the page excluding the text markups
    # Returns the link as a string with the longest page in terms of words

    max_length = 0
    longest_page = ""

    for link in links:
        # GET request for each link
        response = requests.get(link)

        # only parses links that return success status
        if (response.status_code != 200):
            continue
        else:
            # retrieve text from the html
            content = response.text
            soup = BeautifulSoup(content, "html.parser")

            # removes all style and script from html and exracts text from page
            for line in soup(['style', 'script']):
                line.decompose()
            page_text = soup.get_text()

            # clean the text by removing extra whitespace and newlines
            cleaned_text = re.sub(r'\s+', ' ', page_text).strip()
            all_words = cleaned_text.split()

            # updates max_length and current link to longest page
            if len(all_words) > max_length:
                max_length = len(all_words)
                longest_page = link

    return longest_page
