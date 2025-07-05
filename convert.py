import os
from markdownify import markdownify as md

def posts_to_markdown(posts):
    files = []
    for post in posts:
        title = post.get('title', {}).get('rendered', 'untitled')
        slug = post.get('slug', 'untitled')
        date = post.get('date', '')[:10]
        content = post.get('content', {}).get('rendered', '')
        # Preserve all whitespaces in content
        md_content = md(content, strip=[''], convert_whitespace=True)
        md_file = f"""---
title: "{title}"
date: {date}
---

{md_content}
"""
        files.append((f"{date}-{slug}.md", md_file))
    return files

def write_files(markdown_files, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for filename, content in markdown_files:
        with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
            f.write(content)