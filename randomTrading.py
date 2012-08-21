import numpy
import stockprices
import random

print "Importing historical prices"

tickers_list = open('tickers.txt','r')

SP500 = stockprices.Index("SP500")
start_date_string = "20120101"
end_date_string = "20120701"

start_date = datetime.datetime.strptime(start_date_string, '%Y%m%d')

end_date = datetime.datetime.strptime(end_date_string, '%Y%m%d')

for stock_ticker in tickers_list:
    print "Download historical prices ", stock_ticker.strip()
    try:
            hist_prices = ystockquote.get_historical_prices(stock_ticker.strip(),start_date_string,end_date_string)
            SP500.addStock(stock_ticker.strip(),hist_prices)
            print "Download successful"
    except IOError:
            print "Ticker ", stock_ticker.strip(), " could not be opened, skip to the next one\n"

rndtrading_portfolio = stockprices.Portfolio(SP500, "Remo Portfolio")

for weekday_date in stockprices.weekdays_daterange(start_date, end_date):
        available_stocks = indx.getAvailableStocks(weekday_date)
        if len(available_stocks) >1:
                long_positions = random.sample(available_stocks, no_positions)
                short_positions = random.sample(available_stocks, no_positions)
                for long_stock in long_positions:
                        print long_stock
                        rndtrading_portfolio.trade(long_stock, 1, weekday_date, 
#for line in logfile:
#	for word in line.split():
#		#print word
#		try:
#			stocks = numpy.load('SP500/'+word+'.npy')
#			indx.addStock(word,histPrice)
 #    		except IOError:
#			print 'Ticker ', word, ' could not be opened, skip to the next one'

#for day in tradnDays:
#    avalStocks = indx.getAvailableStocks(day)
#    long = random.sample(SP500, noPositions)
#    short = random.sample(avalStocks, noPositions)
