import requests
from bs4 import BeautifulSoup
import sys
import re

def get_actual_posts(channel_s_url):
    """סורק את דף התצוגה המקדימה של הערוץ ושולף קישורי הודעות"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(channel_s_url, headers=headers, timeout=10)
        # מחפש קישורים שנראים כמו t.me/s/channel/123
        # אנחנו מחפשים בתוך ה-HTML את כל הקישורים שנגמרים במספר
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if re.search(r't\.me/s/[\w\d\-_]+/\d+', href):
                links.append(href)
        return links[-5:] # מחזיר את 5 ההודעות האחרונות (הכי חדשות)
    except:
        return []

def search_telegram_deep(query):
    # חיפוש ראשוני לקבלת רשימת ערוצים
    search_url = f"https://lyzem.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        resp = requests.get(search_url, headers=headers)
        # מוצא שמות ערוצים
        channels = list(set(re.findall(r't\.me\/([\w\d\-_]+)', resp.text)))
        
        final_links = []
        print(f"מצאתי {len(channels)} ערוצים פוטנציאליים. סורק הודעות...")
        
        for ch in channels[:5]: # בודק את 5 הערוצים הראשונים
            if ch in ['s', 'lyzem', 'bot']: continue
            preview_url = f"https://t.me/s/{ch}"
            print(f"בודק הודעות בערוץ: {ch}...")
            posts = get_actual_posts(preview_url)
            final_links.extend(posts)
            
        return list(set(final_links))
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    term = sys.argv[1] if len(sys.argv) > 1 else "nature"
    print(f"--- חיפוש עמוק עבור: {term} ---")
    
    results = search_telegram_deep(term)
    
    if results:
        print(f"\nנמצאו {len(results)} קישורי הודעות ישירים:")
        for i, link in enumerate(results, 1):
            print(f"{i}. {link}")
    else:
        print("\nלא נמצאו הודעות ספציפיות. נסה מילת חיפוש אחרת (למשל 'clips' או 'video').")
