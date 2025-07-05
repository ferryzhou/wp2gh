from langdetect import detect
from datetime import datetime

def only_english(posts):
    english_posts = []
    for post in posts:
        try:
            lang = detect(post.get('content', {}).get('rendered', ''))
            if lang == 'en':
                english_posts.append(post)
        except Exception:
            continue
    return english_posts

def by_date_range(posts, start=None, end=None):
    def in_range(post):
        post_date = post.get('date', '')[:10]
        if start and post_date < start:
            return False
        if end and post_date > end:
            return False
        return True
    return [post for post in posts if in_range(post)]