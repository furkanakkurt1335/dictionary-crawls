from bs4 import BeautifulSoup
import requests


def del_br(s):
    k = ''
    is_in = False
    for i in range(len(s)):
        if is_in:
            if s[i] == '>':
                is_in = False
                k += ' '
            else:
                continue
        elif s[i] == '<':
            is_in = True
        elif s[i] != '\n':
            k += s[i]
    return k


f = open('extra entries.txt', 'r', encoding='utf-8')
s = f.read().split()
f.close()
f = open('extra meanings.txt', 'w', encoding='utf-8')
for i in range(len(s)):
    if '+' in s[i]:
        s[i] = s[i].replace('+', '%2B')
    url = 'https://nisanyansozluk.com/?k=' + s[i] + '&view=annotated'
    r = requests.get(url)
    r.encoding = 'utf-8'
    r = r.text
    try:
        r = r[r.index('hghlght')+180:]
    except:
        print(s[i])
        continue
    r = r[:r.index('maddepaylas')-12]
    r = del_br(r).strip().replace('\n', ' ').replace('  ', ' ')
    soup = BeautifulSoup(r, 'html.parser')
    f.write(s[i]+':\n')
    f.write(soup.prettify()+'\n\n')
f.close()
