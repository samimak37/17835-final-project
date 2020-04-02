# 17.835 Final Project

## Setting Up

Install this repo via

```bash
$ git clone https://github.com/samimak37/17835-final-project.git
```

After cloning, requirements can be found in `requirements.txt`. To install all of the dependencies, you can run the 
following in a command line:

```bash
$ pip install -r requirements.txt
```

NOTE: If you are using a Mac, it is probably necessary to call `pip3` instead of `pip`



## Ideal Workflow


After cloning this repo onto your computer, make a branch for your edits.
Once you have finished making edits, merge the remote master back into your local branch before
you push your local branch to the remote repo. Then submit a pull request.

The pull request should be able to automatically merge into master since you just merged master into your 
current branch.

If you changed someone else's file, ideally you should request a review before you merge.


If you are adding to requirements.txt using `pip freeze`, please use virtual environments so that requirements.txt does not get overwhelmed with superfluous packages from
other python packages you have on your computer that may not be used in this project. 
See: \
https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/ or \
https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html


## Directory Sturcture

`misc`: Feel free to put experiments/in-progress code in , and once they are ready enough, move them to `scripts`. \
`scripts`: Code that is 'ready enough' \
`plots`:  Graphics that should go into the 5 page paper and/or the presentation board.


## Using the Webscraper - scripts/scraper/scaper.py
Once the dependencies are installed, all you should have to do is run `scraper.py`. This will create a new directory called `transcripts` that will house text files generated from all of the debates available from the UCSB site. Additionally, there will be a file in the base directory titled `transcript_links.txt` that will have direct links to the website for each of the transcripts.

## Using the Webscraper - scripts/scraper/scraper_to_csv.py
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

