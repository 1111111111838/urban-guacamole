import requests
import sys
import re

def search_telegram_wide(query):
    # חיפוש רחב ב-Lyzem ללא סינונים קשוחים
    url = f"https://lyzem.com/search?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        # חיפוש כל מה שדומה לקישור טלגרם (t.me/something)
        raw_links = re.findall(r't\.me\/[\w\d\-_/]+', response.text)
        
        clean_links = []
        for link in raw_links:
            # הפיכה לפורמט תצוגה מקדימה ציבורי (/s/)
            if '/s/' not in link:
                parts = link.split('/')
                if len(parts) > 1:
                    formatted = f"https://t.me/s/{parts[1]}"
                    # אם יש המשך לקישור (כמו מספר), נוסיף אותו
                    if len(parts) > 2:
                        formatted += f"/{parts[2]}"
                    link = formatted
                else:
                    link = f"https://t.me/s/{parts[0]}"
            else:
                link = "https://" + link

            if link not in clean_links and "lyzem" not in link:
                clean_links.append(link)
        
        return clean_links
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    search_term = sys.argv[1] if len(sys.argv) > 1 else "news"
    print(f"--- Searching for: {search_term} ---")
    
    results = search_telegram_wide(search_term)
    
    if results:
        print(f"Found {len(results)} results:")
        for i, link in enumerate(results[:15], 1): # מציג עד 15 תוצאות
            print(f"{i}. {link}")
    else:
        print("No results found. Try a broader term.")
