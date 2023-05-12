# dictionary.com crawl
import requests
import re

f = open('all_entries.txt', 'a', encoding='utf-8')
url = 'https://www.dictionary.com/list/'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
for i in range(ord('a'), ord('z')+1):
    url_temp = url + chr(i) + '/'
    r = requests.get(url_temp, headers=headers)
    r.encoding = 'utf-8'
    r = r.text
    letter_length = re.findall(
        '<li class="css-3w1ibo e1wvt9ur0"><. data-page=".*" href="/list/./(.*?)">', r)
    for j in range(int(letter_length[0])):
        r_temp = requests.get(url_temp + str(j+1), headers=headers)
        r_temp.encoding = 'utf-8'
        r_temp = r_temp.text
        w_l = re.findall(
            '<li><a href="https://www.dictionary.com/browse/.*?" class="css-aw8l3w e3scdxh3">(.*?)</a>', r_temp)
        for k in range(len(w_l)):
            f.write(w_l[k]+'\n')
    f.close()
    f = open('all_entries.txt', 'a', encoding='utf-8')
f.close()
