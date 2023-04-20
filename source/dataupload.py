from binance.client import Client
import csv
from datetime import datetime
from binance.helpers import date_to_milliseconds
import dateparser
import csv
import dateparser
from binance.client import Client
from binance.exceptions import BinanceAPIException

# Reemplaza "api_key" y "api_secret" con tus propias claves de API de Binance
client = Client("mXI5zUpUWSliqhy2gO3rG8VIKAfbfDtdFX4m0A5YV0mb6QSUjqrSObuIqjF9yR2J", "rFjTrv85H0UrbWTD5JkcRc1r4VsX6NodzhLLfZRaUOqBZfmf0WgOyQbfl3ZWTEoK")

# El símbolo del par de divisas que quieres consultar (por ejemplo, "BTCUSDT")
symbol = "BTCUSDT"

# Obtiene la última fecha registrada en el archivo CSV existente
last_date = None
date_str = 0
try:
    with open('klines_'+symbol+'_5m.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Omitir la primera fila (encabezado)
        for row in reader:
            date_str = row[0]
        try:
            date = dateparser.parse(date_str, settings={'TIMEZONE': 'UTC'})
            timestamp = int(date.timestamp() * 1000)
            if last_date is None or timestamp > last_date:
                last_date = timestamp
        except:
            pass
except FileNotFoundError:
    pass

print("Terminó de analizar")
klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_5MINUTE, "1 day ago UTC")

with open('klines_'+symbol+'_5m.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    if last_date is None:
        writer.writerow(['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    for kline in klines:
        timestamp = int(kline[0])
        if last_date is None or timestamp > last_date:
            writer.writerow(kline)
            last_date = timestamp
            print("Actualizando...")

print("Los datos han sido actualizados exitosamente.")
