#vytvori seznam url vsech pametniku a vzpise do souboru
from requests_html import HTMLSession
session = HTMLSession()
import time

#projedeme abecedou, udela seznam url, kde na kazde je asi 10 odkazu na url pametniku
url_alph = "https://www.pametnaroda.cz/cs/witnesses-alphabetic/"
pismenka = ["a", "á", "b", "c", "č", "d", "ď", "e", "f", "g", "h", "i", "j", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "r", "ř", "s", "š", "t", "ť", "u", "ú", "v", "w", "x", "y", "z", "ž"]
url1 = [url_alph + pismenko for pismenko in pismenka]

url_ready = url1
index1 = 0

for i in range(len(pismenka) -1):
#projede vse
#for url in url1:
  stranka = session.get(url1[index1])
  pages = stranka.html.find('.pager-heading__pages')
  pocet_stranek = int(pages[0].text.split("/")[1].strip())

  index = 1
  for n in range(pocet_stranek - 1):
    if pocet_stranek > 1:
      url_ready += [url1[index1] + "?page=" + str(index)]
      index += 1
      time.sleep(1)
  index1 += 1

#udela seznam url vsech pametniku
odkazy_alph = []
index2 = 0
for url in url_ready:
  stranka = session.get(url_ready[index2])
  odkazy = stranka.html.find(' .pnb-witness-l__bio a')
  for p in odkazy:
    odkazy_alph += [p.attrs['href']]
  index2 += 1



#vypise do souboru
with open('odkazy_alph.txt', 'w', encoding= 'utf-8') as vystup:
  for i in odkazy_alph:
    vystup.write('https://www.pametnaroda.cz' + i + '\t')



