import csv
import os
from tqdm import tqdm
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime as dt
import math

def add_watermark(image_path, watermark_text):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((10, 10), watermark_text, fill=(0, 0, 0), font=font)
    image.save(image_path)


#retrieving data from files
path_list = __file__.split("/")
path_list=path_list[0:-3]
path_list.append("DataProvided")
file_path = "/".join(path_list)

file_names = os.listdir(file_path)

csv_read = []
#converting csv to JSON
with open(os.path.join(file_path,file_names[0]),'r') as file:
    csv_read_init = csv.DictReader(file)
    for row in tqdm (csv_read_init, desc="Reading file data 2017-2018..."):
        csv_read.append(row)

with open(os.path.join(file_path,file_names[1]),'r') as file:
    csv_read_init = csv.DictReader(file)
    for row in tqdm (csv_read_init, desc="Reading file data 2019..."):
        csv_read.append(row)


#--------------------TARGET--------------------#
custSeg_targetDict = {}
totOrd = 0
ordCnt = {}
for row in tqdm (csv_read, desc="Working on prod cat data..."):
    if(row['Order Number'] not in ordCnt):
        ordCnt[row['Order Number']] = 1
        totOrd += 1
        if(row['Customer Segment'] not in custSeg_targetDict):
            custSeg_targetDict[row['Customer Segment']] = {row['Product Category']: 1}
        else:
            if(row['Product Category'] not in custSeg_targetDict[row['Customer Segment']]):
                custSeg_targetDict[row['Customer Segment']].update({row['Product Category']: 1})
            else:
                custSeg_targetDict[row['Customer Segment']][row['Product Category']] += 1

for custSed in custSeg_targetDict:
    custSeg_targetDict[custSed] = dict(sorted(custSeg_targetDict[custSed].items(), key=lambda item: item[1],reverse=True)[0:10])
    
    prodNam = list(custSeg_targetDict[custSed].keys())
    prodVal = list(custSeg_targetDict[custSed].values())
    for p in range(len(prodNam)):
        prodNam[p]="Prod Cat "+prodNam[p][-1]

    plt.figure(figsize=(8,6))

    plt.bar(prodNam,prodVal,color='lightskyblue')
    plt.xlabel("Product Category")
    plt.ylabel("Numbers")
    plt.title("Product Category targeted by "+custSed)
    plt.xticks(rotation=15, ha='right')
    plt.savefig(custSed+'_productCategoryTarget.png')
    add_watermark(custSed+'_productCategoryTarget.png', "made by rpd")
#----------------------------------------------#

#-----------------------------MONTH-WISE-----------------------------#
custSeg_targetDict = {}

for row in tqdm (csv_read, desc="Working on month data..."):
    dateData = row['Invoice Date']
    rev = float(row['Revenue'])
    mnth = str(dt.strptime(dateData,"%d-%m-%Y %H:%M").month)
    if(row['Customer Segment'] not in custSeg_targetDict):
        custSeg_targetDict[row['Customer Segment']] = {mnth: rev}
    else:
        if(mnth not in custSeg_targetDict[row['Customer Segment']]):
            custSeg_targetDict[row['Customer Segment']].update({mnth: rev})
        else:
            custSeg_targetDict[row['Customer Segment']][mnth] += rev

for custSed in custSeg_targetDict:
    custSeg_targetDict[custSed] = dict(sorted(custSeg_targetDict[custSed].items(), key=lambda item: int(item[0])))
    
    prodNam = list(custSeg_targetDict[custSed].keys())
    prodVal = list(custSeg_targetDict[custSed].values())
    for p in range(12):
        prodNam[p] = dt.strptime(str(prodNam[p]), "%m").strftime("%b")
    #strftime("%b")
    plt.figure(figsize=(7,6))

    plt.plot(prodNam,prodVal,color='tomato')
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.title("Month wise data on "+custSed)
    #plt.xticks(rotation=15, ha='right')
    plt.savefig(custSed+'_monthWiseData.png')
    add_watermark(custSed+'_monthWiseData.png', "made by rpd")
#--------------------------------------------------------------------#
    
