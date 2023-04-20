import pandas as pd
import talib
import matplotlib.pyplot as plt
import telebot

bot_token = '6201417182:AAHUuh597R8OadUvDqlgcTfLVUA7gLRLa1I'
group_id = '@tradingandypoquis'
bot = telebot.TeleBot(bot_token)

# Cargar datos del archivo CSV
df = pd.read_csv('klines_BTCUSDT_5m.csv')
df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')   
df['close'] = df['close'].astype(float)

# Definir parámetros para Ichimoku
conversion_line_period = 9
base_line_period = 26
lagging_span_period = 52
displacement = 26

# Calcular Ichimoku Cloud
conversion_line = talib.EMA(df['close'], timeperiod=conversion_line_period)
base_line = talib.EMA(df['close'], timeperiod=base_line_period)
lead_span_a = ((conversion_line + base_line) / 2).shift(displacement)
lead_span_b = talib.EMA(df['close'], timeperiod=lagging_span_period).shift(displacement)

# Definir parámetros para STOCH
stoch_period = 14
stoch_slowing_period = 1

# Calcular STOCH
stoch_k, stoch_d = talib.STOCH(df['high'], df['low'], df['close'], fastk_period=stoch_period, slowk_matype=0, slowd_period=stoch_slowing_period, slowd_matype=0)

# Definir parámetros para MACD
macd_fast_period = 12
macd_slow_period = 26
macd_signal_period = 9

# Calcular MACD
macd, macd_signal, _ = talib.MACD(df['close'], fastperiod=macd_fast_period, slowperiod=macd_slow_period, signalperiod=macd_signal_period)

# Implementar estrategia de trading
positions = []
for i in range(len(df)):
    if lead_span_a[i] > lead_span_b[i] and lead_span_a[i-1] <= lead_span_b[i-1] and stoch_k[i] > 0.2 and macd[i] > macd_signal[i] and macd[i-1] <= macd_signal[i-1]:
        positions.append('long')
    elif lead_span_a[i] < lead_span_b[i] and lead_span_a[i-1] >= lead_span_b[i-1]:
        positions.append('exit')
    elif lead_span_a[i] < lead_span_b[i] and lead_span_a[i-1] <= lead_span_b[i-1]:
        positions.append('wait')
    elif lead_span_a[i] > lead_span_b[i] and lead_span_a[i-1] <= lead_span_b[i-1] and stoch_k[i] > 0.9 and macd[i] < macd_signal[i] and macd[i-1] >= macd_signal[i-1]:
        positions.append('exit')
    else:
        positions.append('hold')

# Agregar posiciones al DataFrame
df['position'] = positions
today = pd.Timestamp.today()
limit_date = today - pd.Timedelta(days=7)
df_filtered = df[df['timestamp'] >= limit_date]

# Crear las figuras y los ejes
fig1, ax1 = plt.subplots(figsize=(30,10))
fig2, ax2 = plt.subplots(figsize=(30,10))
fig3, ax3 = plt.subplots(figsize=(30,10))


ax1.plot(df_filtered['timestamp'], df_filtered['close'], label='Precio')
ax1.legend()

buy_signals = df_filtered[df_filtered['position'] == 'long']
sell_signals = df_filtered[df_filtered['position'] == 'exit']
wait_signals = df_filtered[df_filtered['position'] == 'wait']
ax1.scatter(buy_signals['timestamp'], buy_signals['close'], marker='^', color='green', s=100, label='Compra')
ax1.legend()

ax2.plot(df_filtered['timestamp'], df_filtered['close'], label='Precio')
ax2.scatter(sell_signals['timestamp'], sell_signals['close'], marker='v', color='red', s=100, label='venta')
ax2.legend()

ax3.plot(df_filtered['timestamp'], df_filtered['close'], label='Precio')
ax3.scatter(wait_signals['timestamp'], wait_signals['close'], marker='v', color='yellow', s=100, label='esperar')
ax3.legend()

# Guardar las figuras en archivos png
fig1.savefig('compra.png')
fig2.savefig('venta.png')
fig3.savefig('esperar.png')

# Enviar las imágenes al grupo
with open('compra.png', 'rb') as f:
    bot.send_photo(group_id, f)
with open('venta.png', 'rb') as f:
    bot.send_photo(group_id, f)
with open('esperar.png', 'rb') as f:
    bot.send_photo(group_id, f)