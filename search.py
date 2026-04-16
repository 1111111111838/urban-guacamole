import requests
import sys
import re

def search_files_only(query):
    # חיפוש במנוע Lyzem
    url = f"https://lyzem.com/search?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # רג'קס שמוצא קישורי טלגרם שמסתיימים במספר הודעה (למשל t.me/channel/123)
        # הביטוי /\d+$ מבטיח שיש מספר בסוף הקישור
        links = re.findall(r't\.me\/[\w\d\-_]+\/\d+', response.text)
        
        clean_links = []
        for link in links:
            # הפיכת הקישור לפורמט תצוגה מקדימה ציבורי (/s/) כדי שיעבוד עם yt-dlp
            parts = link.split('/')
            # מבנה רצוי: https://t.me/s/channel_name/123
            formatted_link = f"https://t.me/s/{parts[1]}/{parts[2]}"
            
            if formatted_link not in clean_links:
                clean_links.append(formatted_link)
        
        return clean_links
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    search_query = sys.argv[1] if len(sys.argv) > 1 else "sample"
    print(f"--- מחפש קישורי קבצים עבור: {search_query} ---")
    
    results = search_files_only(search_query)
    
    if results:
        print(f"נמצאו {len(results)} הודעות עם קבצים פוטנציאליים:")
        for i, link in enumerate(results, 1):
            print(f"{i}. {link}")
    else:
        print("לא נמצאו הודעות ספציפיות. נסה מילת חיפוש אחרת או באנגלית.")
