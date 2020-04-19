import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("../../data/debate_transcripts_v3_sentiment.csv")
select_cycle = data[data["election_cycle"] == 2016]
print(select_cycle)

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Debates in the 2016 Election Cycle')
ax1.set_ylabel('Polarity', color=color)
ax1.plot(select_cycle["polarity"], color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Subjectivity', color=color)  # we already handled the x-label with ax1
ax2.plot(select_cycle["subjectivity"], color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
print(plt.xticks())
plt.savefig('../../plots/2016-election-trends.png')

plt.show()
