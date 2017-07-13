# To use:
# 1. Go to yobit.com and view 'bids' history. Save all those pages.
# 2. Save the page or pages to same directory as this script 
# as 'YoBit.Net.$index.html', range of 1-i
# 3. Run script and save output to file:
#   python3 getTradesFromHTMLPages.py <number of html pages> > yobit-trades.csv
#
#
# IMPORTANT:
# - bids page has all the actual executed trades, orders will have 
#   only what you placed the order at and so DO NOT USE THE ORDERS PAGE!
#
# - When you first save the page the download bar at the bottom 
#   will cause the js to resize the page pushing some trades to 
#   the next which causes lost or doubled trades when you import. 
#
#   So make sure that doesn't happen; first download the page so the download
#   bar comes up, then download the page again and use that copy.
#
# Tip: Zoom out on webpage and you can save more results per page.
#

from bs4 import BeautifulSoup

# yobit bids history page
def bidsCSV(numPages):
  print("Date,Action,Source,Symbol,Volume,Price,Currency")
  for i in range(numPages,0, -1):
    page = './YoBit.Net.' + str(i) + '.html'
    soup = BeautifulSoup(open(page))
    tables = soup.find_all('div', {'id': 'history_table_wrapper'})
    for table in tables:
      trades = table.find_all('tr')
      for trade in trades:
        cols = trade.select('td')
        if cols is not None and len(cols)>0:
          date = cols[0].text
          pair = cols[1].text
          source = "YoBit"
          symbol, curr = pair.split("/")
          action = cols[2].text
          price = cols[3].text
          amount = cols[4].text
          print('%s,%s,%s,%s,%s,%s,%s' % (date, action, source, symbol, amount, price, curr))

# yobit orders history page
def ordersCSV(numPages):
  print("Date,Action,Source,Symbol,Volume,Price,Currency")
  for i in range(numPages,0, -1):
    page = './YoBit.Net.' + str(i) + '.html'
    soup = BeautifulSoup(open(page))
    tables = soup.find_all('div', {'id': 'history_table_wrapper'})
    for table in tables:
      trades = table.find_all('tr')
      for trade in trades:
        cols = trade.select('td')
        if cols is not None and len(cols)>0:
          date = cols[1].text
          pair = cols[2].text
          source = "YoBit"
          symbol, curr = pair.split("/")
          action = cols[3].text
          price = cols[4].text
          amount = cols[6].text
          if amount == 0:
            continue
          print('%s,%s,%s,%s,%s,%s,%s' % (date, action, source, symbol, amount, price, curr))

numPages = sys.argv[1]
bidsCSV(numPages)
