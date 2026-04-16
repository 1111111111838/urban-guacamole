import requests
from bs4 import BeautifulSoup
import sys
import urllib.parse

def search_in_telegram_directory(query):
    # הגדרת כתובת החיפוש - מחפש רק בדפי תצוגה מקדימה ציבוריים של טלגרם
    search_url = f"https://www.google.com/search?q=site:t.me/s/+{query}"
    
    # הגדרת User-Agent כדי שגוגל יזהה אותנו כדפדפן רגיל
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status() # בדיקה שהבקשה עברה בהצלחה
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        # סריקת כל הקישורים בדף התוצאות
        for a in soup.find_all('a', href=True):
            href = a['href']
            
            # ניקוי הקישור מהמבנה של גוגל
            if '/url?q=' in href:
                # חילוץ ה-URL האמיתי מתוך הפרמטר q
                actual_url = href.split('/url?q=')[1].split('&')[0]
                # פענוח תווים מיוחדים (כמו %3A שהופך ל-:)
                clean_url = urllib.parse.unquote(actual_url)
                
                # שמירה רק אם זה קישור לתצוגה מקדימה של טלגרם
                if 't.me/s/' in clean_url and not 'google.com' in clean_url:
                    if clean_url not in links:
                        links.append(clean_url)
        
        return links
    except Exception as e:
        print(f"שגיאה במהלך החיפוש: {e}")
        return []

if __name__ == "__main__":
    # קבלת מילת החיפוש מהמשתמש (דרך GitHub Action)
    if len(sys.argv) > 1:
        search_query = sys.argv[1]
    else:
        search_query = "חינוך והעשרה" # ברירת מחדל
        
    print(f"--- מחפש קישורים עבור: {search_query} ---")
    
    found_links = search_in_telegram_directory(search_query)
    
    if found_links:
        print(f"נמצאו {len(found_links)} תוצאות:")
        for i, link in enumerate(found_links, 1):
            print(f"{i}. {link}")
    else:
        print("לא נמצאו קישורים תקינים. נסה לשנות את מילת החיפוש.")
