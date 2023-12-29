import csv
import os
from tqdm import tqdm
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime as dt


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


#----------------FREQUENCY----------------#

#creating frequency dictionary
freq_data = {}
freq_data_by_year = {}
for row in tqdm (csv_read, desc="Working on frequency data..."):
    dateData = row['Invoice Date']
    year = str(dt.strptime(dateData,"%d-%m-%Y %H:%M").year)
    if(year not in freq_data_by_year):
        freq_data_by_year[year] = {}
    if(row['Customer ID'] not in freq_data_by_year[year]):
        freq_data_by_year[year][row['Customer ID']] = 1
    else:
        freq_data_by_year[year][row['Customer ID']] += 1

    if(row['Customer ID'] not in freq_data):
        freq_data[row['Customer ID']] = 1
    else:
        freq_data[row['Customer ID']] += 1

#top 10 customers of all time by frequency
freq_data_top_10_all = dict(sorted(freq_data.items(), key=lambda item: item[1],reverse=True)[0:10])
custID__list_10_all = list(freq_data_top_10_all.keys())
custVal_list_10_all = list(freq_data_top_10_all.values())


#top 10 customers by year by frequency
freq_data_top_10 = {}
custID__list_10 = {}
custVal_list_10 = {}

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))

xBin=[0,0,1,1]
yBin=[0,1,0,1]

for y in ["2017","2018","2019"]:
    freq_data_top_10[y] = dict(sorted(freq_data_by_year[y].items(), key=lambda item: item[1],reverse=True)[0:10])
    custID__list_10[y] = list(freq_data_top_10[y].keys())
    custVal_list_10[y] = list(freq_data_top_10[y].values())

    
    axes[xBin[int(y)-2017],yBin[int(y)-2017]].bar(custID__list_10[y],custVal_list_10[y],color='orange')
    axes[xBin[int(y)-2017],yBin[int(y)-2017]].set_xlabel("Customer ID")
    axes[xBin[int(y)-2017],yBin[int(y)-2017]].set_ylabel("Frequency")
    axes[xBin[int(y)-2017],yBin[int(y)-2017]].set_title("Top 10 customers in "+y+" by frequency")
    


axes[1,1].bar(custID__list_10_all,custVal_list_10_all,color='m')
axes[1,1].set_xlabel("Customer ID")
axes[1,1].set_ylabel("Frequency")
axes[1,1].set_title("Top 10 customers of all time by frequency")


for ax in axes.flat:
    ax.tick_params(axis='x', rotation=45)

plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.3, hspace=0.5)

plt.savefig('freq_data.png')
add_watermark('freq_data.png', "made by rpd")

#-------------------END-------------------#

#-------------------COST-REVENUE-------------------#

finc_data = {}
finc_data_all = {}

for row in tqdm (csv_read, desc="Working on financial data..."):
    cID = row['Customer ID']
    dateData = row['Invoice Date']
    year = str(dt.strptime(dateData,"%d-%m-%Y %H:%M").year)

    rev = float(row['Revenue'])
    cst = float(row['Cost'])
    if(year not in finc_data):
        finc_data[year] = {}

    if(cID not in finc_data[year]):
        finc_data[year][cID] = [rev,cst]
    else:
        finc_data[year][cID][0] += rev
        finc_data[year][cID][1] += cst

    if(cID not in finc_data_all):
        finc_data_all[cID] = [rev,cst]
    else:
        finc_data_all[cID][0] += rev
        finc_data_all[cID][1] += cst


#-----------year-wise-rev-start-----------#
finc_data_top_10_all = dict(sorted(finc_data_all.items(), key=lambda item: item[1][0],reverse=True)[0:10])
custID__list_10_all = list(finc_data_top_10_all.keys())
custVal_list_10_all = [fd[0] for fd in finc_data_top_10_all.values()][0:10]

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))

xBin=[0,0,1,1]
yBin=[0,1,0,1]

for finc in finc_data:
    finc_data_sort = dict(sorted(finc_data[finc].items(), key=lambda item: item[1][0],reverse=True)[0:10])
    custID__list = list(finc_data_sort.keys())[0:10]
    custRev_list = [fd[0] for fd in finc_data_sort.values()][0:10]
    y=finc
    axes[xBin[int(y)-2017],yBin[int(y)-2017]].bar(custID__list,custRev_list,color='orange')
    axes[xBin[int(y)-2017],yBin[int(y)-2017]].set_xlabel("Customer ID")
    axes[xBin[int(y)-2017],yBin[int(y)-2017]].set_ylabel("Frequency")
    axes[xBin[int(y)-2017],yBin[int(y)-2017]].set_title("Top 10 customers in "+y+" by revenue")


axes[1,1].bar(custID__list_10_all,custVal_list_10_all,color='m')
axes[1,1].set_xlabel("Customer ID")
axes[1,1].set_ylabel("Frequency")
axes[1,1].set_title("Top 10 customers of all time by Revenue")


for ax in axes.flat:
    ax.tick_params(axis='x', rotation=45)

plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.3, hspace=0.5)

plt.savefig('finc_rev_data.png')
add_watermark('finc_rev_data.png', "made by rpd")
#------------year-wise-rev-end------------#

