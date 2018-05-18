# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 10:36:05 2018

@author: yuhaibo
"""

from bs4 import BeautifulSoup
import requests
import re
import time
import csv
import os
import codecs
import json
from urllib.parse import urlencode
from requests.exceptions import RequestException
from json.decoder import JSONDecodeError
from hashlib import md5
from multiprocessing import Pool
'''
目标:获取延安市的携程酒店信息
'''

url = "http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx?"
folder = "E:/携程/鹰潭/"
path = folder+"鹰潭5.csv"
csvfile = open(path, 'w', newline='',errors='ignore')
csvfile.write(str(codecs.BOM_UTF8))
writer = csv.writer(csvfile,dialect='excel')
writer.writerow(('id','酒店名称','星级','地址','行政区','经度','纬度','价格','评分','推荐率','评论数','酒店类型','简称','url'))
   

def get_page(url,star,page,data=None):
    # 创建输出路径
    if os.path.isdir(folder) == False:
        os.makedirs(folder)

    testData = {'__VIEWSTATEGENERATOR':'DB1FBB6D',
            'cityName': '%E9%B9%B0%E6%BD%AD',
            'StartTime': '2018-05-27',
            'DepTime': '2018-05-28',
            'RoomGuestCount': '1,1,0',
            'cityId': '534',
            'cityPY': 'yingtan',
            'cityCode': '0701',
            'cityLat': '28.244597',
            'cityLng': '117.040715',
            'htlPageView': '0',
            'hotelType': 'F',
            'hasPKGHotel': 'F',
            'requestTravelMoney': 'F',
            'isusergiftcard': 'F',
            'useFG': 'F',
            'HotelEquipment':'', 
            'priceRange': '-2',
            'hotelBrandId':'', 
            'promotion': 'F',
            'prepay': 'F',
            'IsCanReserve': 'F',
            'OrderBy': '99',
            'checkIn': '2018-05-27',
            'checkOut': '2018-05-28',
            'DealSale': '',
            'ulogin': '',
            'hidTestLat': '0%7C0',
            'AllHotelIds': '5347302%2C2862335%2C6532851%2C2041781%2C895510%2C5916263%2C2301818%2C1343168%2C900624%2C4394796%2C7586060%2C15226245%2C1228588%2C5485740%2C1430192%2C7361769%2C6085373%2C1419879%2C4605716%2C1535941%2C1768331%2C901013%2C1692033%2C1350391%2C2218186',
            'psid':'' ,
            'HideIsNoneLogin': 'T',
            'isfromlist': 'T',
            'ubt_price_key': 'htl_search_result_promotion',
            'showwindow': '',
            'defaultcoupon': '',
            'isHuaZhu': 'False',
            'hotelPriceLow':'', 
            'htlFrom': 'hotellist',
            'unBookHotelTraceCode':'' ,
            'showTipFlg': '',
            'hotelIds': '5347302_1_1,2862335_2_1,6532851_3_1,2041781_4_1,895510_5_1,5916263_6_1,2301818_7_1,1343168_8_1,900624_9_1,4394796_10_1,7586060_11_1,15226245_12_1,1228588_13_1,5485740_14_1,1430192_15_1,7361769_16_1,6085373_17_1,1419879_18_1,4605716_19_1,1535941_20_1,1768331_21_1,901013_22_1,1692033_23_1,1350391_24_1,2218186_25_1',
            'markType': '0',
            'zone': '',
            'location': '',
            'type':'', 
            'brand':'', 
            'group':'' ,
            'feature':'', 
            'equip':'', 
            'star': star,
            'sl':'' ,
            's': '',
            'l': '',
            'price': '',
            'a': '0',
            'keywordLat':'', 
            'keywordLon':'', 
            'contrast':'0',
            'contyped': '0',
            'productcode':'', 
            'page': page
            }
    #print(url + urlencode(testData))
    resq = requests.get(url + urlencode(testData)).json()
#    print(resq)

    hotelinf = resq.get('hotelPositionJSON')
    hotelamount = resq.get('HotelMaiDianData')
    amounts = hotelamount['value']['htllist']
    amounts = amounts.replace('[','').replace(']','').replace('{','').replace('}','').replace('"hotelid":','').replace('"amount":','').replace('"','')
    amounts = amounts.strip(',').split(',')
    amounts = amounts[1::2]
    print('page:' + str(page) +',酒店数:'+str(len(hotelinf)))
    
   
    for i in range(len(hotelinf)):
        
        hotelid = hotelinf[i]['id']
        hotelname = hotelinf[i]['name']
        hotellon = hotelinf[i]['lon']
        hotellat = hotelinf[i]['lat']
        hotelurl = hotelinf[i]['url']
        hoteladdress = hotelinf[i]['address']
        hotelscore = hotelinf[i]['score']
        hoteldpscore = hotelinf[i]['dpscore']
        hoteldpcount = hotelinf[i]['dpcount']
        hoteldesc = hotelinf[i]['stardesc']
        hotelshortName = hotelinf[i]['shortName']
        print(hotelname)
        
        
        price = amounts[i]
        
        writer.writerow((hotelid, hotelname,star,hoteladdress,hoteladdress[0:2],hotellon,hotellat,price,hotelscore,hoteldpscore,hoteldpcount, hoteldesc,hotelshortName,hotelurl))
 
def get_more_pages(start,end,star):
    for one in range(start,end):
        get_page(url,star,str(one))
        time.sleep(2)
    csvfile.close()
    

get_more_pages(1,13,2)
