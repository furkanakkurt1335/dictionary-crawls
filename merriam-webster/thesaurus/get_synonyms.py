import requests, json, re, argparse
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from pathlib import Path

base_url = 'https://www.merriam-webster.com'
base_url_parsed = urlparse(base_url)

def get_args():
    parser = argparse.ArgumentParser(description='Get synonyms from Merriam-Webster thesaurus')
    parser.add_argument('-e', '--entries', help='Path to the entries file', default='entries.json')
    return parser.parse_args()

def get_soup(entry):
    url = base_url_parsed._replace(path=base_url_parsed.path + entry).geturl()
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    return soup

def main():
    args = get_args()
    entries_path = Path(args.entries)
    with entries_path.open() as f:
        entries = json.load(f)
    dir = entries_path.parent

    out_file = dir / 'data.json'

    if out_file.exists():
        with out_file.open() as f:
            synonym_d = json.load(f)
    else:
        synonym_d = {entry['word']: [] for entry in entries}
    color_pattern = re.compile(r'color-(\d)')
    for i, entry in enumerate(entries):
        word = entry['word']
        if word in synonym_d and synonym_d[word]:
            continue
        soup = get_soup(entry['link'])
        # thesaurus-entry-container
        thesaurus_entry_containers = soup.find_all('div', class_='thesaurus-entry-container')
        for thesaurus_entry_container in thesaurus_entry_containers:
            # parts-of-speech
            parts_of_speech = thesaurus_entry_container.find('h2', class_='parts-of-speech')
            parts_of_speech_text = None
            if parts_of_speech:
                parts_of_speech_text = parts_of_speech.text.strip()
            items = thesaurus_entry_container.find_all('div', class_='vg-sseq-entry-item')
            for item in items:
                # as-in-word
                as_in_word = item.find('div', class_='as-in-word')
                as_in_word_text = None
                if as_in_word:
                    as_in_word_text = as_in_word.find('em').text
                # definition
                definition = item.find('span', class_='dt')
                definition_text = None
                ex_sent_text = None
                if definition:
                    # ex-sent
                    ex_sent = definition.find('span', class_='ex-sent')
                    if ex_sent:
                        ex_sent_text = ex_sent.text.strip()
                        ex_sent.decompose()
                    definition_text = definition.text.strip()
                # thes-list
                synonym_lists = item.find_all('span', class_='thes-list')
                related_words = {relation: {str(color): [] for color in range(1, 5)} for relation in ['synonyms', 'antonyms']}
                if synonym_lists:
                    for synonym_list in synonym_lists:
                        # opp-list-scored
                        synonym_list_attr = synonym_list['class']
                        if 'opp-list-scored' in synonym_list_attr:
                            relation = 'antonyms'
                        else:
                            relation = 'synonyms'
                        # thes-list-content
                        thes_list_content = synonym_list.find('div', class_='thes-list-content')
                        if thes_list_content:
                            # thes-word-list-item
                            thes_word_list_items = thes_list_content.find_all('li', class_='thes-word-list-item')
                            for thes_word_list_item in thes_word_list_items:
                                # lozenge
                                lozenge = thes_word_list_item.find('span', class_='lozenge')
                                if lozenge:
                                    # get color
                                    lozenge_attr = lozenge['class']
                                    color = None
                                    for attr in lozenge_attr:
                                        if 'color' in attr:
                                            color = color_pattern.search(attr).group(1)
                                # syl
                                syl = thes_word_list_item.find('span', class_='syl')
                                syl_text = None
                                if syl:
                                    syl_text = syl.text
                                related_words[relation][color].append(syl_text)
                synonym_d[word].append({'as in': as_in_word_text, 'definition': definition_text, 'example': ex_sent_text, 'related words': related_words, 'POS': parts_of_speech_text})
        if i % 50 == 0:
            with out_file.open('w', encoding='utf-8') as f:
                json.dump(synonym_d, f, indent=4, ensure_ascii=False)
    with out_file.open('w', encoding='utf-8') as f:
        json.dump(synonym_d, f)

if __name__ == '__main__':
    main()