import numpy
import datetime
# read in stock prices (file, yahoo finance or direct feed)

class Stock:
	def __init__(self,histDataListRaw,name):
                histDataList = numpy.array(histDataListRaw)
		histDataList = numpy.delete(histDataList,0,0)
		histDataList = histDataList[::-1,:]
		self.dates = numpy.array(histDataList[:,0])
		self.size = histDataList.shape[0]
		self.name = name
		self.open = numpy.array(histDataList[:,1]).astype(float)
		self.high = numpy.array(histDataList[:,2]).astype(float)
		self.low = numpy.array(histDataList[:,3]).astype(float)
		self.close = numpy.array(histDataList[:,4]).astype(float)
		self.volume = numpy.array(histDataList[:,5]).astype(float)
		self.adjclose = numpy.array(histDataList[:,6]).astype(float)
		self.startdate = datetime.date(int(self.dates[0][0:4]),int(self.dates[0][5:7]),int(self.dates[0][8:10]))#self.dates[0]
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

    def getAvailableStocks(self,date):
        return (ticker for ticker in self.tickers if ((self.stocks).get[ticker]).startdate >= date and  ((self.stocks).get[ticker]).enddate <= date)


class Portfolio:
    def __init__(self, index, portfolioname = 'Portfolio'):
        self.name = portfolioname
        self.holdings = {} # dict with keys given by tickers in index
# and value given by size of position
        self.trades = list() # list of all trades: ticker, date,
# price, size
        self.index = index

    def populateHoldingList(self,tickers):
        for ticker in tickers:
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
  
