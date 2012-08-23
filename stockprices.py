import numpy
import datetime
import math
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
                # INDEX arrays with Dates!!
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
        
        def availableOnDate(self,date):
            return date in self.dates
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

    def getAvailableStocks_deprecated(self,date):
        return [ticker for ticker in self.tickers if ((self.stocks).get(ticker)).startdate <= date and ((self.stocks).get(ticker)).enddate >= date]

    def getAvailableStocks(self,date):
        return [ticker for ticker in self.tickers if (date in ((self.stocks).get(ticker)).dates)]

class Position:
    def __init__(self, index, stock, ticker, entry_date, entry_price, size):
        self.index = index
        self.stock = stock
        self.size = size
        self.ticker = ticker
        self.entry_date = entry_date
        self.exit_date = "Open"
        self.entry_price = entry_price
        self.exit_price = "Open"
        self.profit = "Open"
        self.return_rate = "Open"
        self.status = "Open"

    def closePosition(self, exit_price, exit_date):
        self.exit_price =exit_price
        self.exit_date = exit_date
        self.profit = self.size*(self.exit_price-self.entry_price)
        if self.size > 0:
            self.return_rate = math.log(self.exit_price/self.entry_price)
        else:
            self.return_rate = math.log(self.entry_price/self.entry_price)

        self.status = "Closed"

class PortfolioWPositions:
    def __init__(self, index, portfolioname = 'Portfolio'):
        self.name = portfolioname
        self.holdings = {} # dict with keys given by tickers in index
# and value given by size of position
        self.open_positions = list()
        self.closed_positions = list()
        self.index = index
        for ticker in self.index.tickers:
            self.holdings[ticker] = 0

    def populateHoldingListTickers(self,tickers):
        for ticker in tickers:
            self.holdings[ticker] = 0
    
    def populateHoldingsListindex(self, indx):
        for ticker in indx.tickers:
            self.holdings[ticker] = 0

    def enterPosition(self, curr_ticker, enter_date,enter_price, pos_size):
        curr_stock = self.index.stocks.get(curr_ticker)
        if curr_stock.availableOnDate(enter_date):
            new_position = Position(self.index, curr_stock, curr_ticker, enter_date, enter_price, pos_size)
            self.open_positions.append(new_position)
            self.holdings[curr_ticker] += pos_size
            return pos_size*enter_price

    def closePosition(self, postn, exit_price, exit_date):
        self.open_positions.remove(postn)
        postn.closePosition(exit_price, exit_date)
        self.closed_positions.append(postn)
        self.holdings[postn.ticker] += postn.size
        return postn.size*exit_price

    def currentPLPosition(self,postn,curr_price):
        return postn.size*(curr_price - postn.entry_price)

    def currentReturnPosition(self,postn,curr_price):
        if postn.size>0:
            return math.log(curr_price/postn.entry_price)
        else:
            return math.log(postn.entry_price/curr_price)

    # def trade(self, ticker, size, date, price):
    #     self.holdings[ticker] += size
    #     self.trades.append([ticker, date, price, size])
    #     self.active_trades.append([ticker, date, price, size])
    #     return (size*price) # commission, slippage??

    # def closeTrade(self,ticker, curr_date, size ):
    #     stock = self.index.stocks.get(ticker)
    #     if stock.availableOnDate(curr_date):
    #         self.holdings[ticker] -= size
    #         exit_price = self.index.stocks.get(ticker).close[numpy.where(stock.dates == curr_date)]
    #         self.trades.append([ticker, curr_date, exit_price ,-size])
    #         print ticker, exit_price, curr_date
    #         return exit_price*size
    #     return 0

    # def closePosition(self,ticker,date, price):
    #     size = self.holdings[ticker]
    #     self.holdings[ticker] = 0
    #     self.trades.append([ticker, date, price, size])
    #     return size*price # commission, slippage??

  
class Portfolio:
    def __init__(self, index, portfolioname = 'Portfolio'):
        self.name = portfolioname
        self.holdings = {} # dict with keys given by tickers in index
# and value given by size of position
        self.active_trades = list()
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
        self.active_trades.append([ticker, date, price, size])
        return (size*price) # commission, slippage??

    def closeTrade(self,ticker, curr_date, size ):
        stock = self.index.stocks.get(ticker)
        if stock.availableOnDate(curr_date):
            self.holdings[ticker] -= size
            exit_price = self.index.stocks.get(ticker).close[numpy.where(stock.dates == curr_date)]
            self.trades.append([ticker, curr_date, exit_price ,-size])
            print ticker, exit_price, curr_date
            return exit_price*size
        return 0

    def closePosition(self,ticker,date, price):
        size = self.holdings[ticker]
        self.holdings[ticker] = 0
        self.trades.append([ticker, date, price, size])
        return size*price # commission, slippage??

