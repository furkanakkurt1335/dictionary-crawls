import json, argparse
from pathlib import Path

def get_args():
    parser = argparse.ArgumentParser(description='Get synonyms from Merriam-Webster thesaurus')
    parser.add_argument('-i', '--input', help='Path to the input file', type=Path, required=True)
    return parser.parse_args()

def main():
    args = get_args()
    input_file = args.input
    with input_file.open() as f:
        data = json.load(f)

    for word in data:
        for entry in data[word]:
            if entry['POS'] == 'adjective':
                syns = entry['related words']['synonyms']
                for degree in syns:
                    for syn in syns[degree]:
                        found = False
                        for entry2 in data[syn]:
                            if entry2['POS'] == 'adjective':
                                for degree2 in entry2['related words']['synonyms']:
                                    if word in entry2['related words']['synonyms'][degree2]:
                                        found = True
                                        break
                        if not found:
                            print(f"{word} {degree} {syn}")
                            input()

if __name__ == '__main__':
    main()

'''
    With this script, it can be seen that the synonymity degrees between words are not symmetric.

    An example is 'A1' and 'radical'. 'A1' has 'radical' as a synonym in degree 2, while 'radical' has 'A1' as a synonym in degree 3.

    Another example is 'A1' and 'OK'. While 'A1' has 'OK' as a synonym in degree 2, 'OK' doesn't have 'A1' as a synonym at all.
'''