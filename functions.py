from binance.spot import Spot
import database


def get_balances(symbol_money: str, net: Spot):
    balance = net.account().get('data').get('balances')
    for i in balance:
        if i.get('asset') == symbol_money:
            return i


def get_balances_test(symbol_money: str, net: Spot):
    for i in net.account()['balances']:
        if i.get('asset') == symbol_money:
            return i


def search_pairs(symbol_money: str, net: Spot, wallet: float) -> list:
    counter = 1
    result_list = net.ticker_price().get('data')
    for i in range(len(result_list)):
        for j in range(len(result_list)):
            for k in range(len(result_list)):
                first_pair_price = float(result_list[i]['price'])
                second_pair_price = float(result_list[j]['price'])
                third_pair_price = float(result_list[k]['price'])

                first_pair_symbol = str(result_list[i]['symbol'])
                second_pair_symbol = result_list[j]['symbol']
                third_symbol_currency = result_list[k]['symbol']

                first_symbol_currency = first_pair_symbol.replace(symbol_money, '')
                third_symbol_currency = third_symbol_currency.replace(symbol_money, '')

                if symbol_money in first_pair_symbol and\
                        symbol_money in third_symbol_currency and\
                        third_symbol_currency in second_pair_symbol and\
                        first_symbol_currency in second_pair_symbol and\
                        (len(third_symbol_currency) + len(first_symbol_currency)) == len(second_pair_symbol) and\
                        first_pair_symbol != third_symbol_currency:

                    if first_pair_symbol.rfind(symbol_money):
                        percent = wallet / first_pair_price / 100 * 0.1
                        res = wallet / first_pair_price - percent
                        print(counter, wallet, '/', first_pair_symbol, end=' ')
                    else:
                        percent = wallet / first_pair_price / 100 * 0.1
                        res = wallet * first_pair_price - percent
                        print(counter, wallet, '*', first_pair_symbol, end=' ')
                    if second_pair_symbol.rfind(first_symbol_currency):
                        percent = res / second_pair_price / 100 * 0.1
                        res = res / second_pair_price - percent
                        print('/', second_pair_symbol, end=' ')
                    else:
                        percent = res / second_pair_price / 100 * 0.1
                        res = res * second_pair_price - percent
                        print('*', second_pair_symbol, end=' ')
                    if third_symbol_currency.rfind(symbol_money):
                        percent = res / third_pair_price / 100 * 0.1
                        res = res * third_pair_price - percent
                        print('*', third_symbol_currency, f'{first_pair_price}, {second_pair_price}, {third_pair_price}')
                    else:
                        percent = res / third_pair_price / 100 * 0.1
                        res = res / third_pair_price - percent
                        print('/', third_symbol_currency, f'{first_pair_price}, {second_pair_price}, {third_pair_price}')

                    sym = f"{first_pair_symbol}->{second_pair_symbol}->{third_symbol_currency}"
                    print(counter, sym, res)
                    print()
                    counter = counter + 1
                    result_list.append(f"{first_pair_symbol}-{second_pair_symbol}-{third_symbol_currency}")
    return result_list


def get_price_pairs(symbol_currency: str, net: Spot, wallet: float):
    counter = 0
    temp_result_list = []
    result_list = []
    price_list = net.book_ticker().get('data')

    for pairs in database.get_pair(symbol_currency):
        first_currency_symbol = ''
        second_currency_symbol = ''

        first_pair_symbol = pairs.split('-')[0]
        second_pair_symbol = pairs.split('-')[1]
        third_pair_symbol = pairs.split('-')[2]

        if first_pair_symbol != second_pair_symbol and \
                first_pair_symbol != third_pair_symbol and \
                third_pair_symbol != second_pair_symbol and \
                first_pair_symbol.startswith(symbol_currency) or \
                first_pair_symbol.endswith(symbol_currency) and \
                second_pair_symbol.startswith(first_currency_symbol) or \
                second_pair_symbol.endswith(first_currency_symbol) and \
                symbol_currency in third_pair_symbol and \
                second_currency_symbol in third_pair_symbol:

            first_currency_symbol = first_pair_symbol.replace(symbol_currency, '')
            second_currency_symbol = second_pair_symbol.replace(first_currency_symbol, '')

            while len(temp_result_list) != 3:
                for i in range(len(price_list)):
                    bid_price = float(price_list[i]['bidPrice'])
                    ask_price = float(price_list[i]['askPrice'])
                    symbol = price_list[i]['symbol']
                    if symbol == first_pair_symbol and bid_price != 0.0 and ask_price != 0.0:
                        temp_result_list.insert(0, [bid_price, ask_price])
                    if symbol == second_pair_symbol and bid_price != 0.0 and ask_price != 0.0:
                        temp_result_list.insert(1, [bid_price, ask_price])
                    if symbol == third_pair_symbol and bid_price != 0.0 and ask_price != 0.0:
                        temp_result_list.insert(2, [bid_price, ask_price])
                    if len(temp_result_list) == 3:
                        break

            if first_pair_symbol.endswith(symbol_currency):
                percent = wallet / float(temp_result_list[0][0]) / 100 * 0.075
                res = wallet / float(temp_result_list[0][0]) - percent
            else:
                percent = wallet * float(temp_result_list[0][1]) / 100 * 0.075
                res = wallet * float(temp_result_list[0][1]) - percent

            if second_pair_symbol.endswith(first_currency_symbol):
                percent = res / float(temp_result_list[1][0]) / 100 * 0.075
                res = res / float(temp_result_list[1][0]) - percent
            else:
                percent = res * float(temp_result_list[1][1]) / 100 * 0.075
                res = res * float(temp_result_list[1][1]) - percent

            if third_pair_symbol.endswith(second_currency_symbol):
                percent = res / float(temp_result_list[2][0]) / 100 * 0.075
                res = res / float(temp_result_list[2][0]) - percent
                result_list.append([res, f'{first_pair_symbol}, {second_pair_symbol}, {third_pair_symbol}'])
            else:
                percent = res * float(temp_result_list[2][1]) / 100 * 0.075
                res = res * float(temp_result_list[2][1]) - percent
                result_list.append([res, f'{first_pair_symbol}, {second_pair_symbol}, {third_pair_symbol}'])

        temp_result_list.clear()

    result_list.sort()
    result_list.reverse()

    for i in result_list:
        print(counter, i)
        counter = counter + 1
