import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("../../data/debate_transcripts_by_candidate_after2008_sentiment.csv")

data['datetime'] =pd.to_datetime(data.debate_date)
data.sort_values(by=['datetime'], inplace=True)

by_cycle_subjectivity = data[data["speaker"] == "clinton"].groupby("debate_date", sort = False)["subjectivity"].mean()
by_cycle_polarity = data[data["speaker"] == "clinton"].groupby("debate_date", sort = False)["polarity"].mean()


fig, ax1 = plt.subplots()

plt.xticks(rotation = 90)


color = 'tab:red'
ax1.set_xlabel('Election Cycle')
ax1.set_ylabel('Polarity', color=color)
ax1.plot(by_cycle_polarity, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Subjectivity', color=color)  # we already handled the x-label with ax1
ax2.plot(by_cycle_subjectivity, color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.title("Hillary Clinton: Subjectivity and Polarity")
fig.tight_layout()  # otherwise the right y-label is slightly clipped
print(plt.xticks())
plt.savefig('../../plots/trump_sentiment.png')
plt.show()
