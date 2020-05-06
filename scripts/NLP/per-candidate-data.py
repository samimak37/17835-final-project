import pandas as pd
from textblob import TextBlob

data = pd.read_csv("../../data/debate_transcripts_by_candidate_after2008_v1.csv")
print(data.head)

print(data.columns)

subjectivity = []
polarity = []

for row in data.iterrows():
     debate_text = TextBlob(str(row[1]["text"]))
     subjectivity.append(debate_text.sentiment.subjectivity)
     polarity.append(debate_text.sentiment.polarity)
     print(row[0])

data["subjectivity"] = subjectivity
data["polarity"] = polarity

print(data.head)
data.to_csv(r'../../data/debate_transcripts_by_candidate_after2008_sentiment.csv', index = False, header=True)