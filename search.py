import requests
import sys
import re
import urllib.parse

def search_telegram(query):
    # שימוש ב-DuckDuckGo לחיפוש באתר טלגרם
    search_url = f"https://duckduckgo.com/html/?q=site:t.me/s/+{query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        
        # חיפוש קישורי טלגרם בתוך הטקסט של הדף באמצעות Regex
        # מחפש כתובות שמתחילות ב-t.me/s/
        links = re.findall(r't\.me\/s\/[\w\d\-_/]+', response.text)
        
        # ניקוי והסרת כפילויות
        clean_links = []
        for link in links:
            full_link = "https://" + link
            if full_link not in clean_links:
                clean_links.append(full_link)
        
        return clean_links
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "קובץ דוגמה"
    print(f"--- מחפש ב-DuckDuckGo עבור: {query} ---")
    
    results = search_telegram(query)
    
    if results:
        print(f"נמצאו {len(results)} תוצאות:")
        for i, link in enumerate(results, 1):
            print(f"{i}. {link}")
    else:
        print("לא נמצאו תוצאות. נסה מונח חיפוש אחר באנגלית או בעברית.")
