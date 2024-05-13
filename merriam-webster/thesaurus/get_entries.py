import requests, json, re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from pathlib import Path

base_url = 'https://www.merriam-webster.com/browse/thesaurus'
base_url_parsed = urlparse(base_url)

def get_soup(letter, page):
    url = base_url_parsed._replace(path=base_url_parsed.path + '/' + letter + '/' + str(page)).geturl()
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    return soup

def get_entries(soup):
    entries = []
    table = soup.find('div', class_='mw-grid-table-list')
    if table:
        rows = table.find_all('li', class_='col-6 col-lg-4')
        for row in rows:
            a_t = row.find('a')
            link = a_t['href']
            word = a_t.text
            entries.append({'link': link, 'word': word})
    return entries

page_count_pattern = re.compile(r'page 1 of (\d+)')

def get_page_count(first_soup):
    counters_span = first_soup.find('span', class_='counters')
    if counters_span:
        count_match = page_count_pattern.search(counters_span.text)
        if count_match:
            page_count = int(count_match.group(1))
            return page_count
    return 1

def main():
    entries_path = Path('entries.json')

    letters = [chr(i) for i in range(97, 123)] + ['0']
    entries = []
    for letter in letters:
        soup = get_soup(letter, 1)
        entries += get_entries(soup)
        page_count = get_page_count(soup)
        for page in range(2, page_count + 1):
            soup = get_soup(letter, page)
            entries += get_entries(soup)

        with entries_path.open('w') as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
        
        print(f'Found {len(entries)} entries, current letter: {letter}')

    with entries_path.open('w') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    print(f'Found {len(entries)} entries')

if __name__ == '__main__':
    main()