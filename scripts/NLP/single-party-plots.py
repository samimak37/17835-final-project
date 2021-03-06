import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("../../data/debate_transcripts_v3_sentiment.csv")

parties = [("Democratic Party","dem"), ("Republican Party","rep")]


for p in parties:

    by_cycle_subjectivity = data[data["party"]==p[0]].groupby("election_cycle")["subjectivity"].mean()
    by_cycle_polarity = data[data["party"]==p[0]].groupby("election_cycle")["polarity"].mean()


    fig, ax1 = plt.subplots()

    plt.xticks(by_cycle_polarity.index, rotation = 90)

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

    plt.title("Subjectivity and Polarity in " + p[0] + " Primaries")
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    print(plt.xticks())
    plt.savefig('../../plots/election_cycle_means_'+p[1]+'.png')
    plt.show()
