#!/usr/bin/python3
"""
Function that queries the Reddit API and prints
the top ten hot posts of a subreddit
"""
import re
import requests
import sys


def count_words(subreddit, word_list, after=None, count_dict=None):
    """count words function"""
    if count_dict is None:
        count_dict = {}

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0"}

    params = {"limit": 100}

    if after:
        params["after"] = after

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        posts = data["data"]["children"]

        if not posts:
            print_results(count_dict)
            return

        for post in posts:
            title = post["data"]["title"].lower()
            for word in word_list:
                count = title.count(word.lower())
                if count > 0:
                    count_dict[word] = count_dict.get(word, 0) + count

        after = data["data"]["after"]

        count_words(subreddit, word_list, after, count_dict)

    else:
        print("An error occurred while fetching data from the Reddit API.")


def print_results(count_dict):
    """printing results"""
    sorted_counts = sorted(count_dict.items(), key=lambda x: (-x[1], x[0]))
    for word, count in sorted_counts:
        print(f"{word}: {count}")


count_words("python", ["Python", "java", "javascript", "machine learning"])
