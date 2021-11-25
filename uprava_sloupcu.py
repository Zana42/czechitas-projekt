
#nacte tabulku pametniku
import csv
seznam = []
with open('pametnici_polorucne - spojeno.tsv', 'r', encoding= 'utf-8') as pam:
  for row in csv.reader(pam, delimiter= "\t"):
    seznam += [row]
seznam = [s for s in seznam if len(s)]
print(seznam[:2])
#vytvori seznam jmen a ocisti je od data
jmena = [j[1] for j in seznam]
print(jmena)
cista_jmena = [i.strip("1234567890()- ") for i in jmena]
print(cista_jmena)

#rozdeli puvodni jmena na seznam podle ( a vybere pouze datum narozeni nebo nic, pokud chybi
jmena2 = [i.split("(") for i in jmena]

datum = [i[-1].strip("() ") for i in jmena2]

datum1 = [i.split('-') for i in datum]

birth = [i[0].strip() for i in datum1 ]


#pokus o vytvoreni data umrti, ktery nevysel
#death = [i[1] for i in datum1  if int(len(i)) == 2 ]
# for i in datum1:
#   if int(len(i)) == 2:
#     death = i[-1]
#   else:
#     death = "-"
# print(death)

#vytvori dekadu narozeni
decade = []
cislo2 = 0
for i in birth:
  if int(len(birth[cislo2])) == 4 :
    decade += [int(birth[cislo2]) // 10 * 10]
  else:
    decade += ['']
  cislo2 += 1

#rozodne pohlavi, jeslti se na zacatku short story objevi narodil ci narodila
short_story = [i[4] for i in seznam]
short_story_list = [s.split() for s in short_story]
short_story_list = [s[:12] for s in short_story_list]

gender = []
for i in short_story_list:
  if 'narodila' in i or 'Narodila' in i or 'rozená' in i or 'narozená' in i:
    gender += ['zena']
  elif 'narodil' in i or 'Narodil' in i:
    gender += ["muz"]
  else:
    gender += ["nevime"]

print(gender)

#vse vzpise zpet do seznamu
cislo = 0
seznam2 = seznam
for i in seznam2:
    if int(len(birth[cislo])) == 4:
      i[2] = birth[cislo]
    else:
      i[2]= ''
    i[1] = cista_jmena[cislo]
    i[3] = decade[cislo]
    i[10] = gender[cislo]
    cislo +=1

cislo = 0
with open('pametnici_polorucne - spojeno2.tsv', 'w', encoding= 'utf-8', newline='') as pam:

    # using csv.writer method from CSV package
    write = csv.writer(pam, delimiter= "\t")
      
    
    write.writerows(seznam2)