#-----------year-wise-cst-start-----------#
finc_data_top_10_all = dict(sorted(finc_data_all.items(), key=lambda item: item[1][1],reverse=True)[0:10])
custID__list_10_all = list(finc_data_top_10_all.keys())
custVal_list_10_all = [fd[1] for fd in finc_data_top_10_all.values()][0:10]

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))

xBin=[0,0,1,1]
yBin=[0,1,0,1]

for finc in finc_data:
    finc_data_sort = dict(sorted(finc_data[finc].items(), key=lambda item: item[1][1],reverse=True)[0:10])
    custID__list = list(finc_data_sort.keys())[0:10]
    custCst_list = [fd[1] for fd in finc_data_sort.values()][0:10]
    y=finc
    axes[xBin[int(y)-2017],yBin[int(y)-2017]].bar(custID__list,custCst_list,color='orange')
    axes[xBin[int(y)-2017],yBin[int(y)-2017]].set_xlabel("Customer ID")
    axes[xBin[int(y)-2017],yBin[int(y)-2017]].set_ylabel("Frequency")
    axes[xBin[int(y)-2017],yBin[int(y)-2017]].set_title("Top 10 customers in "+y+" by cost")


axes[1,1].bar(custID__list_10_all,custVal_list_10_all,color='m')
axes[1,1].set_xlabel("Customer ID")
axes[1,1].set_ylabel("Frequency")
axes[1,1].set_title("Top 10 customers of all time by Cost")


for ax in axes.flat:
    ax.tick_params(axis='x', rotation=45)

plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.3, hspace=0.5)

plt.savefig('finc_cst_data.png')
add_watermark('finc_cst_data.png', "made by rpd")
#------------year-wise-cst-end------------#


#-----------year-wise-comparison-start-----------#
finc_data_top_10_all = dict(sorted(finc_data_all.items(), key=lambda item: item[1][0],reverse=True)[0:10])
custID__list_10_all = list(finc_data_top_10_all.keys())
custVal_list_10_all_rev = [fd[0] for fd in finc_data_top_10_all.values()][0:10]
custVal_list_10_all_cst = [fd[1] for fd in finc_data_top_10_all.values()][0:10]

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))

xBin=[0,0,1,1]
yBin=[0,1,0,1]

for finc in finc_data:
    finc_data_sort = dict(sorted(finc_data[finc].items(), key=lambda item: item[1][0],reverse=True)[0:10])
    custID__list = list(finc_data_sort.keys())[0:10]
    custRev_list = [fd[0] for fd in finc_data_sort.values()][0:10]
    custCst_list = [fd[1] for fd in finc_data_sort.values()][0:10]
    y=finc
    axes[xBin[int(y)-2017],yBin[int(y)-2017]].bar(custID__list,custRev_list,color='orange',label="Revenue")
    axes[xBin[int(y)-2017],yBin[int(y)-2017]].bar(custID__list,custCst_list,color='red',bottom=custRev_list,label="Cost")
    axes[xBin[int(y)-2017],yBin[int(y)-2017]].set_xlabel("Customer ID")
    axes[xBin[int(y)-2017],yBin[int(y)-2017]].set_ylabel("Frequency")
    axes[xBin[int(y)-2017],yBin[int(y)-2017]].set_title("Top 10 customers cost revenue comparison in "+y)
    axes[xBin[int(y)-2017],yBin[int(y)-2017]].legend()

axes[1,1].bar(custID__list_10_all,custVal_list_10_all_rev,color='m',label="Revenue")
axes[1,1].bar(custID__list_10_all,custVal_list_10_all_cst,color='blue',bottom=custVal_list_10_all_rev,label="Cost")
axes[1,1].set_xlabel("Customer ID")
axes[1,1].set_ylabel("Frequency")
axes[1,1].set_title("Top 10 customers cost revenue comparison of all time")
axes[1,1].legend()


for ax in axes.flat:
    ax.tick_params(axis='x', rotation=45)

plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.3, hspace=0.5)

plt.savefig('finc_comp_data.png')
add_watermark('finc_comp_data.png', "made by rpd")
#------------year-wise-comparison-end------------#


#-----------------------END------------------------#

#---------------END-MARKET---------------#
end_mrkt = {}
custDone = []

for row in tqdm (csv_read, desc="Working on end market data..."):
    cID = row['Customer ID']
    eMrk = row['End Market']
    if(cID not in custDone):
        custDone.insert(0,cID)
        if(eMrk not in end_mrkt):
            end_mrkt[eMrk] = 1
        else:
            end_mrkt[eMrk] += 1

plt.figure(figsize=(8, 8))
plt.pie(end_mrkt.values(), labels=end_mrkt.keys(), autopct='%1.1f%%', startangle=90, colors=['orange', 'red'], wedgeprops = { 'linewidth' : 3, 'edgecolor' : 'white' })

my_circle=plt.Circle( (0,0), 0.7, color='white')
p=plt.gcf()
p.gca().add_artist(my_circle)

plt.title('End Market categorised on the basis of customers')
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.3, hspace=0.5)

plt.savefig('end_market_data.png')
add_watermark('end_market_data.png', "made by rpd")

print("Total customers:",len(custDone))
#---------------END----------------------#



#plt.show()
