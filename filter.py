from datetime import datetime

def by_date_range(posts, start=None, end=None):
    def in_range(post):
        post_date = post.get('date', '')[:10]
        if start and post_date < start:
            return False
        if end and post_date > end:
            return False
        return True
    return [post for post in posts if in_range(post)]