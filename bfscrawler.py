""" Python implementation to perform Breadth first crawling of the web.
    Starts from the url https://en.wikipedia.org/wiki/Space_exploration and downloads all
    links to other wiki articles in a breadth first manner.
    Only downloads english articles, ignores links to sections in the same page, links to images etc.
    """
import requests
from bs4 import BeautifulSoup
import time
import os
import collections

# Global variables
url_init = "https://en.wikipedia.org"                      # Site url
url_visited = []

# This method will check if the url points to a site in English or not
# Also checks for sections within the same page, images and administrative links


def excludeURL(url):
    not_english = False
    not_new_urls = (url.startswith('#') or url.endswith('.jpg') or url.startswith('//') or url.startswith('/w/index.php')
                   or ':' in url)
    if "https" in url:
        url = url.replace("https://", "")
        not_english = not(url.startswith("en"))
    return not_new_urls or not_english


# This method will save the page
def save_page(content, n):
    f = open("result" + str(n) + ".txt", 'w+')
    f.write(str(content))
    f.close()


def bfs_crawler(seed):
    url_count = 0
    url_depth = []
    url_queue = collections.deque([{'link': seed, 'depth': 1}])  # Initialize url queue with link and depth
    while len(url_queue) > 0 and len(url_visited) < 1000:
        to_visit = url_queue.pop()                             # Get url from the queue
        if to_visit['link'] not in url_visited:                # Proceed only if it has not been already crawled
            curr_depth = to_visit['depth']
            url_visited.append(to_visit['link'])               # Append to visited list
            url_count += 1
            url_depth.append(curr_depth)
            # Sleep for a second before crawling
            time.sleep(1)
            page = requests.get(to_visit['link'])
            save_page(page.content, url_count)                 # Call to save page
            soup = BeautifulSoup(page.content, 'html.parser')  # Use beautiful soup object to parse the document
            urls = soup.findAll("a", href=True)                # Fetch all links from the document
            if curr_depth < 6:   # Fetch more urls only if the link is within depth 6.
                for i in urls:
                     # For a url in depth 6, we need not add more urls to the queue
                    if not excludeURL(i['href']):
                        url = url_init + i['href'] if i['href'].startswith('/') else i['href']  # append site url if not already present
                        url_queue.append({'link': url, 'depth': curr_depth + 1})  # add to queue to be crawled


    return url_visited, url_count, url_depth





if __name__ == "__main__":
    seed = "https://en.wikipedia.org/wiki/Space_exploration"
    # 1. Call BFS crawling
    url_list, url_count, url_depth = bfs_crawler(seed)
    print('Url Count: ', url_count)
    print('Url Depth: ', url_depth)
    f = open("bfs_urls.txt", 'w+')
    for item in url_list:
        f.write("%s\n" % item)
    f.close()






