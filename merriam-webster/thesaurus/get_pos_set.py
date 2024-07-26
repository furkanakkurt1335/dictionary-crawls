import json, argparse, re
from pathlib import Path

def get_args():
    parser = argparse.ArgumentParser(description='Get synonyms from Merriam-Webster thesaurus')
    parser.add_argument('-i', '--input', help='Path to the input file', required=True)
    return parser.parse_args()

def main():
    number_pattern = re.compile(r'(^.*?) \(\d+\)$')
    args = get_args()
    input_file = Path(args.input)
    with input_file.open() as f:
        data = json.load(f)
    pos_set = set()
    for senses in data.values():
        for sense in senses:
            pos = sense['POS']
            pos = number_pattern.sub(r'\1', pos)
            pos_set.add(pos)
    print(pos_set)

if __name__ == '__main__':
    main()

'''
POS set:
{'noun', 'phrase', 'conjunction', 'preposition', 'adjective', 'pronoun', 'adverb', 'verb', 'interjection', 'plural noun'}
'''