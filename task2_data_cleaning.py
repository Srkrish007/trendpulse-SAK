import os
import pandas as pd

json_file_path = "data/trends_20260409.json"

df = pd.read_json(json_file_path)
print(f"Loaded {len(df)} stories from {json_file_path}")

df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")

df = df.dropna(subset=["score", "num_comments"])

df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

df["title"] = df["title"].astype(str).str.strip()

os.makedirs("data", exist_ok=True)
df.to_csv("data/trends_clean.csv", index=False)

print(f"\nSaved {len(df)} rows to data/trends_clean.csv")

print("\nStories per category:")
for category, count in df["category"].value_counts().items():
    print(f"  {category:<15} {count}")
