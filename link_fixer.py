import os
import re
import sys
from pathlib import Path

# Regex to find Markdown links [text](path) and images ![alt](path)
# Ignores web links starting with http://, https://, or mailto:
LINK_REGEX = re.compile(r'!?\[([^\]]*?)\]\(((?!http://|https://|mailto:)[^)]+)\)')

def find_closest_file(target_name, search_root):
    """Searches the repository for a file matching target_name."""
    for path in Path(search_root).rglob('*'):
        if path.is_file() and path.name.lower() == target_name.lower():
            return path
    return None

def fix_markdown_file(file_path, repo_root):
    """Scans and fixes broken links within a single markdown file."""
    file_path = Path(file_path)
    file_dir = file_path.parent
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    matches = LINK_REGEX.findall(content)
    if not matches:
        return

    updated_content = content
    changes_made = False

    for text, link_path in matches:
        # Clean potential anchor tags or query parameters from link
        clean_link = link_path.split('#')[0].split('?')[0]
        full_target_path = (file_dir / clean_link).resolve()

        # If the file doesn't exist, it's a broken link!
        if not full_target_path.exists():
            target_name = Path(clean_link).name
            found_path = find_closest_file(target_name, repo_root)

            if found_path:
                # Calculate the new relative path from the MD file to the found asset
                new_relative_path = os.path.relpath(found_path, file_dir)
                # Keep original anchor tag if it existed
                if '#' in link_path:
                    new_relative_path += '#' + link_path.split('#')[1]
                
                updated_content = updated_content.replace(f"({link_path})", f"({new_relative_path})")
                print(r"  [FIXED] 🛠️ Broken: '{link_path}' -> Found at: '{new_relative_path}'")
                changes_made = True
            else:
                print(f"  [WARNING] ❌ Could not locate asset: '{link_path}' anywhere in repo.")

    if changes_made:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

def main():
    # Use current working directory if no path is provided
    repo_root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    repo_root = Path(repo_root).resolve()

    print(f"🔍 Scanning directory: {repo_root} for broken markdown links...")
    
    md_files = list(repo_root.rglob('*.md'))
    if not md_files:
        print("No .md files found.")
        return

    for md_file in md_files:
        print(f"Checking: {md_file.relative_to(repo_root)}")
        fix_markdown_file(md_file, repo_root)

    print("\n✅ Scan complete!")

if __name__ == "__main__":
    main()
