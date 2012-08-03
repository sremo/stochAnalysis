import numpy
import stockprices
import random

starttime = '20110101'
endtime = '20110630'
exchange = 'SP500'
tradnDays = tradingsDays(exchange, starttime, endtime) 

indx = Index('SP500')

for line in logfile:
	for word in line.split():
		#print word
		try:
			stocks = numpy.load('SP500/'+word+'.npy')
			indx.addStock(word,histPrice)
     		except IOError:
			print 'Ticker ', word, ' could not be opened, skip to the next one'

for day in tradnDays:
    avalStocks = indx.getAvailableStocks(day)
    long = random.sample(avalStocks, noPositions)
    short = random.sample(avalStocks, noPositions)
