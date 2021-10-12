import numpy as np
import binanceapikey # a .py file with your api keys
from binance.client import Client
import time
import pandas as pd

client = Client(binanceapikey.API_KEY, binanceapikey.SECRET_KEY) #Binance credentials
# client = Client(binanceapikey.API_TEST, binanceapikey.SECRET_TEST, testnet = True) #Binance paper account credentials (can't get it to work)
pair = ['ONTUSDT','SOLUSDT','XMRUSDT','IOTAUSDT','OMGUSDT'] #Cryptocoin pair 
quantity = [20,0.15,0.07,15,1.5] #How much to deal with, must be align with the 'pair' list
decimals = [4,2,1,4,3] #Number of decimals the Cryptocoin accepts, also must be align

def tendency(current_coin): #first derivative, check if in up or downtrend
	x = []
	y = []
	counter = 0
	mean_50 = 0
	tendency_50 = False

	klines = client.get_historical_klines(current_coin, Client.KLINE_INTERVAL_15MINUTE,"18 hour ago")

	if len(klines) == 72:
		for i in range(56,72):
			for j in range(i-50, i):
				counter = counter + float(klines[i][4])
			mean_50 = counter/50
			counter = 0
			x.append(i)
			y.append(mean_50)

		model = np.polyfit(x,y,1)
		if model[0] > 0:
			tendency_50 = True
		
		return (tendency_50)


def ma_50(current_coin): #moving average 50, 15 minutes
	klines = client.get_historical_klines(current_coin, Client.KLINE_INTERVAL_15MINUTE,"13 hour ago")
	counter = 0
	mean = 0
	if len(klines) == 52:
		for i in range(2,52):
			counter = counter + float(klines[i][4])		
		mean = counter/50
		return float(mean)
	

def review_current_order(current_coin, flo_po): #checks conditions to apply stoploss
	open_orders = client.get_open_orders(symbol=current_coin)

	#check open orders
	if len(open_orders) != 0:
		current_order = open_orders[0]
		print('There is an open order')
		print('Order:')
		print(current_order)
		df_order = pd.DataFrame(current_order, index = [0])		
		order_price = df_order['price']
		ticker = client.get_symbol_ticker(symbol = current_coin)
		price = ticker['price']
		for i in order_price:
			limit=float(i)
		
		 # if the current price gets close to the selling price, the limit gets 1% higher 
		 # a stop_loss price in set 2% lower than the the previous limit
		 # limit order is never executed for it is always going up chasing the maximun price
		 # coins will be sold at stop_loss price
		 # this way we sold always 1% lower than the peak price

		if round(float(price),flo_po) >= round(float(limit)*0.99,flo_po):
			print('cancelling order, setting stop_loss limit')			  		

			order_id_1 = df_order['orderId']
			for i in order_id_1:
				order_id = int(i)

			quantity_order_1 = df_order['origQty']
			for i in quantity_order_1:
				quantity_order = float(i)

			cancelled_order = client.cancel_order(
				symbol = current_coin,
				orderId = order_id
				)

			stop_limit_order =  client.create_order(
				symbol = current_coin,
				side = 'BUY',
				type = 'STOP_LOSS_LIMIT',
				price = round(float(limit)*1.01,flo_po),
				stopPrice = round(float(limit)*0.98,flo_po),
				timeInForce = 'GTC'
				)			
			print('Cancelled order:')
			print(cancelled_order)
			print('New order:')
			print(stop_limit_order)
			
		
		else:
			print('Current order for ' + current_coin + ' is OK for now')
			print(' ')
		return(True)
			
	else:
		print('There are no open orders for: ' + current_coin)		
		return(False)

def set_order(current_coin, quant, flo_po):
	ticker = client.get_symbol_ticker(symbol=current_coin)
	price = ticker['price']
	mean50 = ma_50(current_coin)
	print(current_coin + ':')
	print('MA 50: ' + str(mean50))
	print('Current price: ' + str(price))

	if not tendency(current_coin): #Only works at uptrends
		print('Downtrend')
		print(' ')			
	else:
		print('Uptrend!') 

		# No initial stop_loss
		# if prices don't go up the script will HODL untill they do

		if float(price) < mean50*0.98: #buys at a price 2% lower than te MA50
			print('Buying!')

			buy_order = client.order_market_buy(
				symbol = current_coin,
				quantity = quant
				)
			print('Bought, making sell order')

			sell_order = client.order_limit_sell(
				symbol = current_coin,
				quantity = quant,
				price = round(float(price)*1.04, flo_po), #Sells at a price 4% higher
				timeInForce = 'GTC',				
				)

			print('Sell order made')


while True: #Loop
	try:

		for i in range(len(pair)):
			coin = pair[i]
			coin_quantity = quantity[i]
			coin_point = decimals[i]
			if not review_current_order(coin, coin_point):
				set_order(coin, coin_quantity, coin_point)

		print('A cycle has been completed')
		print('sleeping for a bit')
		print(' ')
		time.sleep(20)
	
	except:
		print('Something went wrong, possibly connection was interrupted')
		print('trying again in a moment')
		time.sleep(20)
		continue

