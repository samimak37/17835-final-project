"""
Per-candidate resolution scraper from transcripts.
"""

import urllib.request
import os
from bs4 import BeautifulSoup
import pandas as pd
from scripts.scraper import scrape_a_transcript

UCSB_SITE = 'https://www.presidency.ucsb.edu/documents/presidential-documents' \
            '-archive-guidebook/presidential-candidates-debates-1960-2016'
OUTPUT_DIRECTORY = "../../data/"
OUTPUT_FILE = "debate_transcripts_by_candidate_ordered_v1.csv"

# %%

if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)

with urllib.request.urlopen(UCSB_SITE) as response:
    ucsb_html = response.read()

# BeautifulSoup HTML Parser, see docs for details:
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
ucsb_soup = BeautifulSoup(ucsb_html, 'html.parser')
uscb_body = ucsb_soup.find('tbody')
body_rows = uscb_body.find_all('tr')


csv_column_names = ['election_cycle', # Election year. Unique for each set of debates.
                   'election_type',   # Are the debates for the 'Primary Election' or 'General Election'
                   'party', # Only relevant for the Primary Elections.
                   'debate_date',
                   'debate_location',
                   'general_debate_num',  # Total number debates for the general election so far in this election cycle
                   'total_dem_debate_num', # Total number of debates the democrat candidate(s) have gone through in this election cycle
                   'total_rep_debate_num', # Total number of debates the republican candidate(s) have gone through in this election cycle
                   'dem_debate_num', #  Total number debates for the democratic primary election so far in this election cycle
                   'rep_debate_num', #  Total number debates for the republican primary election so far in this election cycle
                   'link', # Link to transcript
                   'block_num', # Block number, indicating how far thru a particular speech we are.
                   'speaker', # Speaker name
                   'text' # Speaker text. All text spoken consecutively by the speaker, thus forming a 'block'.
                ]


csv_rows = [] # List of dictionaries to be converted to a dataframe.

current_election_type = None
current_party_type = None
current_election_cycle = None
# %%
# Iterate over rows from the link.
# for i, body_row in enumerate(body_rows):
for i, body_row in enumerate(body_rows):

    body_row_text = body_row.find_all(text=True, recursive=True)

    # debugging:
    # if i == 5:
    #     break
    # i = 47
    # body_row = body_rows[i]
    # /debugging

    print(str(i+1) + " rows out of " + str(len(body_rows)) + " scraped.")

    ##################################################
    # EXTRACT META INFORMATION
    ##################################################

    # class 'xl74' represents the start of a new debate subtype (e.g. primary vs general)
    # within a particular election_cycle, so we reset election_type variables.
    if body_row.find(class_="xl74"):
        current_election_type = None
        current_party_type = None

    # Tags with 'xl69' uniquly identify the election_cycle.
    if body_row.find(class_="xl69"):
        current_election_cycle = body_row.find(class_="xl69").find(text=True)

        # If we have a subtag with class 'xl69' but there is no "General" tag
        # we are at or before 1996 election cycle, and we do not have primary transcripts.
        # So all debates going forward are "General"
        if "General" not in body_row_text:
            current_election_type = "General Election"
            current_party_type = "Both Parties"

    # If there is no link in this row,
    # and if it does not say "General Election", "Primary Election", "Democratic Party"
    # or "Republican Party", then it is superfluous information and we can skip this row
    key_words = ["General Election", "Primary Election", "Democratic Party", "Republican Party"]
    if (not body_row.find('a')) and \
       (not any([word in body_row_text for word in key_words])):
        continue

    # Else, check if the current row only contains meta information about type of debate.
    # If it does, record it and go the next row.
    skip = False
    for word in body_row_text:
        if word == "General Election":
            current_election_type = word
            current_party_type = "Both Parties"
            skip = True
        elif word == "Primary Election":
            current_election_type = word
            skip = True

        elif word in ["Democratic Party", "Republican Party"]:
            current_party_type = word
            skip = True

    if skip:
        continue

    ##################################################
    ##################################################

    # If we get here, the row must contain a link to a transcript
    assert body_row.find('a')
    ###

    # Get date of transcript
    debate_date = body_row.find(align="right").find(text=True)

    # Get link to transcript
    transcript_link = body_row.a['href']

    link_text = body_row.a.text
    if "Debate in the " in link_text:
        debate_location = link_text.partition("Debate in the ")[2]
    elif "Debate on " in link_text:
        debate_location = link_text.partition("Debate on ")[2]
    elif "Debate in " in link_text:
        debate_location = link_text.partition("Debate in ")[2]
    elif "Debate at the " in link_text:
        debate_location = link_text.partition("Debate at the ")[2]
    elif "Debate at " in link_text:
        debate_location = link_text.partition("Debate at ")[2]
    elif "Debate " in link_text:
        debate_location = link_text.partition("Debate ")[2]
    elif "Forum in " in link_text:
        debate_location = link_text.partition("Forum in ")[2]
    elif "Town Hall in " in link_text:
        debate_location = link_text.partition("Town Hall in ")[2]
    else:
        debate_location = link_text

    # Scraper only works properly for 2008 and after
    # if current_election_cycle and int(str(current_election_cycle)) < 2008:
    #     break

    # Call helper function
    year = int(current_election_cycle.encode('utf-8'))
    transcript_text_block_list = scrape_a_transcript.extract_transcript_text(transcript_link, year)

    for block_num, (speaker_name, speaker_text) in enumerate(transcript_text_block_list):
        # For each text block, make a new row in the dataframe.

        csv_row = {}
        for csv_column_name in csv_column_names:
            csv_row[csv_column_name] = None

        csv_row['election_cycle'] = str(year)
        csv_row['election_type'] = current_election_type
        csv_row['party'] = current_party_type
        csv_row['debate_date'] = debate_date
        csv_row['debate_location'] = debate_location
        csv_row['link'] = transcript_link
        csv_row['block_num'] = block_num+1
        csv_row['text'] = speaker_text
        csv_row['speaker'] = speaker_name

        csv_rows.append(csv_row)

