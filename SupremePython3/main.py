import requests
import pprint
import json
from timeit import default_timer as timer
from datetime import datetime

pp = pprint.PrettyPrinter()
url = 'http://supremenewyork.com/mobile_stock.json'
headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B350 Safari/8536.25"
}

def etcTime():
    current_time = datetime.now()
    return str(current_time) + ' EST'

def getJsonData(siteUrl):
    try:
        req = requests.get(siteUrl, headers=headers)  
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)
    else:
        json_data = req.json() 
        return json_data

def getShopLink(id):
    return 'http://www.supremenewyork.com/shop/' + str(id) + '.json'

def lookupItems(jsonData, keyword):
    for i in jsonData[u'products_and_categories'].values():
        for j in i:
            if keyword in j[u'name']:
                return j[u'id']

def lookupSize(jsonUrl, color, size):
    color = color.lower()
    size = str(size).lower()
    data = getJsonData(jsonUrl)
    found = False
    for i in data[u'styles']:
        if color in i[u'name'].lower():
            for j in i[u'sizes']:
                if size == j[u'name'] and j[u'stock_level'] > 0:
                    found = j[u'id']
                    return found
    return found

def addToCart(itemId, sizeId):
    addUrl = "http://www.supremenewyork.com/shop/" + str(itemId) + "/add.json"
    addHeaders = {
        'Host':                 'www.supremenewyork.com',
        'Accept':               'application/json',
        'Proxy-connection':     'keep-alive',
        'X-Requested-Width':    'XMLHttpRequest',
        'Accept-Encoding':      'gzip, deflate',
        'Accept-Language':      'en-us',
        'Content-Type':         'application/x-www-form-urlencoded',
        'Origin':               'http://www.supremenewyork.com',
        'Connection':           'keep-alive',
        'User-Agent':           'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257',
        'Referrer':             'http://www.supremenewyork.com/mobile'
    }
    addPayload = {
        'utf8': '%E2%9C%93',
        'st': str(itemId),
        's': str(sizeId),
        'commit': 'add+to+cart'
    }
    session = requests.Session()
    try:
        addResp = session.post(addUrl, data=addPayload, headers=addHeaders)
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)
    else:
        return addResp

def main():
    item  = 'Box Logo Hooded'
    color = 'Black'
    size  = 'Medium'
    # start the timer
    start = timer()
    # get the stock data
    stockData = getJsonData(url)
    pp.pprint(stockData)
    # lookup items in data
    itemId = lookupItems(stockData, item) 
    print('itemId', itemId)
    # get the shop link
    shopLink = getShopLink(itemId)
    # get size id from items
    sizeId = lookupSize(shopLink, color, size) 
    print('sizeId', sizeId)
    if not sizeId:
        pp.pprint('Out of stock')
    else:
        pp.pprint(addToCart(itemId, sizeId))

    pp.pprint(sizeId)
    end = timer()
    print ('Time elapsed: ', end - start)

if __name__ == "__main__":
    main()
