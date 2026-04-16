import requests
from bs4 import BeautifulSoup
import sys

def search_in_telegram_directory(query):
    # חיפוש דרך גוגל על דפי התצוגה המקדימה של טלגרם
    search_url = f"https://www.google.com/search?q=site:t.me/s/+{query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            # סינון קישורים שמובילים לטלגרם
            if 't.me/s/' in href and not 'google.com' in href:
                # ניקוי הקישור
                clean_link = href.replace('/url?q=', '').split('&')[0]
                if clean_link not in links:
                    links.append(clean_link)
        return links
    except Exception as e:
        print(f"Error: {e}")
        return []

# שינוי קטן: הסקריפט יקבל את מילת החיפוש מהפקודה שנריץ
if __name__ == "__main__":
    search_query = sys.argv[1] if len(sys.argv) > 1 else "סרט דוגמה"
    print(f"--- מחפש קישורים עבור: {search_query} ---")
    results = search_in_telegram_directory(search_query)
    
    if not results:
        print("לא נמצאו קישורים. נסה מילת חיפוש אחרת.")
    for link in results:
        print(f"נמצא קישור פוטנציאלי: {link}")
