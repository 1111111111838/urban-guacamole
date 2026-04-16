import requests
import sys
import re

def get_latest_posts(channel_url):
    """נכנס לעמוד התצוגה המקדימה ושולף קישורי הודעות ממוספרות"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(channel_url, headers=headers, timeout=10)
        # מחפש תבנית של קישור עם מספר בסוף בתוך הדף
        post_links = re.findall(r'href="(https://t\.me/s/[\w\d\-_]+/\d+)"', res.text)
        return post_links[-3:] # מחזיר רק את 3 ההודעות האחרונות (הכי חדשות)
    except:
        return []

def search_and_drill_down(query):
    search_url = f"https://lyzem.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(search_url, headers=headers)
        # מוצא ערוצים
        channels = re.findall(r't\.me\/[\w\d\-_]+', response.text)
        
        valid_files = []
        for ch in list(set(channels))[:5]: # בודק את 5 הערוצים הראשונים שנמצאו
            channel_name = ch.split('/')[-1]
            if channel_name == 's' or 'lyzem' in channel_name: continue
            
            preview_url = f"https://t.me/s/{channel_name}"
            print(f"Checking channel: {preview_url}...")
            
            posts = get_latest_posts(preview_url)
            valid_files.extend(posts)
            
        return list(set(valid_files))
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    search_term = sys.argv[1] if len(sys.argv) > 1 else "nature"
    print(f"--- Searching and extracting file links for: {search_term} ---")
    
    links = search_and_drill_down(search_term)
    
    if links:
        print(f"\nSUCCESS! Found {len(links)} direct file links:")
        for i, link in enumerate(links, 1):
            print(f"{i}. {link}")
    else:
        print("\nNo direct files found. Try a more popular search term.")
