import urllib.request
import re
from bs4 import BeautifulSoup
import scripts.scraper.cleaning as cleaning

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
    pattern = '\s*\[.*?\]\s*'
    text = re.sub(pattern, ' ', text)

    # Remove things inside parentheses. e.g. (applause), (laughter) (crosstalk)
    pattern = '\s*\(.*?\)\s*'
    text = re.sub(pattern, ' ', text)

    # Replace new line characters with ' '
    text = re.sub('\n', ' ', text)

    return text


# Helper function
# Determines whether a tag should be skipped while parsing
def skip_tag(tag, tag_index):

    watch_words = ["participants", "candidates", "(unknown"]

    # We don't want to include the list of moderators that happens
    # at the beginning of these transcripts.
    if tag_index < 2:
        watch_words.extend(['moderator', 'moderators'])

    watch_words.extend([word + ":" for word in watch_words])

    try:
        if tag.find('strong').text.lower() in watch_words:
            return True
    except AttributeError:
        pass

    try:
        if tag.find('b').text.lowr() in watch_words:
            return True
    except AttributeError:
        pass

    try:
        if tag.text.lower() in ["(laughter)", "(crosstalk)", "(applause)", "(applause.)"]:
            return True
    except AttributeError:
        pass

    return False


# Helper function
# Determines whether there is a new speaker, and returns the name of the speaker if so,
# otherwise returns '' for the name.
def is_new_speaker(tag, year):

    if year >= 2008:
        speaker_name = ""
        new_speaker = True if tag.find('strong') else False

        if new_speaker:
            speaker_name = tag.find('strong').text

            if speaker_name:
                speaker_name = speaker_name[:-1] if speaker_name[-1] == ":" else speaker_name

        if not new_speaker:
            new_speaker = True if tag.find('b') else False
            if new_speaker:
                speaker_name = tag.find('b').text
                speaker_name = speaker_name[:-1] if speaker_name[-1] == ":" else speaker_name

    else:   # per 2008

        speaker_name = ""
        new_speaker = False

        # If the tag has :, it's a new speaker candidate
        if ':' in tag.text and not new_speaker:
            colon_split = tag.text.split(':')
            candidate_speaker_name = colon_split[0]

            # Fix issues in this one: https://www.presidency.ucsb.edu/documents/democratic-presidential-candidates-debate-manchester-new-hampshire
            candidate_speaker_name = re.sub("PRESIDENTIAL CANDIDATE", "", candidate_speaker_name)

            # Check if the candidate "speaker" has a reasonable length and remove false positives
            if len(candidate_speaker_name) > 30 or candidate_speaker_name in cleaning.non_speakers_colon:
                pass
            else:
                speaker_name = candidate_speaker_name
                new_speaker = True

        if '.' in tag.text and not new_speaker:
            period_splits = tag.text.split('.')
            candidate_speaker_name = period_splits[0]

            # check if the first element is a title
            for title in cleaning.titles:
                if title in candidate_speaker_name.upper():

                    # add the name to the title
                    candidate_speaker_name += "." + period_splits[1]
                    break

            # If the length of the string suspected to be a speaker is too long, assume it is just text
            if len(candidate_speaker_name) > 30 or \
                len(candidate_speaker_name.split(' ')) > 3 or \
                candidate_speaker_name in cleaning.non_speakers_period:
                    pass
            else:
                speaker_name = candidate_speaker_name
                new_speaker = True

    ########################

    speaker_name = speaker_name.lower()
    pattern = '\s*\((laughter)\)\s*'
    speaker_name = re.sub(pattern, '', speaker_name)
    pattern = '\s*\((applause)\)\s*'
    speaker_name = re.sub(pattern, '', speaker_name)
    pattern = '\s*\((\?)\)\s*'
    speaker_name = re.sub(pattern, '', speaker_name)

    return new_speaker, speaker_name

