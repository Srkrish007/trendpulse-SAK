import requests
import time
import json
import os
from datetime import datetime

# Base URL and headers for the Hacker News API
BASE_URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# Keywords for each category (all checks will be case-insensitive)
CATEGORY_KEYWORDS = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"],
}

# Limits from the assignment
MAX_PER_CATEGORY = 25
MAX_TOP_IDS = 500


def fetch_top_story_ids(limit=MAX_TOP_IDS):
    """
    Fetch the top story IDs from Hacker News.
    Returns a list of integers (story IDs).
    """
    try:
        url = f"{BASE_URL}/topstories.json"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        story_ids = response.json()
        # Keep only the first 'limit' IDs
        return story_ids[:limit]
    except requests.RequestException as e:
        print("Error while fetching top stories:", e)
        return []


def fetch_item(item_id):
    """
    Fetch a single item (story) by ID.
    Returns the JSON object as a dict, or None if something goes wrong.
    """
    try:
        url = f"{BASE_URL}/item/{item_id}.json"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error while fetching item {item_id}:", e)
        return None


def categorize_title(title):
    """
    Decide which category a title belongs to based on the keywords.
    Returns one of the category names, or None if it doesn't match anything.
    """
    if not title:
        return None

    text = title.lower()

    # Simple first-match logic: go through categories in this order
    for category, keywords in CATEGORY_KEYWORDS.items():
        for word in keywords:
            if word in text:
                return category

    return None


def collect_stories():
    """
    Main logic to:
    - fetch top story IDs
    - fetch each story
    - categorise by title
    - collect up to 25 stories per category
    """
    top_ids = fetch_top_story_ids()
    if not top_ids:
        print("No top story IDs were fetched. Exiting.")
        return []

    stories = []
    stories_per_category = {cat: 0 for cat in CATEGORY_KEYWORDS.keys()}

    # Cache to avoid fetching the same item multiple times for different categories
    item_cache = {}

    # Outer loop over categories so we can sleep 2 seconds between categories
    for category in CATEGORY_KEYWORDS.keys():
        print(f"\n=== Collecting category: {category} ===")

        # Loop over all top IDs and try to fill this category
        for item_id in top_ids:
            # Stop if we have enough stories for this category
            if stories_per_category[category] >= MAX_PER_CATEGORY:
                break

            # Reuse story details if we already fetched this item before
            if item_id in item_cache:
                item = item_cache[item_id]
            else:
                item = fetch_item(item_id)
                if item is None:
                    # If a request fails, we just print above and move on
                    continue
                item_cache[item_id] = item

            # Only keep normal stories with a title
            if item.get("type") != "story" or "title" not in item:
                continue

            # Check which category this title belongs to
            assigned_category = categorize_title(item.get("title", ""))

            # If it doesn't match the current category, skip it
            if assigned_category != category:
                continue

            # Add the current timestamp in ISO format
            collected_at = datetime.now().isoformat(timespec="seconds")

            # Build the record with the required fields
            story_record = {
                "post_id": item.get("id"),
                "title": item.get("title", ""),
                "category": category,
                "score": item.get("score", 0),
                "num_comments": item.get("descendants", 0),
                "author": item.get("by", ""),
                "collected_at": collected_at,
            }

            stories.append(story_record)
            stories_per_category[category] += 1

        print(f"Finished {category} with {stories_per_category[category]} stories.")
        # Wait 2 seconds between each category (not per story)
        time.sleep(2)

    return stories


def save_to_json(stories):
    """
    Save all collected stories into data/trends_YYYYMMDD.json.
    """
    if not stories:
        print("No stories collected. Nothing to save.")
        return

    # Create data/ folder if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Use today's date in YYYYMMDD format
    today_str = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{today_str}.json"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(stories, f, ensure_ascii=False, indent=2)
        print(f"\nCollected {len(stories)} stories. Saved to {filename}")
    except OSError as e:
        print("Error while saving JSON file:", e)


if __name__ == "__main__":
    all_stories = collect_stories()
    save_to_json(all_stories)