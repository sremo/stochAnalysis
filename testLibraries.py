
import ystockquote
import stockprices

print "Importing historical prices"
#hist_prices_appl = ystockquote.get_historical_prices("AAPL","20120101","20120731")
#print "Historical prices imported"
#stock_appl = stockprices.Stock(hist_prices_appl, "AAPL")

tickers_list = open('tickers.txt','r')

SP500 = stockprices.Index("SP500")
start_date = "20120101"
end_date = "20120701"
for stock_ticker in tickers_list:
    print stock_ticker
    hist_prices = ystockquote.get_historical_prices(stock_ticker.strip(),start_date,end_date)
    SP500.addStock(stock_ticker.strip(),hist_prices)


prtf_remo = stockprices.Portfolio(SP500, "Remo Portfolio")
