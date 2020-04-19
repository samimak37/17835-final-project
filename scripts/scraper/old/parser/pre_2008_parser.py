import pandas as pd
from pathlib import Path

from scripts.scraper.old.parser.debate import DebatePre2008

TRANSCRIPT_CSV = Path('data', 'debate_transcripts_v3.csv')
OUTPUT_CSV = Path('data', 'debate_transcripts_by_candidate_before2008.csv')

CSV_COLUMN_NAMES = ['election_cycle', # Election year. Unique for each set of debates.
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
                   'speaker', # Speaker name
                   'text' # Speaker text. All text spoken by the speaker.
                ]

transcript_df = pd.read_csv(TRANSCRIPT_CSV)
old_cycles = transcript_df['election_cycle'] < 2007

# Subset all of the transcripts from before the 2008 cycle
pre_2008 = transcript_df[old_cycles]

# Create Debate objects for each transcript
debates = list()
for index, row in pre_2008.iterrows():
    debate = DebatePre2008(row)
    debates.append(debate)

# Create the csv file from the debates
csv_rows = list()
for debate in debates:

    debate_data = dict()

    for csv_col in CSV_COLUMN_NAMES:
        debate_data[csv_col] = None

    # Store all of the general debate values in the row
    debate_data['election_cycle'] = debate.election_cycle
    debate_data['election_type'] = debate.election_type
    debate_data['party'] = debate.party
    debate_data['debate_date'] = debate.debate_date
    debate_data['debate_location'] = debate.debate_location
    debate_data['general_debate_num'] = debate.general_debate_num
    debate_data['total_dem_debate_num'] = debate.total_dem_debate_num
    debate_data['total_rep_debate_num'] = debate.total_rep_debate_num
    debate_data['dem_debate_num'] = debate.dem_debate_num
    debate_data['rep_debate_num'] = debate.rep_debate_num
    debate_data['link'] = debate.link

    # Create new rows for each speaker in a debate
    for speaker_name in debate.speakers:

        # create a copy of the dict from the debate metadata
        row = dict(debate_data)

        # get the metadata for the speaker and add it to the csv
        speaker = debate.speakers[speaker_name]
        row['speaker'] = speaker.name
        row['text'] = speaker.text

        csv_rows.append(row)

# save the data to a csv file
df = pd.DataFrame(csv_rows)
df.to_csv(OUTPUT_CSV, index=False)



