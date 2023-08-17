from binance.spot import Spot
from config import API_BINANCE, KEY_BINANCE, SECRET_BINANCE

connect_to_binance = Spot(base_url=API_BINANCE, key=KEY_BINANCE, secret=SECRET_BINANCE, show_header=True)
