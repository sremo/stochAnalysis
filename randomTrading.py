import numpy
import stockprices
import random
import ystockquote
import datetime
import matplotlib.pyplot


reload(stockprices)

def initializeit():
    print "Importing historical prices"

    tickers_list = open('tickers.txt','r')

    global SP500
    SP500 = stockprices.Index("SP500")
    start_date_string = "20120101"
    end_date_string = "20120901"

    global start_date 
    start_date = datetime.datetime.strptime(start_date_string, '%Y%m%d')

    global end_date 
    end_date = datetime.datetime.strptime(end_date_string, '%Y%m%d')

    for stock_ticker in tickers_list:
        print "Download historical prices ", stock_ticker.strip()
        try:
                hist_prices = ystockquote.get_historical_prices(stock_ticker.strip(),start_date_string,end_date_string)
                SP500.addStock(stock_ticker.strip(),hist_prices)
                print "Download successful"
        except IOError:
                print "Ticker ", stock_ticker.strip(), " could not be opened, skip to the next one\n"

    global rndtrading_portfolio 
    rndtrading_portfolio = stockprices.PortfolioWPositions(SP500, "Remo Portfolio")

    global sum_trades 
    sum_trades = 0
    global sum_closing_trades 
    sum_closing_trades = 0
    global no_positions 
    no_positions = 20
    global sizing 
    sizing = 5

def tradeit():
    global start_date, end_date
    global SP500
    global rndtrading_portfolio
    global return_threshold
    lower_return_threshold = -0.05
    upper_return_threshold = 10

    global profit_per_day
    profit_per_day = []
    global tot_profit_per_day
    tot_profit_per_day = []
    for weekday_date in stockprices.weekdays_daterange(start_date, end_date):
            daily_profit = 0
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
                if(open_pos.stock.availableOnDate(weekday_date)):
                    current_price = open_pos.stock.close[numpy.where(open_pos.stock.dates == weekday_date)]
                    if(rndtrading_portfolio.currentReturnPosition(open_pos,current_price) < lower_return_threshold or rndtrading_portfolio.currentReturnPosition(open_pos,current_price) < upper_return_threshold or (weekday_date-open_pos.entry_date).days > 20):
                        rndtrading_portfolio.closePosition(open_pos,current_price,weekday_date)
                        daily_profit += open_pos.profit
            profit_per_day.append(daily_profit)
            tot_profit_per_day.append(sum(profit_per_day))
    
    


    global tot_ret 
    tot_ret = 0
    global profits 
    profits = []
    global return_rates 
    return_rates = []

    for clsd in rndtrading_portfolio.closed_positions:
        tot_ret += clsd.profit
        profits.append(clsd.profit)
        return_rates.append(clsd.return_rate)
    rndtrading_portfolio.closed_positions = []
    rndtrading_portfolio.open_positions = []

    print tot_ret

def plotit():
    global return_rates
    global tot_profit_per_day
    fig = matplotlib.pyplot.figure(1)
    matplotlib.pyplot.plot(tot_profit_per_day)
    fig.show()
#    global hst_fig
#    hst_fig = matplotlib.pyplot.figure(1)
#    matplotlib.pyplot.hist(return_rates,500,(-0.02,0.02), normed=1)
#    matplotlib.pyplot.savefig("retrates.png")




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
