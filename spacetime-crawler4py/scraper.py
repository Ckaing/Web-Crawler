import re
from urllib.parse import urlparse

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

# NOTE (delete) don't worry about robots.txt in assignment

""" 
NOTE delete after we finish
gets response from URL (text, html, idk what it is figure it out)
what you need to do is parse that response, supposed to extract the url links on that page 
TODO RETURN: a list of those urls
content found on resp.raw_response.content
package: beautifulsoup --> will do all the work for you
"""

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
    return list()

"""
NOTE they ask us back for each URL, should we crawl the URL or not
    if yes, keep and eventually will crawl
    if no, do not keep
put a bunch of filters 
don't worry about robots.txt
"""

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        # NOTE (delete) DEFAULT FILTERS, the absolute minimum
        # NOTE (delete) if shcheme of HTML is not these, not interested in crawling (return False)
        if parsed.scheme not in set(["http", "https"]):
            return False
        # NOTE (delete) regex match on all the files we're not interested in crawling
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

        """
            TODO: (delete) figure out what other things we need to filter out according to specs
            process: run crawler as is, change USER AGENT
            start looking at URLs that is printing on console
                compare URLs with project specification 
                    i.e. only crawl things in ics --> if cralwer brought things outside of ics probably 
                    add filter so that we don't crawl those
            hard code policies about what we want/don't want
                be careful on excluding things that you shouldn't be excluding
        """

    except TypeError:
        print ("TypeError for ", parsed)
        raise
