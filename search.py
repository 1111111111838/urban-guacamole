import requests
from bs4 import BeautifulSoup
import sys
import re

def get_actual_posts(channel_name):
    """נכנס לדף התצוגה המקדימה של הערוץ ושולף קישורי הודעות ממוספרות"""
    url = f"https://t.me/s/{channel_name}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # מחפש קישורים שנראים כמו t.me/s/channel/123
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            # מוודא שזה קישור להודעה (מכיל מספר בסוף)
            if re.search(r't\.me/s/[\w\d\-_]+/\d+', href):
                links.append(href)
        # מחזיר את 3 הקישורים האחרונים (הכי חדשים)
        return list(set(links))[-3:]
    except:
        return []

def deep_search(query):
    # חיפוש ראשוני ב-Lyzem
    search_url = f"https://lyzem.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        resp = requests.get(search_url, headers=headers)
        # מוצא שמות ערוצים מהדף
        channels = list(set(re.findall(r't\.me\/([\w\d\-_]+)', resp.text)))
        
        all_post_links = []
        print(f"--- Found {len(channels)} potential channels. Scanning for posts... ---")
        
        for ch in channels[:5]: # סורק את 5 הערוצים הראשונים בלבד כדי לחסוך זמן
            if ch in ['s', 'lyzem', 'bot', 'joinchat']: continue
            print(f"Checking: {ch}...")
            posts = get_actual_posts(ch)
            all_post_links.extend(posts)
            
        return all_post_links
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    term = sys.argv[1] if len(sys.argv) > 1 else "nature"
    results = deep_search(term)
    
    if results:
        print(f"\nSUCCESS! Found {len(results)} direct post links:")
        for i, link in enumerate(results, 1):
            print(f"{i}. {link}")
    else:
        print("\nNo specific posts found. Try a different search term.")
