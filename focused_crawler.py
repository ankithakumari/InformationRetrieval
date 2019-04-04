""" Python implementation to perform focused crawling of the web.
    Starts from the url https://en.wikipedia.org/wiki/Space_exploration and downloads all
    links to other wiki articles if they contain the keywords provided in the keyword list.
    Performs a a BFS crawl of focused urls.
    Only downloads english articles, ignores links to sections in the same page, links to images etc.
    """
import requests

from bs4 import BeautifulSoup
import time
import collections


def excludeURL(url):
    not_english = False
    not_new_urls = (url.startswith('#') or url.endswith('.jpg') or url.startswith('//') or url.startswith('/w/index.php')
                   or ':' in url)
    if "https" in url:
        url = url.replace("https://", "")
        not_english = not(url.startswith("en"))
    return not_new_urls or not_english


def match_str(string, keywords):
    if string == None:
        return False
    else:
        for w in string.split():            # Use each word in the text string to see if it exists in keywords
            if w.lower() in keywords:       # If found return True
                return True
        return False


def focused_crawler(seed, keywords):
    url_queue = collections.deque([{'link': seed, 'depth': 1}])
    url_visited = []
    url_count = 0
    dup_url = 0
    url_init = "https://en.wikipedia.org"
    while len(url_queue) > 0 and url_count < 1000:
        to_visit = url_queue.pop()
        curr_depth = to_visit['depth']
        if to_visit['link'] in url_visited:
            dup_url += 1
        else:
            time.sleep(1)                                           # wait for 1 second - politeness policy
            page = requests.get(to_visit['link'])
            soup = BeautifulSoup(page.content, 'html.parser')
            url_visited.append(to_visit['link'])
            url_count += 1
            if curr_depth <= 5:
                urls = soup.find_all('a', href=True)
                for item in urls:
                    if match_str(item.string, keywords) and not excludeURL(item['href']):  # anchor text contains keyword and is a valid url for crawling
                        url = url_init + item['href']
                        url_queue.append({'link': url, 'depth': curr_depth + 1})

    return dup_url, url_count, url_visited, curr_depth


if __name__ == "__main__":
    keywords = ["mars", "space", "orbit", "explore", "martian", "exploration", "exploring", "orbital",
                "mars exploration", "mars mission", "galaxy", "astronomy", "red planet", "Rover", "orbiter",
                "pathfinder", "spacecraft", "landers", "satellite", "observer", "mission", "planet"]
    seed = "https://en.wikipedia.org/wiki/Space_exploration"
    duplicate_count, url_count, visited_list, curr_depth = focused_crawler(seed, keywords)
    f = open("focused_urls.txt", 'w+')
    for item in visited_list:
        f.write("%s\n" % item)
    f.close()
    print(duplicate_count, url_count, curr_depth)


