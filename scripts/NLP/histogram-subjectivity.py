import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("../../data/debate_transcripts_by_candidate_ordered_v2_sentiment.csv")
by_cycle_subjectivity = data.groupby("election_cycle")["subjectivity"].mean()
by_cycle_polarity = data.groupby("election_cycle")["polarity"].mean()


plt.hist(data["subjectivity"], bins = 13, edgecolor='white', linewidth=1.2)
plt.title("Subjectivity Over All Candidate Debate Statements")
plt.savefig('../../plots/subjectivity_histogram.png')
plt.show()