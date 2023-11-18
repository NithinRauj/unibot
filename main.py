import os
import time
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# The URL of the website you want to start scraping from
base_url = 'https://uits.iu.edu/index.html'

# Directory path where you want to save the files
directory_path = './scraped/'

# Check if the directory exists, and create it if it doesn't
if not os.path.exists(directory_path):
    print('Creating otuput dir...')
    os.makedirs(directory_path)

# Set to keep track of visited URLs
visited_urls = set()

# Function to scrape a single page


def scrape_page(url):
    print(f'Scraping text from {url}...')
    try:
        # Terminate if url ends with .php,.pdf,.docx
        if url.endswith(('.docx', '.pdf', '.php')):
            return
        # Check if URL has already been visited
        if url in visited_urls:
            return
        visited_urls.add(url)

        # Rate limiting to avoid overwhelming the server
        time.sleep(1)  # Delay for 1 second between requests

        # Get the page content
        response = requests.get(url)
        # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()

        # Parse the page content
        soup = BeautifulSoup(response.content, 'html.parser')
        page_text = f'URL: {url}\n\n'

        content = soup.find("div", id="main-content", recursive=True)
        children_elements = content.find_all(True)
        # Format headers and paragraphs
        for element in children_elements:
            text = element.get_text(separator='\n', strip=True)
            if element.name.startswith('h') and element.name[1].isdigit():
                header_level = int(element.name[1])
                page_text += '\n' + ('#' * header_level) + ' ' + text + '\n\n'
            elif element.name == 'p':
                page_text += text + '\n\n'
            elif element.name == 'a' and element['href'].startswith('http') and text:
                page_text += f"[{text}]({element['href']})\n\n"
            # Exclude certain elements like 'Skip to content' links
            if 'Skip' in text or 'skip' in text:
                continue

        # Save the scraped text with the URL at the top
        save_text_to_file(url, page_text)

        # Find and scrape all linked pages
        for link in soup.find_all('a', href=True):
            link_url = urljoin(url, link['href'])
            # Check if the link is a valid URL and within the same domain
            if is_valid_url(link_url) and get_domain(link_url) == get_domain(base_url):
                scrape_page(link_url)
    except requests.HTTPError as e:
        print(f'HTTP Error for URL {url}: {e}')
    except requests.RequestException as e:
        print(f'Request Error for URL {url}: {e}')
    except Exception as e:
        print(f'An error occurred for URL {url}: {e}')


# Helper function to save text to a file
def save_text_to_file(url, text):
    # Create a valid filename from the URL
    filename = os.path.join(directory_path, urlparse(
        url).path.replace('/', '_').strip('_') + '.txt')
    print(f'Saving text to {filename}...')
    if not filename.endswith('.txt'):
        filename += '.txt'
    # Save the scraped text
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


# Helper function to get the domain of a URL
def get_domain(url):
    return urlparse(url).netloc


# Helper function to validate URLs
def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


# Start the scraping process
scrape_page(base_url)

print(f'Scraping completed. Check the content in {directory_path}')
