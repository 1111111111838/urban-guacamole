import requests
import sys
import re

def search_telegram_final(query):
    # שלב 1: מציאת ערוצים דרך Lyzem
    search_url = f"https://lyzem.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        print(f"--- Searching for: {query} ---")
        resp = requests.get(search_url, headers=headers, timeout=15)
        # מוצא שמות ערוצים (למשל nature_r)
        channels = list(set(re.findall(r't\.me\/([\w\d\-_]+)', resp.text)))
        
        final_links = []
        # שלב 2: כניסה לכל ערוץ ומציאת הודעות ממוספרות
        for ch in channels[:5]:
            if ch in ['s', 'lyzem', 'bot', 'joinchat', 'search']: continue
            
            preview_url = f"https://t.me/s/{ch}"
            print(f"Exploring channel: {ch}...")
            
            try:
                ch_resp = requests.get(preview_url, headers=headers, timeout=10)
                # מחפש קישורים להודעות ספציפיות: t.me/s/channel/123
                posts = re.findall(rf't\.me/s/{ch}/\d+', ch_resp.text)
                for p in posts:
                    link = "https://" + p
                    if link not in final_links:
                        final_links.append(link)
            except:
                continue
                
        return final_links
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    search_term = sys.argv[1] if len(sys.argv) > 1 else "video"
    results = search_telegram_final(search_term)
    
    if results:
        print(f"\nSUCCESS! Found {len(results)} file links:")
        for i, link in enumerate(results[:10], 1): # מציג עד 10 תוצאות
            print(f"{i}. {link}")
    else:
        print("\nNo direct posts found. Try searching for something like 'nature video' or 'archive'.")
