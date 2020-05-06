import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("../../data/debate_transcripts_v3_sentiment.csv")
by_cycle_subjectivity = data.groupby("election_cycle")["subjectivity"].mean()
data["emotion"] = abs(data["polarity"])
print(data.head())
by_cycle_polarity = data.groupby("election_cycle")["emotion"].mean()


fig, ax1 = plt.subplots()

plt.xticks(by_cycle_polarity.index, rotation = 90)

color = 'tab:red'
ax1.set_xlabel('Election Cycle')
ax1.set_ylabel('Non-Neutrality', color=color)
ax1.plot(by_cycle_polarity, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Subjectivity', color=color)  # we already handled the x-label with ax1
ax2.plot(by_cycle_subjectivity, color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.title("Subjectivity and Non-Neutrality across Election Cycles")
fig.tight_layout()  # otherwise the right y-label is slightly clipped
print(plt.xticks())
plt.savefig('../../plots/emotion_cycle_means.png')
plt.show()