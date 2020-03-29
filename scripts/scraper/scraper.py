import urllib.request
import os
from pathlib import Path

from bs4 import BeautifulSoup

from scripts.scraper import scraper_util

UCSB_SITE = 'https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/presidential-candidates-debates-1960-2016'
LINK_FILE = 'transcript_links.txt'
TRANSCRIPT_DIRECTORY = Path('../../data/transcripts/')

if not os.path.exists(TRANSCRIPT_DIRECTORY):
    os.makedirs(TRANSCRIPT_DIRECTORY)

with urllib.request.urlopen(UCSB_SITE) as response:
    ucsb_html = response.read()

# BeautifulSoup HTML Parser, see docs for details:
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
ucsb_soup = BeautifulSoup(ucsb_html, 'html.parser')

# all links are housed in table cells of class="xl77"
transcript_links = list()
for cell in ucsb_soup.find_all(class_='xl77'):
    a_tag = cell.find('a')

    # filter out non-link cells
    if a_tag is not None:
        link = a_tag['href']
        transcript_links.append(link)

# Store links to a file for future reference
with open(LINK_FILE, 'w') as f:
    for link in transcript_links:
        f.write(link + '\n')

# Get the transcript from each of the links
for link in transcript_links:
    
    with urllib.request.urlopen(link) as response:
        transcript_html = response.read()

    transcript_soup = BeautifulSoup(transcript_html, 'html.parser')

    # Get the title for the transcript
    title_tag = transcript_soup.find(class_='field-ds-doc-title').contents[1]
    title = title_tag.contents[0]

    # Pull the date of the debate from the file
    date_tag = transcript_soup.find(class_='field-docs-start-date-time').contents[1]
    date = date_tag['content']

    # Get the text of the debate
    text_tags = transcript_soup.find(class_='field-docs-content').contents
    text = ''
    for tag in text_tags:
        text += scraper_util.stringify_soup(tag)

    # name the file the transcript's pid field from the UCSB site
    pid = link.split('=')[-1]
    filepath = Path(TRANSCRIPT_DIRECTORY, pid + '.txt')

    with open(filepath, 'w') as f:
        f.write(title + '\n')
        f.write(date + '\n\n')
        f.write(text + '\n')

