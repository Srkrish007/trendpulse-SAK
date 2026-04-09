import pandas as pd
import numpy as np

file_path = "data/trends_clean.csv"

df = pd.read_csv(file_path)

print(f"Loaded data: {df.shape}\n")

print("First 5 rows:")
print(df.head(), "\n")

print(f"Average score   : {df['score'].mean():,.0f}")
print(f"Average comments: {df['num_comments'].mean():,.0f}\n")

scores = df["score"].to_numpy()
comments = df["num_comments"].to_numpy()

print("--- NumPy Stats ---")
print(f"Mean score   : {np.mean(scores):,.0f}")
print(f"Median score : {np.median(scores):,.0f}")
print(f"Std deviation: {np.std(scores):,.0f}")
print(f"Max score    : {np.max(scores):,.0f}")
print(f"Min score    : {np.min(scores):,.0f}\n")

most_stories_category = df["category"].value_counts().idxmax()
most_stories_count = df["category"].value_counts().max()
print(f"Most stories in: {most_stories_category} ({most_stories_count} stories)\n")

most_commented_row = df.loc[df["num_comments"].idxmax()]
print(
    f'Most commented story: "{most_commented_row["title"]}"  — '
    f'{most_commented_row["num_comments"]:,} comments\n'
)

average_score = df["score"].mean()
df["engagement"] = df["num_comments"] / (df["score"] + 1)
df["is_popular"] = df["score"] > average_score

output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"Saved to {output_file}")
