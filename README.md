# Smart Markdown Link & Image Fixer 🛠️

A lightweight, automated Python CLI tool designed to find and repair broken relative links and broken image assets across your project's `.md` files. 

### 🛑 The Problem
Moving files around, refactoring repository structures, or renaming folders frequently breaks Markdown documentation links (`[text](../path)`) and image rendering (`![alt](images/pic.png)`). Finding and fixing these manually in large repositories is tedious.

### ✨ The Solution
This tool scans your repository for `.md` files, verifies if local file targets exist, and utilizes localized search to automatically correct broken relative paths dynamically.

## 🚀 Getting Started

### Run the Script
You can target your current repository or pass a specific path:

```bash
# Run in the current directory
python link_fixer.py

# Run on a specific target directory
python link_fixer.py /path/to/another/repo
```

## 📋 Features
- **Auto-Discovery:** Automatically finds all `.md` files recursively.
- **Intelligent Remapping:** Calculates accurate relative steps (`../`) based on file locations.
- **Anchor Preserving:** Preserves internal link bookmarks (`#heading-tags`).