# %%
def extract_transcript_text(link, year):
    """
    Parse text of a transcript.
    :param link: Link to the transcript document
    :return: transcript_text - a list of tuples where transcript_text[i] corresponds to the ith text block, where a text
    block is defined as a stretch of text spoken by the same person.
    In each tuple, the first element is the speaker (e.g. transcript_text[i][0]), and
     the second element is the text (e.g. transcript_text[i][1]).
    """

# %%
    # Debugging
    # link = "https://www.presidency.ucsb.edu/documents/democratic-candidates-forum-drake-university-des-moines-iowa"
    # link = "https://www.presidency.ucsb.edu/documents/republican-presidential-candidates-debate-the-ronald-reagan-library-and-museum-simi-valley"
    # link = "https://www.presidency.ucsb.edu/documents/republican-candidates-debate-las-vegas-nevada-0"
    # link = "https://www.presidency.ucsb.edu/documents/republican-presidential-candidates-debate-phoenix-arizona"
    # year = 1999

    # Problem transcripts:
    # https://www.presidency.ucsb.edu/documents/vice-presidential-debate-atlanta-georgia
    # https://www.presidency.ucsb.edu/documents/presidential-debate-chicago
    # https://www.presidency.ucsb.edu/documents/debate-between-the-president-and-former-vice-president-walter-f-mondale-louisville

    # link = "https://www.presidency.ucsb.edu/documents/republican-presidential-candidates-debate-phoenix-arizona"
    # link = "https://www.presidency.ucsb.edu/documents/vice-presidential-debate-atlanta-georgia"
    # year = 1999
    # link = "https://www.presidency.ucsb.edu/documents/vice-presidential-debate-centre-college-danville-kentucky-0"
    # year = 2008
    # link = "https://www.presidency.ucsb.edu/documents/republican-presidential-candidates-debate-the-ronald-reagan-library-and-museum-simi-valley"
    # link = "https://www.presidency.ucsb.edu/documents/presidential-campaign-debate-1"
    # year = 1976

    with urllib.request.urlopen(link) as response:
        transcript_html = response.read()

    transcript_soup = BeautifulSoup(transcript_html, 'html.parser')

    # Get the text of the debate
    text_tags = transcript_soup.find(class_='field-docs-content').findAll('p')

    # Thing we are returning. Will be a list of tuples t, where
    # the ith element corresponds to ith 'text block', where a text block
    # is defined as speech that is spoken consecutively by the same person.
    # t[i][0] will be the candidate name, and t[i][1] will be the text being spoken.

    text_blocks_list = []

    current_block_text = ""
    current_block_speaker = ""

    current_tag_index = 0
    while current_tag_index < len(text_tags):

        # current_tag_index = 282

        current_tag = text_tags[current_tag_index]

        if skip_tag(current_tag, current_tag_index):
            current_tag_index += 1
            continue


        # Check if the speaker has changed.
        new_speaker, new_speaker_name = is_new_speaker(current_tag, year)

        # Get the text spoken by the current speaker (modulo the speaker's name - fix next).
        current_tag_text = format_text(current_tag)

        # Don't include the speaker's name in the text (or the proceeding : and .)
        if new_speaker:
            current_tag_text = current_tag_text[len(new_speaker_name)+1:]

        # if speaker changed, add current block to list
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

    text_blocks_list.append((current_block_speaker, current_block_text))

    #######################################

    # Sometimes for whatever reason the same person will speak consecutively but
    # will be given a new 'block' in the transcript.
    # We will fix this here.
    new_text_blocks_list = []

    current_text = ""
    current_speaker = text_blocks_list[0][0]

    for new_speaker, new_text in text_blocks_list:

        if current_speaker != new_speaker:
            new_text_blocks_list.append((current_speaker, current_text))

            current_speaker = new_speaker
            current_text = new_text
        else:
            current_text = current_text + new_text

    new_text_blocks_list.append((current_speaker, current_text))

# %%
    return new_text_blocks_list
