import pandas as pd
from textblob import TextBlob

data = pd.read_csv("../../data/debate_transcripts_by_candidate_ordered_v2.csv")
print(data.head)

print(data.columns)

print(data['election_cycle'])


subjectivity = []
polarity = []

for row in data.iterrows():
    try:
     debate_text = TextBlob(row[1]["text"])
     print(debate_text.sentiment)
     subjectivity.append(debate_text.sentiment.subjectivity)
     polarity.append(debate_text.sentiment.polarity)
    except:
     subjectivity.append(0.5)
     polarity.append(0.0)

data["subjectivity"] = subjectivity
data["polarity"] = polarity

print(data.head)
data.to_csv(r'../../data/debate_transcripts_by_candidate_ordered_v2_sentiment.csv', index = False, header=True)
