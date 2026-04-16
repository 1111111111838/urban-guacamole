import requests
import sys

def search_lyzem(query):
    # שימוש בכתובת החיפוש של Lyzem שמחזירה תוצאות מערוצים ציבוריים
    # אנחנו נבצע חיפוש ונסנן את הכתובות של הטלגרם
    url = f"https://lyzem.com/search?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # אנחנו מחפשים קישורים שמתחילים ב-t.me בתוך ה-HTML
        import re
        # מוצא את כל הקישורים לערוצים או הודעות
        links = re.findall(r't\.me\/[\w\d\-_/]+', response.text)
        
        clean_links = []
        for link in links:
            # מוודא שזה פורמט של תצוגה מקדימה (מוסיף /s/ אם חסר)
            if '/s/' not in link:
                parts = link.split('/')
                if len(parts) > 1:
                    link = f"{parts[0]}/s/{'/'.join(parts[1:])}"
            
            full_link = "https://" + link
            if full_link not in clean_links:
                clean_links.append(full_link)
        
        return clean_links
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "sample"
    print(f"--- מחפש במאגר טלגרם עבור: {query} ---")
    
    results = search_lyzem(query)
    
    if results:
        print(f"נמצאו {len(results)} תוצאות פוטנציאליות:")
        # מציג רק את ה-10 הראשונות כדי לא להעמיס
        for i, link in enumerate(results[:10], 1):
            print(f"{i}. {link}")
    else:
        print("לא נמצאו תוצאות. נסה מילת חיפוש אחרת (למשל 'nature' או 'tech').")
