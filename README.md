# 17.835 Final Project

## Setting Up the Web Scraper
The requirements for the webscraper can be found in `requirements.txt`. To install all of the dependencies, you can run the following in a command line:

```bash
$ pip install -r requirements.txt
```

NOTE: If you are using a Mac, it is probably necessary to call `pip3` instead of `pip`

## Using the Web Scraper
Once the dependencies are installed, all you should have to do is run `scraper.py`. This will create a new directory called `transcripts` that will house text files generated from all of the debates available from the UCSB site. Additionally, there will be a file in the base directory titled `transcript_links.txt` that will have direct links to the website for each of the transcripts.