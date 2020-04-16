import urllib.request
import re
from bs4 import BeautifulSoup

#######################
# Functions to parse the text in an individual transcript.
#######################

# Helper function
# Returns all the text from a bs4 soup object
def stringify_soup(soup):
    if soup.string is not None:
        return soup.string

    text = ''
    for child in soup.children:
        text += stringify_soup(child)

    return text

# Helper function
# Gets only the words spoken by participants
def format_text(tag):

    # Remove html tags
    text = stringify_soup(tag)

    # Remove things inside brackets. e.g. [applause], [laughter]
    pattern = '\s\[.*?\]\s'
    text = re.sub(pattern, '', text)

    # Remove all characters up to first ':'.
    text = re.sub('.*:', '', text)

    # Replace new line characters with ' '
    text = re.sub('\n', ' ', text)

    return text

# Helper function
# Determines whether a tag should be skipped while parsing
def skip_tag(tag):
    try:
        if tag.find('strong').text == 'PARTICIPANTS:':
            return True
    except AttributeError:
        pass

    try:
        if tag.find('b').text == 'PARTICIPANTS:':
            return True
    except AttributeError:
        pass

    return False

# Helper function
# Determines whether there is a new speaker, and returns the name of the speaker if so,
# otherwise returns '' for the name.
def is_new_speaker(tag):
    speaker_name = ""
    new_speaker = True if tag.find('strong') else False
    if new_speaker:
        speaker_name = tag.find('strong').text[:-1].lower()
    else:
        new_speaker = True if tag.find('b') else False
        if new_speaker:
            speaker_name = tag.find('b').text[:-1].lower()

    return new_speaker, speaker_name

def extract_transcript_text(link):

    """
    Parse text of a transcript.
    :param link: Link to the transcript document
    :return: transcript_text - a list of tuples where transcript_text[i] corresponds to the ith text block, where a text
    block is defined as a stretch of text spoken by the same person.
    In each tuple, the first element is the speaker (e.g. transcript_text[i][0]), and
     the second element is the text (e.g. transcript_text[i][1]).
    """
    # def is_moderator_definition(tag):
    #     if tag.find('strong').text[:-1].lower() == "moderator":
    #     tag.find_all('strong').next_sibling()
    #     for hit in tag.findAll():
    #         print(hit.strip())
    #
    #     tag.find('br').next_sibling.next_sibling
    ###########################################

# %%

    # Debugging
    link = "https://www.presidency.ucsb.edu/documents/democratic-candidates-forum-drake-university-des-moines-iowa"
    #

    with urllib.request.urlopen(link) as response:
        transcript_html = response.read()

    transcript_soup = BeautifulSoup(transcript_html, 'html.parser')

    # Get the text of the debate
    text_tags = transcript_soup.find(class_='field-docs-content').findAll('p')

    text_blocks_list = []

    current_block_text = ""
    current_block_speaker = ""

    current_tag_index = 12
    while current_tag_index < len(text_tags):

        current_tag = text_tags[current_tag_index]

        if skip_tag(current_tag):
            current_tag_index += 1
            continue

        # Speaker only changes when a 'strong' text occurs.
        # This should be turned into a function that returns (new_speaker_boolean, new_speaker_name)
        new_speaker, new_speaker_name = is_new_speaker(current_tag)

        if new_speaker_name in ['moderator' or 'moderators']:
            current_tag_index += 1
            continue

        # Get the text spoken by the current speaker
        current_tag_text = format_text(current_tag)

        # speaker changed, add current block to list
        # and start parsing new block
        if new_speaker:
            if current_block_speaker:  # Only add to list if we are not at beginning of document.
                text_blocks_list.append((current_block_speaker, current_block_text))

            current_block_text = current_tag_text
            current_block_speaker = new_speaker_name

        # Speaker hasn't change. Keep adding text to current block
        else:
            current_block_text += current_tag_text

        current_tag_index += 1

# %%
    return text_blocks_list