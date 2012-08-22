import numpy
import stockprices
import random
import ystockquote
import datetime
import matplotlib.pyplot


def initializeit():
    print "Importing historical prices"

    tickers_list = open('tickers.txt','r')

    global SP500 = stockprices.Index("SP500")
    start_date_string = "20120101"
    end_date_string = "20120901"

    global start_date = datetime.datetime.strptime(start_date_string, '%Y%m%d')

    global end_date = datetime.datetime.strptime(end_date_string, '%Y%m%d')

    for stock_ticker in tickers_list:
        print "Download historical prices ", stock_ticker.strip()
        try:
                hist_prices = ystockquote.get_historical_prices(stock_ticker.strip(),start_date_string,end_date_string)
                SP500.addStock(stock_ticker.strip(),hist_prices)
                print "Download successful"
        except IOError:
                print "Ticker ", stock_ticker.strip(), " could not be opened, skip to the next one\n"

    global rndtrading_portfolio = stockprices.PortfolioWPositions(SP500, "Remo Portfolio")

    global sum_trades = 0
    global sum_closing_trades = 0
    global no_positions = 10
    global sizing =5

def tradeit():
    global start_date, end_date
    global SP500
    global rndtrading_portfolio
    for weekday_date in stockprices.weekdays_daterange(start_date, end_date):
            available_stocks = SP500.getAvailableStocks(weekday_date)
            if len(available_stocks) >1:
                    long_positions = random.sample(available_stocks, no_positions)
                    short_positions = random.sample(available_stocks, no_positions)
                    #print "Going long on:"
                    for long_stock_ticker in long_positions:
                            #print "L:", long_stock
                        long_stock = SP500.stocks.get(long_stock_ticker)
                        entry_price = long_stock.close[numpy.where(long_stock.dates == weekday_date)]
                        rndtrading_portfolio.enterPosition(long_stock_ticker,weekday_date,entry_price, sizing)
                    #print "Going short on:"
                    for short_stock_ticker in short_positions:
                            #print "S:",short_stock
                        short_stock = SP500.stocks.get(short_stock_ticker)
                        entry_price = short_stock.close[numpy.where(short_stock.dates == weekday_date)]
                        rndtrading_portfolio.enterPosition(short_stock_ticker, weekday_date, entry_price, -sizing)

            for open_pos in rndtrading_portfolio.open_positions:
                if((weekday_date-open_pos.entry_date).days > 10):
                    if(open_pos.stock.availableOnDate(weekday_date)):
                        exit_price = open_pos.stock.close[numpy.where(open_pos.stock.dates == weekday_date)]
                        rndtrading_portfolio.closePosition(open_pos,exit_price,weekday_date)


    global tot_ret = 0
    global profits = list()
    global return_rates = list()

    for clsd in rndtrading_portfolio.closed_positions:
        tot_ret += clsd.profit
        profits.append(clsd.profit)
        return_rates.append(clsd.return_rate)

    print tot_ret

def plotit():
    global return_rates
    matplotlib.pyplot.hist(return_rates,100,(-0.15,0.15))
    matplotlib.pyplot.savefig("retrates.png")
# for weekday_date in stockprices.weekdays_daterange(start_date, end_date):
#         available_stocks = SP500.getAvailableStocks(weekday_date)
#         if len(available_stocks) >1:
#                 long_positions = random.sample(available_stocks, no_positions)
#                 short_positions = random.sample(available_stocks, no_positions)
#                 #print "Going long on:"
#                 for long_stock in long_positions:
#                         #print "L:", long_stock
#                         sum_trades = sum_trades - rndtrading_portfolio.trade(long_stock, 1, weekday_date,SP500.stocks.get(long_stock).close[numpy.where(SP500.stocks.get(long_stock).dates == weekday_date)])
#                 #print "Going short on:"
#                 for short_stock in short_positions:
#                         #print "S:",short_stock
#                         rndtrading_portfolio.trade(short_stock, 1, weekday_date,SP500.stocks.get(short_stock).close[numpy.where(SP500.stocks.get(short_stock).dates == weekday_date)])

#         for act_trade in rndtrading_portfolio.active_trades:
#             if((weekday_date-act_trade[1]).days>10):
#                 close_pos_ticker = act_trade[0]
#                 pos_size = act_trade[3]
#                 sum_trades = sum_trades + rndtrading_portfolio.closeTrade(close_pos_ticker,weekday_date,pos_size)
#                 rndtrading_portfolio.active_trades.remove(act_trade)


# print "Balance: ", sumTrades

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
