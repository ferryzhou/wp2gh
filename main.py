import argparse
import wordpress_api
import filter
import convert
import subprocess
import os
import tempfile

def main():
    parser = argparse.ArgumentParser(description="Copy WordPress posts to GitHub Pages blog.")
    parser.add_argument('--site', help='Source WordPress site URL (e.g., https://example.com)')
    parser.add_argument('--xml', help='Path to local WordPress exported XML file')
    parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)', default=None)
    parser.add_argument('--end-date', help='End date (YYYY-MM-DD)', default=None)
    parser.add_argument('--repo', help='Destination GitHub Pages repository URL (e.g., https://github.com/user/repo.git)')
    args = parser.parse_args()

    if not args.site and not args.xml:
        parser.error('You must specify either --site or --xml.')

    if args.xml:
        posts = wordpress_api.fetch_posts_from_xml(xml_file=args.xml)
    else:
        posts = wordpress_api.fetch_posts(site_url=args.site)

    if args.start_date or args.end_date:
        posts = filter.by_date_range(posts, start=args.start_date, end=args.end_date)
    english_posts = filter.only_english(posts)
    markdown_files = convert.posts_to_markdown(english_posts)

    if not args.repo:
        # Write to local output directory if no repo is specified
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        convert.write_files(markdown_files, output_dir=output_dir)
        print(f"Posts written to local directory: {output_dir}")
    else:
        # Use a temp dir for the repo
        with tempfile.TemporaryDirectory() as tmpdir:
            # Clone the repo
            subprocess.run(['git', 'clone', args.repo, tmpdir], check=True)
            posts_dir = os.path.join(tmpdir, '_posts')
            os.makedirs(posts_dir, exist_ok=True)
            convert.write_files(markdown_files, output_dir=posts_dir)

            # Create a new branch
            branch_name = 'add-wordpress-posts'
            subprocess.run(['git', '-C', tmpdir, 'checkout', '-b', branch_name], check=True)
            subprocess.run(['git', '-C', tmpdir, 'add', '_posts'], check=True)
            subprocess.run(['git', '-C', tmpdir, 'commit', '-m', 'Add WordPress posts'], check=True)
            subprocess.run(['git', '-C', tmpdir, 'push', '-u', 'origin', branch_name], check=True)

            print(f"Posts pushed to branch '{branch_name}'. Please create a pull request on GitHub.")

if __name__ == "__main__":
    main()