# 17.835 Final Project

## Setting Up the Web Scraper
The requirements for the webscraper can be found in `requirements.txt`. To install all of the dependencies, you can run the following in a command line:

```bash
$ pip install -r requirements.txt
```

NOTE: If you are using a Mac, it is probably necessary to call `pip3` instead of `pip`

## Using the Webscraper - scaper.py
Once the dependencies are installed, all you should have to do is run `scraper.py`. This will create a new directory called `transcripts` that will house text files generated from all of the debates available from the UCSB site. Additionally, there will be a file in the base directory titled `transcript_links.txt` that will have direct links to the website for each of the transcripts.

### Using the Webscraper - scraper_to_csv.py
A new directory `data` will be created. There, a file called `debate_transcripts_v3.csv` will be placed. 
Some software (e.g. excel) incorrectly loads the data by default, since some of the fields contain
commas. The "Numbers" application that comes with macOS seems to open it fine.
Importing it as a pandas dataframe into python also works correctly:

`df = pd.read_csv("debate_transcripts_v3.csv")`

The columns of the csv are as follows:

`election_cycle` = Election year. Unique for each set of debates.\
`election_type` = Are the debates for the 'Primary Election' or 'General Election' \
`party` = Only relevant for the Primary Elections. \
`debate_date` = Month Day, Year format\
`debate_location` = The city or place the debate took place. \
`general_debate_num` = Total number debates for the general election so far in this election cycle \
`total_dem_debate_num` = Total number of debates the democrat candidate(s) have gone through in this election cycle \
`total_rep_debate_num` = Total number of debates the republican candidate(s) have gone through in this election cycle \
`dem_debate_num` = Total number debates for the democratic primary election so far in this election cycle \
`rep_debate_num` = Total number debates for the republican primary election so far in this election cycle \
`link` = Link to transcript \
`text` = Transcript text

