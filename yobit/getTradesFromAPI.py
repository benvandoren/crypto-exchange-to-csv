# This was missing some older trades so DO NOT USE or at least double check
# the output. 
#
# At the very least it shows the yobit API usage. 
# It should be working but mistakes might have snuck in since 
# debugging the missing trade issue and committing the code.
# And because of my debugging some API calls might be
# needlessly explicit. I don't ever intend to use this,
# so you're on your own.
# 

from urllib.parse import urlencode
import json
import time
import requests
import hmac
import hashlib
import datetime

class yobit(object):

    def __init__(self):
        self.key = 'myKey'
        self.secret = b'mySecret'        
        self.public = ['info', 'ticker', 'depth', 'trades']
        self.trade = ['activeorders', 'getInfo', 'TradeHistory', 'tradehistory']

    def query(self, method, values={}):
        if method in self.public:
            url = 'https://yobit.net/api/3/'+method
            for i, k in values.iteritems():
                url += '/'+k

            req = requests.get(url)
            return json.loads(req.text)

        elif method in self.trade:
            url = 'https://yobit.net/tapi'
            values['method'] = method
            values['nonce'] = str(int(time.time()))
            body = urlencode(values).encode('ASCII')
            signature = hmac.new(self.secret, body, hashlib.sha512).hexdigest()
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Key': self.key,
                'Sign': signature
            }

            req = requests.post(url,data=values,headers=headers)
            return json.loads(req.text)

        return "error"

    def printCSV(self, source, curr):
        pair = source + '_' + curr
        queryRtn = self.query('TradeHistory', values={'pair':pair,'from':'0','count':'9999999999999', 'from_id':'0','since':'0'})
        
        print(queryRtn)
        if len(queryRtn) == 1:
            print("No Data")
            return 1

        transactions = queryRtn['return']
        for tradeId in transactions:
            trade = transactions[tradeId]
            date = datetime.datetime.fromtimestamp(int(trade['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
            action = trade['type']
            volume = trade['amount']
            price = trade['rate']
            fee = ''
            feeCurr = ''
            print('%s, %s, %s, %s, %s, %s, %s, %s' % (date, action, source, volume, curr, price, fee, feeCurr))
        return 0

# blah just hardcode this
source = 'pivx'
curr = 'btc'
yobit = yobit()
yobit.printCSV(source, curr)
