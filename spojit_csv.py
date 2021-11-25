import glob

#nacte do seznamu nazvy csv souboru
file_extension = '.csv'
all_filenames = [i for i in glob.glob(f"*{file_extension}")]

#vypise vse do noveho souboru
cislo = 0

with open('spojeno_ready.csv', 'w', encoding='utf-8', newline = '') as file:
  for i in range(len(all_filenames)):
    with open(all_filenames[cislo], 'r', encoding= 'utf=8', newline = '') as pametnik:
      row = [p for p in pametnik]
      file.write(row[0])

    cislo += 1

