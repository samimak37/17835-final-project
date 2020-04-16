class Speaker:
    """
    Stores the information and text of a participant in a debate
    """

    def __init__(self, name):
        self.name = name
        self.text = list()


class Debate:
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

        # Keep track of the participants in the debate
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

                # If the speaker has been assigned, save it before it is overwritten
                if current_speaker is not None:
                    
                    # If this is a new speaker, add them to the dictionary
                    if current_speaker not in self.speakers:
                        self.speakers[current_speaker] = Speaker(current_speaker)

                    self.speakers[current_speaker].text.append(current_text)

                # Keep track of the new speaker and text
                current_speaker = line.split(':')[0]
                current_text = line.split(':')[1]

                continue

            # If the line doesn't have :, assume that the old speaker is still speaking
            else:
                current_text += line

        print(self.speakers['BUSH'].text)

