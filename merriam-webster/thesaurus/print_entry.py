import json, argparse
from pathlib import Path

def get_args():
    parser = argparse.ArgumentParser(description='Get synonyms from Merriam-Webster thesaurus')
    parser.add_argument('-i', '--input', help='Path to the input file', required=True)
    parser.add_argument('-e', '--entry', required=True)
    return parser.parse_args()

def main():
    args = get_args()
    input_file = Path(args.input)
    with input_file.open() as f:
        data = json.load(f)
    print(json.dumps(data[args.entry], indent=4))

if __name__ == '__main__':
    main()