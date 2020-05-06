import scripts.scraper.old.parser.cleaning_pre_2008 as cleaning

class Speaker:
    """
    Stores the information and text of a participant in a debate
    """

    def __init__(self, name):
        self.name = name
        self.text = list()


class DebatePre2008:
    """
    Stores the information about a specific debate
    """

    def __init__(self, debate_row):
        """
        Initializes a new Debate Object

        :param debate_row: a single Pandas row from the csv dataframe
        """
        
        # Load data from the dataframe row
        self.election_cycle = debate_row['election_cycle']
        self.election_type = debate_row['election_type']
        self.party = debate_row['party']
        self.debate_date = debate_row['debate_date']
        self.debate_location = debate_row['debate_location']
        self.general_debate_num = debate_row['general_debate_num']
        self.total_dem_debate_num = debate_row['total_dem_debate_num']
        self.total_rep_debate_num = debate_row['total_rep_debate_num']
        self.dem_debate_num = debate_row['dem_debate_num']
        self.rep_debate_num = debate_row['rep_debate_num']
        self.link = debate_row['link']
        self.text = debate_row['text']

        # Keep track of the participants in the debate as Speaker objects
        self.speakers = dict()

        # separate the text into different speakers
        self.parse_text()

    def parse_text(self):
        """
        Parses this debate's text to split it into parts that have been spoken by
        different speakers. These are stored in the speakers dict.
        """

        # keep track of the current speaker and text accumulated so far
        current_speaker = None
        current_text = ''

        # First try to split the data by :
        for line in self.text.splitlines():

            # If the row has :, it's a new speaker
            if ':' in line:

                # Check if the detected "speaker" has a reasonable length and remove false positives
                speaker = line.split(':')[0]
                if len(speaker) > 30 or speaker in cleaning.non_speakers_colon:
                    current_text += line
                    continue

                # If the speaker has been assigned, save it before it is overwritten
                if current_speaker is not None:
                    
                    # If this is a new speaker, add them to the dictionary
                    if current_speaker not in self.speakers:
                        self.speakers[current_speaker] = Speaker(current_speaker)

                    self.speakers[current_speaker].text.append(current_text)

                # Keep track of the new speaker and text
                current_speaker = speaker
                current_text = line.split(':')[1]

            # If the line doesn't have :, assume that the old speaker is still speaking
            else:
                current_text += line


        current_speaker = None
        current_text = ''
        # If the dictionary is not empty, we can stop here
        if len(self.speakers) > 0:
            return

        # Otherwise, split based on periods
        for line in self.text.splitlines():

            period_splits = line.split('.')

            # If the line doesn't have a period, then there isn't a speaker in this scheme
            if len(period_splits) == 1:
                current_text += line
                continue

            potential_speaker = period_splits[0]
            period_splits = period_splits[1:]

            # check if the first element contains a title
            for title in cleaning.titles:
                if title in potential_speaker.upper():

                    # add the name to the title
                    potential_speaker += period_splits[0]
                    period_splits = period_splits[1:]
                    break

            # If the length of the string suspected to be a speaker is too long, assume it is just text
            if len(potential_speaker) > 30 or len(potential_speaker.split(' ')) > 3 or potential_speaker in cleaning.non_speakers_period:
                current_text += line
                continue

            # Otherwise, update the current speaker and add the text
            if current_speaker is not None:

                # If this is a new speaker, add them to the dictionary
                if current_speaker not in self.speakers:
                    self.speakers[current_speaker] = Speaker(current_speaker)

                self.speakers[current_speaker].text.append(current_text)

            current_speaker = potential_speaker

            text_without_names = ''
            for sentence in period_splits:
                text_without_names += sentence + '.'

            current_text = text_without_names
            

