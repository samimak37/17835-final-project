
import pandas as pd


transcript_df = pd.read_csv("../../data/debate_transcripts_by_candidate_ordered_v1.csv")


a = set(list(transcript_df["speaker"]))