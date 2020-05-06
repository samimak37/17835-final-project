import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("../../data/debate_transcripts_by_candidate_ordered_v2_sentiment.csv")

clinton = data[data["speaker"] == "clinton"]
print(clinton)
clinton = clinton.sort_values(by=['polarity'])
print(clinton.tail(10))
print(data.loc[1812,"text"])


new_data = data[data["polarity"] < -0.5]

bars = new_data.groupby("election_cycle")["text"].count()
print(bars)


plt.plot(bars, color = "red")
plt.title("Frequency of Highly Negative Statements by Election Cycle")
plt.xticks(bars.index, rotation = 90)
plt.savefig('../../plots/highly_neg.png')
plt.show()


new_data = data[data["polarity"] > 0.5]
bars = new_data.groupby("election_cycle")["text"].count()
print(bars)


plt.plot(bars, color = "green")
plt.title("Frequency of Highly Positive Statements by Election Cycle")
plt.xticks(bars.index, rotation = 90)
plt.savefig('../../plots/highly_pos.png')
plt.show()
