import os
from dotenv import load_dotenv
import requests
import json
import random

load_dotenv()


def better_replace(item: str, value_to_replace: str or list, value_to_replace_with ="") -> str:
    """
    Replaces a single or list of items with an another item

    Params:
        item: The value to loop through and replace
        value_to_replace: The value(s) to replace
        value_to_replace_with: What to replace with, default is blank

    Returns:
        A string with the value(s) replaced
    """

    # flags to prevent errors
    _ValueIsStr = True if type(value_to_replace) == str else False

    item_list = list(item)

    # loop through the list version
    # of the string and replace the
    # values as necessary
    for i in range(len(item_list)):
        if _ValueIsStr:
            if item_list[i] == value_to_replace:
                item_list[i] = value_to_replace_with
            else:
                continue
        elif not _ValueIsStr:
            for j in range(len(value_to_replace)):
                if item_list[i] == value_to_replace[j]:
                    item_list[i] = value_to_replace_with
                else:
                    continue

    return "".join(item_list)


# print(better_replace(os.environ.get('GUILD_ID'), "\"", ""))

# print(int(value[0]))
# print(int(value[1]))

subreddit = input("Enter subreddit: ")

subreddit_link = f'https://www.reddit.com/r/{subreddit}/hot/.json?sort=top&t=week&limit=10'

# Asking for a random post
r = requests.get(subreddit_link, headers={'User-agent': 'Emperor'})

post_data = json.JSONDecoder().decode(r.text)

if 'error' in post_data:
    print("not found")

with open('reddit_post.json', 'w', encoding='utf-8') as post:
    post.write(json.dumps(post_data, indent=4))
post.close()
