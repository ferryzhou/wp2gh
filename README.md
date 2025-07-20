# wp2gh

Extract WordPress content to GitHub Pages

## Overview

wp2gh is a Python tool that converts WordPress blog exports to GitHub Pages format. It processes WordPress XML export files and converts them to Markdown files suitable for Jekyll-based GitHub Pages blogs.

## Prerequisites

- A GitHub repository set up for your blog (see [How to Build a SQL Blog](https://chadbaldwin.net/2021/03/14/how-to-build-a-sql-blog.html))
- Python 3.6 or higher
- Git (for pushing to GitHub)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd wp2gh
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Step 1: Export WordPress Content

1. Go to your WordPress website
2. Navigate to **Tools** → **Export**
3. Select your desired categories, dates, etc.
4. Click **"Download Export file"** 
5. You will receive an email with link to the XML file. Download it.

### Step 2: Convert and Push to GitHub

Run the following command to extract the content and push to GitHub Pages:

```bash
python main.py --xml=/path/to/your/wordpress-export.xml --repo=https://github.com/username/repo.git
```

My example:

```
python main.py --xml=/Users/ferryzhou/Downloads/ferryzhou.wordpress.com-2025-07-20-03_16_45/lostferry.wordpress.2025-07-20.000.xml --repo=https://github.com/ferryzhou/ferryzhou.github.io.git
```

### Step 3: Create Pull Request

The tool will:
- Create a new branch called `add-wordpress-posts`
- Push the converted posts to your repository
- Display a message with instructions

1. Go to your GitHub repository webpage
2. You'll see the new branch with updates
3. Click on the branch link
4. Create a pull request and merge it

## Command Line Options

| Option | Description | Required |
|--------|-------------|----------|
| `--xml` | Path to WordPress exported XML file | Yes |
| `--repo` | GitHub Pages repository URL | No |

## Output

- **With `--repo`**: Posts are pushed to the `_posts` directory in your GitHub repository
- **Without `--repo`**: Posts are saved to a local `output` directory

## Example

```bash
python main.py --xml=~/Downloads/my-blog-export.xml --repo=https://github.com/myusername/myblog.git
```
