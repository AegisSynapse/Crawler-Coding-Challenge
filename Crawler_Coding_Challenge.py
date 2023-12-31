import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

def get_common_words(Webpage, section, num_words=10, exclude_words=None, timeout=8):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    
    try:
        response = requests.get(Webpage, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Unable to Navigate to Webpage. Error: {e}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    header = soup.find('span', {'class': 'mw-headline'}, string=section)
    if not header:
        print('Section not found')
        return []
    
    text_content = []
    for sibling in header.find_parent().find_next_siblings():
        if sibling.name == 'h2':
            break  
        text_content.append(sibling.get_text())
    
    text = ' '.join(text_content)
    words = re.findall(r'\b[a-zA-Z_]\w*\b', text.lower())
    
    if exclude_words:
        words = [word for word in words if word not in exclude_words]
    
    counter = Counter(words)
    return counter.most_common(num_words)

Webpage = "https://en.wikipedia.org/wiki/Microsoft"
section = "History"
exclude_words = {"Company", "New", "that", "brand", "Knew", "any", "isn't", "without", "form", "only"}
most_common_words = get_common_words(Webpage, section, num_words=10, exclude_words=exclude_words)

if most_common_words:
    print("\nCrawler Coding Challenge (excluding some common words):")
    for i, (word, freq) in enumerate(most_common_words, start=1):
        print(f"{i}. {word.capitalize()}: {freq} times")
else:
    print("\nNothing Found")