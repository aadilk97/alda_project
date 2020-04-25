import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import xmltodict
import re
import xlsxwriter 
from links import arr
workbook = xlsxwriter.Workbook('rssNews.xlsx') 
worksheet = workbook.add_worksheet() 

def getArticle(url,row):
#    if url.startswith('\t'):
#        url=url[2:]
        
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    
    hval=soup.find('h1',attrs={"itemprop":"headline"})
    new_hval=re.sub('<[^>]*>', '', str(hval))
    worksheet.write(row, 0, new_hval)
#     print('Headline: '+new_hval)
    
    aval=soup.find(attrs={"itemprop":"author"})
    new_aval=re.sub('<[^>]*>', '', str(aval))
    worksheet.write(row, 1, new_aval)
#     print('Author: '+new_aval)

    dval=soup.find('time')
    new_dval=re.sub('<[^>]*>', '', str(dval))
    worksheet.write(row, 2, new_dval)
#     print('Published on: '+new_dval)

    data=soup.find("section", attrs={"name":"articleBody"})
    if data!=None:
        new_data=(data.find_all('p'))
        arr=[]
        for a in new_data:
            arr.append(re.sub('<[^>]*>', '', str(a)))
        worksheet.write(row, 3, ''.join(arr))
#         print("Article: \n"+''.join(arr))
        main_article.append(''.join(arr))

row=0

for a in arr:
    r=requests.get(a)
    soup = BeautifulSoup(r.text, "html.parser")
    jsonString = json.dumps(xmltodict.parse(r.text), indent=1)
    data = json.loads(jsonString)
    items=data['rss']['channel']['item']
    links=[]
    for i in items:
        if '.html' in i['link']:
            getArticle(i['link'],row)
            row+=1
    break        
    
workbook.close()    
                        