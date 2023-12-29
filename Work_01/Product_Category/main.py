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


#-----------------------------MONTH-WISE-----------------------------#
        """
custSeg_targetDict = {}

for row in tqdm (csv_read, desc="Working on month data..."):
    dateData = row['Invoice Date']
    rev = float(row['Revenue'])-float(row['Cost'])
    mnth = str(dt.strptime(dateData,"%d-%m-%Y %H:%M").month)
    if(row['Product Category'] not in custSeg_targetDict):
        custSeg_targetDict[row['Product Category']] = {mnth: rev}
    else:
        if(mnth not in custSeg_targetDict[row['Product Category']]):
            custSeg_targetDict[row['Product Category']].update({mnth: rev})
        else:
            custSeg_targetDict[row['Product Category']][mnth] += rev

for custSed in custSeg_targetDict:
    custSeg_targetDict[custSed] = dict(sorted(custSeg_targetDict[custSed].items(), key=lambda item: int(item[0])))
    
    prodNam = list(custSeg_targetDict[custSed].keys())
    prodVal = list(custSeg_targetDict[custSed].values())
    for p in range(12):
        prodNam[p] = dt.strptime(str(prodNam[p]), "%m").strftime("%b")
    #strftime("%b")
    plt.figure(figsize=(7,6))

    plt.plot(prodNam,prodVal,color='yellowgreen')
    plt.xlabel("Month")
    plt.ylabel("Net Revenue Generated")
    plt.title("Month wise data on "+custSed)
    #plt.xticks(rotation=15, ha='right')
    plt.savefig(custSed+'_monthWiseData.png')
    add_watermark(custSed+'_monthWiseData.png', "made by rpd")
    """
#--------------------------------------------------------------------#

#---------------PRODUCT-CATEGORY-PIE---------------#
prod_data = {}

for row in tqdm (csv_read, desc="Working on total product category data..."):
    prod = row['Product Category']
    revn = float(row['Revenue'])
    if(prod not in prod_data):
        prod_data[prod] = revn
    else:
        prod_data[prod] += revn

plt.figure(figsize=(10, 6))
plt.pie(prod_data.values(), labels=None, autopct=None, startangle=90, colors=['purple', 'royalblue','tomato','lightblue','yellowgreen','c','coral','peru'], wedgeprops = { 'linewidth' : 3, 'edgecolor' : 'white' })

my_circle=plt.Circle( (0,0), 0.7, color='white')
p=plt.gcf()
p.gca().add_artist(my_circle)

plt.title('Product Categories on basis of revenue')
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.3, hspace=0.5)
total = sum(prod_data.values())
percentages = [(number / total) * 100 for number in prod_data.values()]
plt.legend([f'{label} ({size:1.1f}%)' for label, size in zip(prod_data.keys(),percentages)], loc='center left', bbox_to_anchor=(1, 0.5))

#plt.tight_layout()

plt.savefig('pie_prod_data.png')
add_watermark('pie_prod_data.png', "made by rpd")
#--------------------------------------------------#
