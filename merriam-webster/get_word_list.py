import requests
import re

url = 'https://www.merriam-webster.com/browse/dictionary/'
for i in range(ord('c'), ord('z')+1):
    url_temp = url+chr(i)
    r = requests.get(url_temp).text
    n = int(re.findall('<span class="counters">page 1 of (\d*)</span>', r)[0])
    for j in range(n):
        f = open('m-w_word_list.txt', 'a', encoding='utf-8')
        url_temp_2 = url_temp + '/' + str(j+1)
        r = requests.get(url_temp_2).text
        w_l = re.findall('<a href="/dictionary/.*">(.*)</a>', r)
        for k in range(len(w_l)):
            f.write(w_l[k] + '\n')
        f.close()
