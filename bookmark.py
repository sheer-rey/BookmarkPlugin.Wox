import json
import os

def parse_bookmarks(bookmark_folder: list) -> dict:
    bookmarks = {}
    if not len(bookmark_folder):
        return bookmarks
    for bookmark in bookmark_folder:
        if "children" in bookmark:
            bookmarks.update(parse_bookmarks(bookmark.get("children", [])))
        elif "url" in bookmark:
            bookmarks[bookmark.get("name", "")] = bookmark.get("url", "")
    return bookmarks

def get_edge_bookmarks() -> dict:
    # Obtain bookmark file path based on operating system
    if os.name == 'nt': # Windows
        path = os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Bookmarks")
    elif os.name == 'posix': # macOS/Linux
        if os.uname().sysname == 'Darwin': # macOS
            path = os.path.expanduser("~/Library/Application Support/Microsoft Edge/Default/Bookmarks")
        else: # Linux
            path = os.path.expanduser("~/.config/microsoft-edge/Default/Bookmarks")
    else:
        print("Unsupported OS")
        return

    # load bookmarks
    with open(path, 'r', encoding='utf-8') as file:
        bookmark_data = json.load(file)
    # parse bookmarks
    bookmark_folder = bookmark_data.get('roots', {}).get('bookmark_bar', {}).get('children', [])
    return parse_bookmarks(bookmark_folder)

def search_bookmark(key: str) -> dict:
    result = {}
    bookmarks = get_edge_bookmarks()
    for k, v in bookmarks.items():
        if key.lower() in k.lower():
            result[k] = v
    return result

if __name__ == '__main__':
    results = search_bookmark(input("输入一些关键字："))
    for k, v in results.items():
        print(f"{k} -> ({v})")
