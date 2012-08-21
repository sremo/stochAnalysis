import numpy
import datetime
# read in stock prices (file, yahoo finance or direct feed)

def mkdate(text):
    return datetime.datetime.strptime(text, '%Y-%m-%d')    

def mkdatelist(date_lst):
        rtn = []
        for datet in date_lst:
                rtn.append(mkdate(datet))
        return rtn

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

def weekdays_daterange(start_date,end_date):
    for n in range(int ((end_date - start_date).days)):
        dte = start_date + datetime.timedelta(n)
        if (dte.weekday() != 5 and dte.weekday() != 6):
            yield dte
        

class Stock:
	def __init__(self,histDataListRaw,name):
		histDataList = histDataListRaw[1::]#numpy.delete(histDataListRaw,0,0)
		histDataList = histDataList[::-1]
                hd_array = numpy.array(histDataList)
                
		self.dates = numpy.array(mkdatelist(hd_array[:,0]), dtype = None)#numpy.array(histDataList[:][0])
		self.size = (self.dates).shape[0]
		self.name = name
		self.open = hd_array[:,1].astype(float)
		self.high =  hd_array[:,2].astype(float)
		self.low =   hd_array[:,3].astype(float)
		self.close =  hd_array[:,4].astype(float)
		self.volume =  hd_array[:,5].astype(float)
		self.adjclose =  hd_array[:,6].astype(float)
		self.startdate = self.dates[0]
#self.startdate = datetime.date(int(self.dates[0][0:4]),int(self.dates[0][5:7]),int(self.dates[0][8:10]))#self.dates[0]
		self.enddate = self.dates[-1]
		self.oorate = numpy.zeros(self.size)
		self.ocrate = numpy.zeros(self.size)
		for i in range(self.size-1):
			self.oorate[i] = self.open[i+1]/self.open[i]-1
		self.oorate[-1] = self.oorate[-2]
		self.ocrate = self.close/self.open-1

class Index:
    def __init__(self,indexname = 'Main Index'):
        self.name = indexname
        self.tickers = list() # list of all available stocks
        self.available_stocks = list() #list of lists of stocks
#available on a certain date
        self.stocks = {} #dict of objects stock
        self.end_date = 0

    def addStock(self, ticker, histDataList):
        newStock = Stock(histDataList, ticker)
        self.available_stocks.append(newStock)
        self.tickers.append(ticker)
        self.stocks[ticker] = newStock

    def getAvailableStocks(self,date):
        return [ticker for ticker in self.tickers if ((self.stocks).get(ticker)).startdate <= date and ((self.stocks).get(ticker)).enddate >= date]


class Portfolio:
    def __init__(self, index, portfolioname = 'Portfolio'):
        self.name = portfolioname
        self.holdings = {} # dict with keys given by tickers in index
# and value given by size of position
        self.trades = list() # list of all trades: ticker, date,
# price, size
        self.index = index
        for ticker in self.index.tickers:
            self.holdings[ticker] = 0

    def populateHoldingListTickers(self,tickers):
        for ticker in tickers:
            self.holdings[ticker] = 0
    
    def populateHoldingsListindex(self, indx):
        for ticker in indx.tickers:
            self.holdings[ticker] = 0

    def trade(self, ticker, size, date, price):
        self.holdings[ticker] += size
        self.trades.append([ticker, date, price, size])
        return (size*price) # commission, slippage??

    def closePosition(self,ticker,date, price):
        size = self.holdings[ticker]
        self.holdings[ticker] = 0
        self.trades.append([ticker, date, price, size])
        return size*price # commission, slippage??
  
