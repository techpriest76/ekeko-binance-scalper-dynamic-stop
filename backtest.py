import binanceapikey
from binance.client import Client

client = Client(binanceapikey.API_KEY, binanceapikey.SECRET_KEY)

dollars = 19.14
BTC_q = 0
buy_q = 0
sell_q = 0
currency = 'BTCUSDT'

klines = client.get_historical_klines(currency, Client.KLINE_INTERVAL_15MINUTE, '1 year ago UTC')
print('number of klines: ' + str(len(klines)))

# BTC_q = dolars/float(klines[0][4])
# print(BTC_q)
# comision de binance 0.075% 1.00075
# initial dollars

hold = 19.14*float(klines[-1][4])

for i in range(50, len(klines)):
    counter = 0
    mean = 0
    for j in range(i-50, i):
        counter = counter + float(klines[j][4])
    mean = counter/50

    price = float(klines[i][4])
    if price < mean * 0.980 and 0 < dollars:
        BTC_q = BTC_q + dollars / float(klines[i][4])
        dollars = dollars - BTC_q * float(klines[i][4])
        print('MA 50: ' + str(mean))
        print('buying at: ' + str(klines[i][4]))
        buy_q += 1
        print('dollars: ' + str(dollars))
        print('BTCs in wallet: ' + str(BTC_q))
        print('---------------')
        print(' ')


    # vender
    elif float(klines[i][4]) > mean * 1.04 and 0 < BTC_q:
        dollars = dollars + BTC_q * float(klines[i][4])
        BTC_q = BTC_q - dollars / float(klines[i][4])
        print('MA 50: ' + str(mean))
        print('selling at: ' + str(klines[i][4]))
        sell_q += 1
        print('dollars: ' + str(dollars))
        print('BTCs in wallet: ' + str(BTC_q))
        print('---------------')
        print(' ')




print('-------------------------------------------------')
print('times bought: ' + str(buy_q))
print('times sold: ' + str(sell_q))
print('BTC quantity: ' + str(BTC_q))
print('dollars: ' + str(dollars))
print('total in dolars: ' + str(dollars + BTC_q * float(klines[-1][4])))
print('profit: ' + str(10000 + (dollars + BTC_q * float(klines[-1][4]))))
print('')
print('buy and hold: ' + str(hold))
print('comparison: ' + str(dollars-hold))
