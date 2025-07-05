import xml.etree.ElementTree as ET

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