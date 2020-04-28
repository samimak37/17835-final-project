import pandas as pd
from textblob import TextBlob

data = pd.read_csv("../../data/debate_transcripts_v3.csv")
print(data.head)

print(data.columns)

print(data['election_cycle'])


subjectivity = []
polarity = []

for row in data.iterrows():
     debate_text = TextBlob(row[1]["text"])
     print(debate_text.sentiment)
     subjectivity.append(debate_text.sentiment.subjectivity)
     polarity.append(debate_text.sentiment.polarity)

data["subjectivity"] = subjectivity
data["polarity"] = polarity

print(data.head)
data.to_csv(r'../../data/debate_transcripts_v3_sentiment.csv', index = False, header=True)
