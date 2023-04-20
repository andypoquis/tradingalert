from binance.client import Client
import csv
from datetime import datetime
# Reemplaza "api_key" y "api_secret" con tus propias claves de API de Binance
client = Client("mXI5zUpUWSliqhy2gO3rG8VIKAfbfDtdFX4m0A5YV0mb6QSUjqrSObuIqjF9yR2J", "rFjTrv85H0UrbWTD5JkcRc1r4VsX6NodzhLLfZRaUOqBZfmf0WgOyQbfl3ZWTEoK")

# El símbolo del par de divisas que quieres consultar (por ejemplo, "BTCUSDT")
symbol = "BTCUSDT"
klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_5MINUTE, "10 year ago UTC")

with open('klines_'+symbol+'_5m.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    for kline in klines:
        writer.writerow(kline)