# wp2gh

extract wordpress content to github pages

## Prerequisites

- You need to setup a github repo for your blog first. See https://chadbaldwin.net/2021/03/14/how-to-build-a-sql-blog.html.

## Installation

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

First, export your wordpress blog as an xml file.

Then run the following command to extract the content and push to github pages.

```bash
python main.py --xml=/path/to/your/wordpress-export.xml --repo=https://github.com/username/repo.git
```

