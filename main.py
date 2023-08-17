import connect
from functions import get_price_pairs


if __name__ == '__main__':
    get_price_pairs('BUSD', connect.spot_client_test, 48)
