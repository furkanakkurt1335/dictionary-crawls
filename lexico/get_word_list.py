import requests
import re
from time import sleep

url = 'https://www.lexico.com/en/list/'
for i in range(ord('a'), ord('z')+1):
    url_temp = url+chr(i)
    r = requests.get(url_temp).text
    n = int(re.findall('<a href="/en/list/./(\d*)">Last', r)[0])
    for j in range(n):
        f = open('lexico_word_list.txt', 'a', encoding='utf-8')
        url_temp_2 = url_temp + '/' + str(j+1)
        r = requests.get(url_temp_2).text
        w_l = re.findall(
            '<li><a href="\/en\/definition\/.+?">(.*?)<\/a><\/li>', r)
        for k in range(len(w_l)):
            f.write(w_l[k] + '\n')
        f.close()
    sleep(30)
# url_temp = url+'s'
# r = requests.get(url_temp).text
# n = int(re.findall('<a href="/en/list/./(\d*)">Last', r)[0])
# for j in range(73, n):
#     f = open('lexico_word_list.txt', 'a', encoding='utf-8')
#     url_temp_2 = url_temp + '/' + str(j+1)
#     r = requests.get(url_temp_2).text
#     w_l = re.findall(
#         '<li><a href="\/en\/definition\/.+?">(.*?)<\/a><\/li>', r)
#     for k in range(len(w_l)):
#         f.write(w_l[k] + '\n')
#     f.close()
