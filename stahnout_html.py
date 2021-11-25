from requests_html import HTMLSession
session = HTMLSession()
import sys

#prijme html z prikaaove radky
vstup_odkaz = sys.argv[1]

#nacte stranku pametnika
stranka = session.get(vstup_odkaz)
pametnik = []
for odstavec in stranka.html.find('p'):
  pametnik += [odstavec.text]

#vybere short story a citace, hezci by bylo pouzit typy znaceka a ne misto v seznamu.
short_story = pametnik[-11]
citace = ','.join(pametnik[:-12])

#vybere jmeno a datum
for nadpis in stranka.html.find('title'):
  nadpis = (nadpis.text)

#vybere odkaz na full story
odkaz = stranka.html.find(' .sres-showall a')
odkaz2 = [p.attrs['href'] for p in odkaz]

#nacte full story
dalsi_stranka = session.get('https://www.pametnaroda.cz' + odkaz2[0])

full_story1 = []
for odstavec in dalsi_stranka.html.find(' p'):
  full_story1 += [odstavec.text]

full_story2 = full_story1[1:]
full_story = ','.join(full_story2[:-2])

#nacte tag a anniversary_tag
tag = []
for t in stranka.html.find('a[class="tag__link"]'):
  tag += [t.text]
tag = ','.join(tag)

anniversary_tag = []
for at in stranka.html.find('a[class="anniversary__link"]'):
  anniversary_tag += [at.text]
anniversary_tag = ','.join(anniversary_tag)


#import csv

#vytvori jmeno souboru
novy_soubor = f"{vstup_odkaz.strip('https://www.pametnaroda.cz/cs/')}.tsv"

#vypise potrebne do souboru, kdzy jsem pouzila csv modul, psalo to necozvlastniho, ve finalni verzi je to uz res csv
with open(novy_soubor, 'w', encoding = 'utf-8') as r:
  r.write(nadpis)
  r.write('\t')
  r.write(short_story)
  r.write('\t')
  r.write(full_story) 
  r.write('\t')
  r.write(citace)
  r.write('\t')
  r.write(anniversary_tag)
  r.write('\t')
  r.write(tag)
  r.write('\t')
  r.write(vstup_odkaz)
