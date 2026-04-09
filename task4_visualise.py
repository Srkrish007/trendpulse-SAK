import os
import pandas as pd
import matplotlib.pyplot as plt


file_path = "data/trends_analysed.csv"
df = pd.read_csv(file_path)

os.makedirs("outputs", exist_ok=True)



def shorten_title(title, max_len=50):
    if len(title) > max_len:
        return title[:max_len] + " ..."
    return title



top_10 = df.nlargest(10, "score")

plt.figure(figsize=(10, 6))
plt.barh(range(len(top_10)), top_10["score"], color="steelblue")
plt.yticks(range(len(top_10)), [shorten_title(t) for t in top_10["title"]], fontsize=9)
plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.tight_layout()


plt.savefig("outputs/chart1_top_stories.png", dpi=150)
plt.show()



cat_counts = df["category"].value_counts()

plt.figure(figsize=(8, 5))
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
plt.bar(cat_counts.index, cat_counts.values, color=colors, edgecolor="black", linewidth=0.7)
plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("outputs/chart2_categories.png", dpi=150)
plt.show()



plt.figure(figsize=(8, 6))

popular = df[df["is_popular"]]
not_popular = df[~df["is_popular"]]

plt.scatter(
    popular["score"], popular["num_comments"],
    label="Popular", alpha=0.6, c="tab:blue", s=30
)
plt.scatter(
    not_popular["score"], not_popular["num_comments"],
    label="Not Popular", alpha=0.6, c="tab:orange", s=30
)

plt.title("Score vs Number of Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("outputs/chart3_scatter.png", dpi=150)
plt.show()



fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("TrendPulse Dashboard", fontsize=16)


top_10 = df.nlargest(10, "score")
axes[0, 0].barh(
    range(len(top_10)), top_10["score"],
    color="steelblue"
)
axes[0, 0].set_yticks(range(len(top_10)))
axes[0, 0].set_yticklabels([shorten_title(t) for t in top_10["title"]], fontsize=8)
axes[0, 0].set_title("Top 10 Stories by Score")
axes[0, 0].set_xlabel("Score")


axes[0, 1].bar(
    cat_counts.index, cat_counts.values,
    color=colors, edgecolor="black", linewidth=0.7
)
axes[0, 1].set_title("Stories per Category")
axes[0, 1].set_ylabel("Count")
axes[0, 1].tick_params(axis="x", rotation=45)


popular = df[df["is_popular"]]
not_popular = df[~df["is_popular"]]

axes[1, 0].scatter(
    popular["score"], popular["num_comments"],
    label="Popular", alpha=0.7, c="tab:blue", s=30
)
axes[1, 0].scatter(
    not_popular["score"], not_popular["num_comments"],
    label="Not Popular", alpha=0.7, c="tab:orange", s=30
)
axes[1, 0].set_title("Score vs Comments")
axes[1, 0].set_xlabel("Score")
axes[1, 0].set_ylabel("Comments")
axes[1, 0].legend(fontsize=9)
axes[1, 0].grid(alpha=0.3)


axes[1, 1].axis("off") 

plt.tight_layout()
plt.savefig("outputs/dashboard.png", dpi=150)
plt.show()
