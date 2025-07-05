import requests
import xml.etree.ElementTree as ET

def fetch_posts(site_url="https://your-wordpress-site.com", per_page=100, xml_file=None):
    if xml_file:
        return fetch_posts_from_xml(xml_file)
    url = f"{site_url}/wp-json/wp/v2/posts"
    posts = []
    page = 1
    while True:
        resp = requests.get(url, params={"per_page": per_page, "page": page})
        if resp.status_code != 200:
            print(f"Error: Status code {resp.status_code}")
            print(resp.text)
            return []
        try:
            data = resp.json()
        except Exception as e:
            print("Failed to parse JSON response:")
            print(resp.text)
            raise
        if not data:
            break
        posts.extend(data)
        page += 1
    return posts

def fetch_posts_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'wp': 'http://wordpress.org/export/1.2/',
        'dc': 'http://purl.org/dc/elements/1.1/'
    }
    posts = []
    for item in root.findall('./channel/item'):
        post_type = item.find('./wp:post_type', ns)
        if post_type is not None and post_type.text != 'post':
            continue
        title = item.find('title').text if item.find('title') is not None else 'untitled'
        slug = item.find('./wp:post_name', ns)
        slug = slug.text if slug is not None else 'untitled'
        date = item.find('./wp:post_date', ns)
        date = date.text if date is not None else ''
        content = item.find('./content:encoded', ns)
        content = content.text if content is not None else ''
        posts.append({
            'title': {'rendered': title},
            'slug': slug,
            'date': date,
            'content': {'rendered': content}
        })
    return posts