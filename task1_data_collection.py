import os
import json
import time
from datetime import datetime

import requests


TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"


headers = {
    "User-Agent": "TrendPulse/1.0"
}


category_keywords = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}


def get_top_story_ids():
    try:
        response = requests.get(TOP_STORIES_URL, headers=headers, timeout=10)
        response.raise_for_status()
        story_ids = response.json()
        return story_ids[:500]
    except requests.RequestException as e:
        print(f"Could not fetch top story IDs: {e}")
        return []


def get_story_details(story_id):
    try:
        response = requests.get(ITEM_URL.format(story_id), headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Could not fetch story {story_id}: {e}")
        return None


def title_matches_category(title, keywords):
    title_lower = title.lower()
    for word in keywords:
        if word.lower() in title_lower:
            return True
    return False


def main():
    story_ids = get_top_story_ids()

    if not story_ids:
        print("No story IDs found. Exiting.")
        return

    print(f"Fetched {len(story_ids)} top story IDs")

    
    all_stories = []
    for story_id in story_ids:
        story = get_story_details(story_id)

        if story is None:
            continue

        
        if story.get("type") != "story":
            continue

        if not story.get("title"):
            continue

        all_stories.append(story)

    print(f"Fetched details for {len(all_stories)} stories")

    collected_stories = []
    used_post_ids = set()

    
    for category, keywords in category_keywords.items():
        count = 0

        for story in all_stories:
            if count >= 25:
                break

            post_id = story.get("id")
            title = story.get("title", "")

            
            if post_id in used_post_ids:
                continue

            
            if title_matches_category(title, keywords):
                story_data = {
                    "post_id": story.get("id"),
                    "title": story.get("title"),
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                collected_stories.append(story_data)
                used_post_ids.add(post_id)
                count += 1

        print(f"{category}: collected {count} stories")

       
        time.sleep(2)

   
    os.makedirs("data", exist_ok=True)

  
    file_date = datetime.now().strftime("%Y%m%d")
    file_name = f"data/trends_{file_date}.json"

    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(collected_stories, file, indent=4, ensure_ascii=False)

    print(f"Collected {len(collected_stories)} stories. Saved to {file_name}")


if __name__ == "__main__":
    main()  
