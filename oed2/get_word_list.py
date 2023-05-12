import requests
import re

url = 'https://www.oed.com/oed2/'
f = open('oed2_word_list.txt', 'r', encoding='utf-8')
s = len(f.read().split('\n'))
f.close()
f = open('oed2_word_list.txt', 'a', encoding='utf-8')
for i in range(s, 291602):
    r = requests.get(url + str(i))
    r.encoding = 'utf-8'
    r = r.text[300:700]
    w = re.findall('<div class="hwLabel">(.*?)</div>', r)
    f.write(w[0] + '\n')
    if i % 1000 == 0:
        f.close()
        f = open('oed2_word_list.txt', 'a', encoding='utf-8')
f.close()
