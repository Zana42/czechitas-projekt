#projde potrebne slozky a soubory exportu PN a udela pro kazdeho pametnika csv soubor s danymi sloupci
import re
import json
import glob
from unidecode import unidecode
import csv

#nacte do seznamu 'clip_seznam' vsechny clipy
clip_foldernames = [i for i in glob.glob(f"export-uni-clip\\*")]
clip_filenames = []
for i in clip_foldernames:
  clip_filenames += glob.glob(f"{i}\cs.json")

clip_seznam = []
cislo = 0
for n in range(len(clip_filenames) - 1):
  with open(clip_filenames[cislo], 'r', encoding= 'utf-8') as clip:
      clip_vstup = [i for i in clip]

#vycisti od prazdnych slovniku a od protokolu nahravek
  if len(json.loads(clip_vstup[0])['field_transcript']) > 0 and len(json.loads(clip_vstup[0])['field_witness']) > 0 and 'PROTOKOL' not in json.loads(clip_vstup[0])['field_transcript'][0]['value']:
    clip_vstup1 = json.loads(clip_vstup[0])
    clip_seznam += [clip_vstup1]
  cislo += 1



#nacte seznam nazvu vsech souboru 'recording'
all_foldernames = [i for i in glob.glob(f"export-uni-recording\\*")]
all_filenames = []
for i in all_foldernames:
  all_filenames += glob.glob(f"{i}\cs.json")



#nacte pribeh pametnika jako full_story
for n in range(len(all_filenames) -1):
  with open(all_filenames[n], 'r', encoding= 'utf-8') as pribeh:
    vstup = [i for i in pribeh]
  vstup1 = json.loads(vstup[0])


#vzbere pouze ty pribehy, ktere obsahuji pribeh
  if len(vstup1['field_description']) > 0:
    full_story1 = vstup1['field_description'][0]['value'].strip()
    #vycisti od html znacek, tady by se jiste hodilo uyit regex
    

    full_story1

    #cistic zbavi html znacek
    clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
  
    
    full_story3 = re.sub(clean, '', full_story1)
 

    #pokus prochroustat text a vzbrat pouze tisknutelne znaky, pokus vysel dbore
    full_story4 = []
    for f in full_story3:
      if f.isprintable():
        full_story4 += f
      else:
        full_story4 += ' '
    full_story = ''.join(full_story4).strip()

#vybere pouze ty pribehy, ktere maji id pametnika
    if len(vstup1['field_witness']) > 0:
      witness_id = vstup1['field_witness'][0]['target_id']
      witness_foldernames = [i for i in glob.glob(f"export-uni-witness\\{witness_id}")]


      #vyfiltruje witness pouze psane cesky s priponou cs.json
      witness_filenames1 = []
      for i in witness_foldernames:
        witness_filenames1 += glob.glob(f"{i}\*.json")

      witness_filename = []
      for i in witness_filenames1:
        if 'cs.json' in i:
          witness_filename = i 
        if len(witness_filename) > 0:


        #nacte soubor pametnika
          with open(witness_filename, 'r', encoding= 'utf-8') as pametnik:
            pametnik = [i for i in pametnik]
          pametnik1 = json.loads(pametnik[0])

          #vytvori jmeno pametnika, sluselo by se casem priradit i tituly, ty jsou pres ciselnik
          if len(pametnik1['field_first_name']) > 0:
            first_name = pametnik1['field_first_name'][0]['value']
          last_name = pametnik1['field_last_name'][0]['value']
          witness_name = f"{first_name} {last_name}"

          #napise rok narozeni, kdyz chzbi, tak prazdne misto
          if len(pametnik1['field_birth_year']) > 0:
            year_of_birth = pametnik1['field_birth_year'][0]['value']
          else:
            year_of_birth = ''

          #vypocita dekadu narozeni
          if int(len(year_of_birth)) == 4 :
            decade_of_birth = int(year_of_birth) // 10 * 10
          else:
            decade_of_birth = ''

          #nacte short_story
          if len(pametnik1['field_biography']) > 0:
            short_story1 = re.sub(clean, '', pametnik1['field_biography'][0]['value'].replace('&nbsp;', ' '))
          else:
            short_story1 = ''

          #odstrani netisknutelne znaky
          short_story3 = []
          for f in short_story1:
            if f.isprintable():
              short_story3 += f
            else:
              short_story3 += ' '
          short_story = ''.join(short_story3).strip()


          #vytvori url pametnika, chtelo by ji to overit se seznamem skutecne pouzitych url, ten se da stahnout z webu
          url_first_name = unidecode(first_name.strip('').replace(' ','-').replace('(','').replace(')','').replace('.','').replace(',','').lower())
          url_last_name = unidecode(last_name.strip('().,').replace(' ','-').replace('(','').replace(')','').replace('.','').replace(',','').lower())
          url = f"https://www.pametnaroda.cz/cs/{url_last_name}-{url_first_name}-{year_of_birth}".replace('--', '-').replace('---', '-')
          
        
          #vygeneruje gender, mozna bz asi byla i nejaka cesta pres tvar jmena
          gender = []
          if 'narodila' in short_story or 'Narodila' in short_story or 'rozená' in short_story or 'narozená' in short_story:
            gender += ['zena']
          elif 'narodil' in short_story or 'Narodil' in short_story:
            gender += ['muz']
          else:
            gender += ['nevime']

          #projde clip_seznam a pokud ma id pametnika, priradi ho do citace_string
          citace = ['']
          for i in clip_seznam:
            if  i['field_witness'][0]['target_id'] == witness_id:
              citace += [i['field_transcript'][0]['value'].strip()]
          #ocisti od html znacek
          citace_string1 = re.sub(clean, '', ' '.join(citace))
          #ocisti od netisknutelnych znaku
          citace_string2 = []
          for f in citace_string1:
            if f.isprintable():
              citace_string2 += f
            else:
              citace_string2 += ''
          citace_string = ''.join(citace_string2).strip()

          #tady by se daly pridat tagy, ktere si vede pamet naroda
          anniversary_tag = '-'
          tag = '-'
          

          #vypise potrebne do souboru csv
          novy_soubor = f"{first_name}_{last_name}_{year_of_birth}.csv"
          with open( novy_soubor , 'w', encoding = 'utf-8') as pametnik:
            writer = csv.writer(pametnik, delimiter=',')
            writer.writerow([witness_id, f"{first_name} {last_name}", year_of_birth, decade_of_birth, short_story, full_story, citace_string, anniversary_tag, tag, url, gender[0]])