# Convert the scraped data to dataframe.
transcript_df_save = pd.DataFrame(csv_rows)


# %%
#####################################
# POST PROCESSING OF THE SCRAPED DATA
#####################################

transcript_df = transcript_df_save.copy()

# Get debate counts for each type of debate during each election cycle
# ref:
# https://stackoverflow.com/questions/41750916/combined-two-dataframe-based-on-index-replacing-matching-values-in-other-column
# https://stackoverflow.com/questions/24768657/replace-column-values-based-on-another-dataframe-python-pandas-better-way

####################################
# General

generals_debates = transcript_df['party'] == "Both Parties"
general_debates_df = transcript_df.loc[generals_debates]
x = ((general_debates_df['debate_date'] != general_debates_df['debate_date'].shift(1)).cumsum()[::-1]).astype(int)
x = x.to_frame()
general_debate_nums = x.rename(columns={"debate_date": "general_debate_num"})

transcript_df.loc[generals_debates, 'general_debate_num'] = \
    general_debate_nums[['general_debate_num']].values

####################################
# Democrats

democrat_debates = transcript_df['party'] == "Democratic Party"
democrat_debates_df = transcript_df.loc[democrat_debates]
x = ((democrat_debates_df['debate_date'] != democrat_debates_df['debate_date'].shift(1)).cumsum()[::-1]).astype(int)
x = x.to_frame()
democrat_debate_nums = x.rename(columns={"debate_date": "dem_debate_num"})

transcript_df.loc[democrat_debates, 'dem_debate_num'] = \
    democrat_debate_nums[['dem_debate_num']].values

####################################
# Republicans

republican_debates = transcript_df['party'] == "Republican Party"
republican_debates_df = transcript_df.loc[republican_debates]
x = ((republican_debates_df['debate_date'] != republican_debates_df['debate_date'].shift(1)).cumsum()[::-1]).astype(int)
x = x.to_frame()
republican_debate_nums = x.rename(columns={"debate_date": "rep_debate_num"})

transcript_df.loc[republican_debates, 'rep_debate_num'] = \
    republican_debate_nums[['rep_debate_num']].values

####################################
# Republicans or General
rep_total_debates = republican_debates | generals_debates
rep_total_debates_df = transcript_df.loc[rep_total_debates]
x = ((rep_total_debates_df['debate_date'] != rep_total_debates_df['debate_date'].shift(1)).cumsum()[::-1]).astype(int)
x = x.to_frame()
rep_total_debate_nums = x.rename(columns={"debate_date": "total_rep_debate_num"})

transcript_df.loc[rep_total_debates, 'total_rep_debate_num'] = \
    rep_total_debate_nums[['total_rep_debate_num']].values

####################################
# Democrats or General
dem_total_debates = democrat_debates | generals_debates
dem_total_debates_df = transcript_df.loc[dem_total_debates]
x = ((dem_total_debates_df['debate_date'] != dem_total_debates_df['debate_date'].shift(1)).cumsum()[::-1]).astype(int)
x = x.to_frame()
total_dem_debate_nums = x.rename(columns={"debate_date": "total_dem_debate_num"})

transcript_df.loc[dem_total_debates, 'total_dem_debate_num'] = \
    total_dem_debate_nums[['total_dem_debate_num']].values

####################################
####################################

# Save to data frame.
transcript_df.to_csv(OUTPUT_DIRECTORY + OUTPUT_FILE, index=False)
