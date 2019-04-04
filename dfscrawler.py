
""" Python implementation to perform Depth first crawling of the web.
    Starts from the url https://en.wikipedia.org/wiki/Space_exploration and downloads all
    links to other wiki articles in a depth first manner (only upto depth 6).
    Only downloads english articles, ignores links to sections in the same page, links to images etc.
    """
import requests
from bs4 import BeautifulSoup
import time

url_visited = []
url_init = "https://en.wikipedia.org"


def excludeURL(url):
    not_english = False
    not_new_urls = (url.startswith('#') or url.endswith('.jpg') or url.startswith('//') or url.startswith('/w/index.php')
                   or ':' in url)
    if "https" in url:
        url = url.replace("https://", "")
        not_english = not(url.startswith("en"))
    return not_new_urls or not_english


# This function is a recursive depth first search implementation of crawling
# once a depth 6 is reached, the crawler backtracks and visits other urls till depth 6 is reached in the new path
# The function returns when it has completed crawling 1000 urls / has visited all paths available within depth 6


def rec_dfs_crawl(url, depth):
    if len(url_visited) == 1000:                           # Stop fetching pages when count reaches 1000
        return # Base case
    if url not in url_visited:
        time.sleep(1)                                      # Adhere to politeness policy
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        url_visited.append(url)                     # mark visited
        if depth <= 5 and len(url_visited) < 1000:  # double check to avoid additional calls
            urls = soup.findAll('a', href=True)
            for item in urls:
                if not excludeURL(item['href']):
                    to_visit = url_init + item['href']
                    rec_dfs_crawl(to_visit, depth+1)           # recursive call to crawl



def dfs_crawl(seed):
    curr_depth = 0
    rec_dfs_crawl(seed, curr_depth + 1)


if __name__ == "__main__":
    seed = "https://en.wikipedia.org/wiki/Space_exploration"
    dfs_crawl(seed)
    f = open("dfs_urls.txt", 'w+')
    for item in url_visited:
        f.write("%s\n" % item)
