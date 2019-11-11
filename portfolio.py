from yahoo_fin import stock_info as si
import pandas as pd

# we are injecting capital into portfolio but aren't sure how to allocate
# it amongst our assets
deposit = 100000

# symbols of desired assets
symbols = [
    "AAPL",
    "AMZN",
    "MSFT",
    "JPM"
]

# desired weighting of the symbols above
desired_weights = [
    10,
    15,
    8,
    5
]

share_prices = [si.get_live_price(sym) for sym in symbols]

price_lookup = {}
sum_weights = sum(desired_weights)
for i in range(len(desired_weights)):
    desired_weights[i] /= sum_weights
    price_lookup[symbols[i]] = share_prices[i]

data = list(zip(symbols, share_prices, desired_weights))
data = sorted(data, key=lambda x: -x[1])

min_price = data[-1][1]
res = []

full_pcts = [d[2] for d in data]


def dfs(dep, cash, index, path, total):
    if index == len(data):
        if dep - total < min_price:
            path.append(total)
        res.append(path)
        return
    (stock, price, _) = data[index]
    denom = sum(full_pcts[index:]) if sum(full_pcts[index:]) != 0 else 1
    pct = full_pcts[index] / denom
    desired = cash * pct
    low_shares = int(desired // price)
    high_shares = low_shares + 1
    for shares in [low_shares, high_shares]:
        if cash - shares*price >= 0:
            dfs(dep, cash - shares*price, index+1, path + [(stock, shares)], total + shares*price)

dfs(deposit, deposit, 0, [], 0)

res = sorted(res, key=lambda x: -x[-1])

for option in res:
    amount_invested = option[-1]
    investment_ratio = amount_invested/deposit
    option.pop()

    print("\nINVESTED         :   {:.2f}".format(amount_invested))
    print("INVESTMENT RATIO :   {:.2%}\n".format(investment_ratio))
    df = pd.DataFrame(option, columns=['Symbol', 'Quantity'])
    df['PPS'] = df['Symbol'].map(lambda x: price_lookup[x])
    df['Total Price'] = df['Quantity'] * df['PPS']
    df['Portfolio Pct.'] = df['Total Price'] / amount_invested

    for col in ['PPS', 'Total Price']:
        df[col] = df[col].map(lambda x : "{:.2f}".format(x))
    df['Portfolio Pct.'] = df['Portfolio Pct.'].map(lambda x : "{:.2%}".format(x))

    print(df.to_string(index=False))
    print("\n")
    print("-" * 100)
