# collins crawl
import requests
import re

f = open('all_entries.txt', 'a', encoding='utf-8')
url = 'https://www.collinsdictionary.com/us/browse/english/words-starting-with-'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
for i in range(ord('b'), ord('z')+1):
    url_temp = url + chr(i)
    r = requests.get(url_temp, headers=headers)
    r.encoding = 'utf-8'
    r = r.text
    url_l = re.findall(
        '<li><a href="(https:\/\/www\.collinsdictionary\.com\/us\/browse\/english.*)" title=".*" tooltip=".*">.* \.\.\. .*<\/a>', r)
    for j in range(len(url_l)):
        r_temp = requests.get(url_l[j], headers=headers)
        r_temp.encoding = 'utf-8'
        r_temp = r_temp.text
        w_l = re.findall(
            '<li><a href="https://www.collinsdictionary.com/us/dictionary/english/.*" title=".*" tooltip=".*">(.*)</a>', r_temp)
        for k in range(len(w_l)):
            f.write(w_l[k]+'\n')
    f.close()
    f = open('all_entries.txt', 'a', encoding='utf-8')
f.close()
