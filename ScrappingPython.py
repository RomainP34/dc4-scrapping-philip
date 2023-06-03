import requests
from bs4 import BeautifulSoup
import csv

hockeydesc = open('result.csv', 'w', newline='')

if hockeydesc == None:
    exit()

csvdesc = csv.writer(hockeydesc)
   
base = "https://www.scrapethissite.com/pages/forms/?page_num="

datascsv = []

header_trouve = False

for page in range(1,11):

    url = base + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")
    headers = table.find_all("th")

    if not header_trouve:
        
        i = 0
        headerline = []
        
        for header in headers:
            text = header.text
            headerline.append(text.strip())
            if "+ / -" in text :
                diff_indice = i

            if "Goals Against (GA)" in text:
                ga_indice = i

            i = i+1

        datascsv.append(headerline)
        header_trouve = True

    for line in table.find_all("tr"):
                     
        datas = line.find_all("td")
        if datas != None:
       
            linedata = []
            for d in datas:
                dclean = d.text.strip()
                linedata.append(dclean)
         
            if len(linedata) == 9:
                diff = int(linedata[diff_indice])
                ga = int(linedata[ga_indice])
                if diff > 0 and ga < 300:
                    datascsv.append(linedata)

csvdesc.writerows(datascsv)