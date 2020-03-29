import urllib.request
import os
import scraper_util
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

UCSB_SITE = 'https://www.presidency.ucsb.edu/documents/presidential-documents' \
            '-archive-guidebook/presidential-candidates-debates-1960-2016'
OUTPUT_DIRECTORY = "./data/"
OUTPUT_FILE = "debate_transcripts_v3.csv"

def extract_transcript_text(link):

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

    return text


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
                   'text' # Transcript text.
                ]


csv_rows = [] # List of dictionaries to be converted to a dataframe.

current_election_type = None
current_party_type = None
current_election_cycle = None

# Iterate over rows from the link.
for i, body_row in enumerate(body_rows):

    body_row_text = body_row.find_all(text=True, recursive=True)

    # debugging
    # if i == 30:
    #     break
    ##

    # Debugging
    print(str(i+1) + " rows out of " + str(len(body_rows)) + " scraped.")

    csv_row = {}
    for csv_column_name in csv_column_names:
        csv_row[csv_column_name] = None

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

    # Extract transcript text
    transcript_link = body_row.a['href']
    transcript_text = extract_transcript_text(transcript_link)

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

    csv_row['election_cycle'] = str(current_election_cycle)
    csv_row['election_type'] = current_election_type
    csv_row['party'] = current_party_type
    csv_row['debate_date'] = debate_date
    csv_row['debate_location'] = debate_location
    csv_row['link'] = transcript_link
    csv_row['text'] = transcript_text

    csv_rows.append(csv_row)

# Convert the scraped data to dataframe.
transcript_df_save = pd.DataFrame(csv_rows)

# %%
#####################################
# POST PROCESSING OF THE SCRAPED DATA
#####################################

transcript_df = transcript_df_save.copy()


transcript_df['general_debate_num'] = np.where(
        transcript_df['party'] == "Both Parties",
        transcript_df.groupby(['election_cycle', 'party']).cumcount(ascending=False)+1,
        np.NAN
)

transcript_df['dem_debate_num'] = np.where(
        transcript_df['party'] == "Democratic Party",
        transcript_df.groupby(['election_cycle', 'party']).cumcount(ascending=False)+1,
        np.NAN
)

transcript_df['rep_debate_num'] = np.where(
        transcript_df['party'] == "Republican Party",
        transcript_df.groupby(['election_cycle', 'party']).cumcount(ascending=False)+1,
        np.NAN
)

# Fill in total_dem_debate_num and total_rep_debate_num

transcript_df_dem = transcript_df.copy()
transcript_df_dem = transcript_df_dem[transcript_df_dem['party'] != "Republican Party"]
transcript_df_dem = transcript_df_dem.drop("total_rep_debate_num", 1)

transcript_df_dem['total_dem_debate_num'] = transcript_df_dem.groupby('election_cycle').cumcount(ascending=False)+1

transcript_df_rep = transcript_df.copy()
transcript_df_rep = transcript_df_rep[transcript_df_rep['party'] != "Democratic Party"]
transcript_df_rep = transcript_df_rep.drop("total_dem_debate_num", 1)

transcript_df_rep['total_rep_debate_num'] = transcript_df_rep.groupby('election_cycle').cumcount(ascending=False)+1

new_transcript_df = pd.concat([transcript_df_rep, transcript_df_dem], sort=True)

new_transcript_df = new_transcript_df[csv_column_names]

new_transcript_df = new_transcript_df.sort_index()

#######################
#######################
# A really bad/hacky way to combine the debate_cycle num information
# for the nearly duplicate rows (e.g. the general election rows)

action = {"replace_next": False, "'column_name":None, "val": None}

index = 0
for x, row in new_transcript_df.iterrows():

    if not action['replace_next']:
        if row['election_type'] == "General Election" or row['election_type'] == "General":
            action['replace_next'] = True
            if not np.isnan(row['total_rep_debate_num']):
                action['val'] = row['total_rep_debate_num']
                action['column_name'] = 'total_rep_debate_num'
            else:
                action['val'] = row['total_dem_debate_num']
                action['column_name'] = 'total_dem_debate_num'
    else:
        row[action['column_name']] = action['val']
        new_transcript_df.iloc[index] = row
        action['replace_next'] = False
    index += 1

final_transcript_df = new_transcript_df[
         (
             ~(new_transcript_df['total_dem_debate_num'].isnull()) &
             ~(new_transcript_df['total_rep_debate_num'].isnull()) &
             (new_transcript_df['party'] == "Both Parties")
          )
            |
         (new_transcript_df['party'] != "Both Parties")
    ]
#######################
#######################

# Save to data frame.
final_transcript_df.to_csv(OUTPUT_DIRECTORY + OUTPUT_FILE, index=False)
