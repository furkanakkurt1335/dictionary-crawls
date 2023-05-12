import re
import requests

alphabet = []
alp_temp = [ord('a'), ord('z'), ord('A'), ord('Z')]
for i in range(alp_temp[0], alp_temp[1]+1):
    alphabet.append(chr(i))
for i in range(alp_temp[2], alp_temp[3]+1):
    alphabet.append(chr(i))

# url = 'https://tr.wiktionary.org/wiki/Kategori:T%C3%BCrk%C3%A7e_s%C3%B6zc%C3%BCkler'
# url = 'https://en.wiktionary.org/wiki/Category:English_lemmas'
url = 'https://en.wiktionary.org/w/index.php?title=Category:English_lemmas&pagefrom=♥'
f = open('all-wordssfgfdg-en.txt', 'a', encoding='utf-8')
while True:
    r = requests.get(url)
    s = r.text
    si1 = s.index('are in this category')
    si2 = s.index('printfooter')
    s = s[si1:si2]
    l = re.findall('<li><a href=.*title=.*>(.*)</a></li>', s)
    for j in range(len(l)):
        f.write(l[j] + '\n')
    # if 'züyuf' in l:
    #     break
    # url = 'https://tr.wiktionary.org/w/index.php?title=Kategori:T%C3%BCrk%C3%A7e_s%C3%B6zc%C3%BCkler&pagefrom=' + \
    #     l[-1]
    last = l[-1]
    for j in range(2, 50):
        if last[0] not in alphabet:
            last = l[-j]
        else:
            break
    url = 'https://en.wiktionary.org/w/index.php?title=Category:English_lemmas&pagefrom=' + \
        last
f.close()
