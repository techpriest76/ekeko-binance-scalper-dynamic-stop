# ekeko-binance-scalper-dynamic-stop
easy money win win

How does it work?

The script will check the price for every coin listed in the 'pair' list, (details in the code commentaries).
Then will excecute a buy when if it is a 2% lower than the MA50 price and if it's in a uptrend, then put a selling order at 4% higher.
It will HODL the currency untill it gets 1% below the selling price, when this happens it will put a new selling order 1% above the original limit
and a stop_loss 1% below the current price.
If the price continues to go up, it will repeat the process aiming always for the higher selling price, when the prices starts to go down
(after a peak) it will reach the stop_limit price and sell the currency, this way it assures that we sell at the highest prices we can.
