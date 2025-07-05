import argparse
import wordpress_api
import convert
import subprocess
import os
import tempfile

def main():
    parser = argparse.ArgumentParser(description="Copy WordPress posts to GitHub Pages blog.")
    parser.add_argument('--xml', required=True, help='Path to local WordPress exported XML file')
    parser.add_argument('--repo', help='Destination GitHub Pages repository URL (e.g., https://github.com/user/repo.git)')
    args = parser.parse_args()

    posts = wordpress_api.fetch_posts_from_xml(xml_file=args.xml)
    markdown_files = convert.posts_to_markdown(posts)

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