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



#---------------WAREHOUSE-PIE---------------#
prod_data = {}
totOrd = 0
ordCnt = {}

for row in tqdm (csv_read, desc="Working on warehouse data..."):
    if(row['Order Number'] not in ordCnt):
        ordCnt[row['Order Number']] = 1
        totOrd += 1
        prod = row['Warehouse']
        revn = float(row['Revenue'])
        if(prod not in prod_data):
            prod_data[prod] = 1
        else:
            prod_data[prod] += 1

prod_data = dict(sorted(prod_data.items(), key=lambda item: item[0]))

plt.figure(figsize=(8, 8))
#plt.pie(prod_data.values(), labels=None, autopct=None, startangle=90, colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd','#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#FF5733', '#33FF57', '#5733FF', '#FF3385', '#85FF33'], wedgeprops = { 'linewidth' : 3, 'edgecolor' : 'white' })


plt.bar(prod_data.keys(),prod_data.values(),color='maroon')

#my_circle=plt.Circle( (0,0), 0.7, color='white')
#p=plt.gcf()
#p.gca().add_artist(my_circle)

plt.title('Warehouses on basis of revenue')
#plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.3, hspace=0.5)
#total = sum(prod_data.values())
#percentages = [(number / total) * 100 for number in prod_data.values()]
#plt.legend([f'{label} ({size:1.1f}%)' for label, size in zip(prod_data.keys(),percentages)], loc='center left', bbox_to_anchor=(1, 0.5))

#plt.tight_layout()
plt.tick_params(axis='x', rotation=45)
plt.savefig('pie_prod_data.png')
add_watermark('pie_prod_data.png', "made by rpd")
#-------------------------------------------#
