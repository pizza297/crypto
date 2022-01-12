import pandas as pd
import pytz
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()
from pycoingecko import CoinGeckoAPI

TS_SCALAR = 1000000
TS_SCALAR_1 = 1000000000
MAX_DAYS_FOR_HOURLY_DATA = 90

cg = CoinGeckoAPI()
VS_CURRENCY = 'usd'


def convert_ts(ts: datetime.datetime):
    return str(int(pd.Timestamp(ts).value / TS_SCALAR_1))


def get_prices(id: str, start_ts: datetime.datetime, end_ts: datetime.datetime):
    prices = cg.get_coin_market_chart_range_by_id(id=id,
                                                  vs_currency=VS_CURRENCY,
                                                  from_timestamp=convert_ts(start_ts),
                                                  to_timestamp=convert_ts(end_ts))

    df_prices = pd.DataFrame(data=prices['prices'], columns=['ts', id])
    df_prices['ts'] = pd.to_datetime(df_prices['ts'] * TS_SCALAR)
    return df_prices


def get_lookback_data(id: str, ts: datetime.datetime):
    start_ts = ts - pd.Timedelta(days=MAX_DAYS_FOR_HOURLY_DATA)
    return get_prices(id=id, start_ts=start_ts, end_ts=ts)


def get_all_market_data(id: str, start_ts: datetime.datetime, end_ts: datetime.datetime):
    data_start_ts = end_ts
    df_list = []
    while data_start_ts >= start_ts:
        this_market_data = get_lookback_data(id=id, ts=data_start_ts)
        df_list.append(this_market_data)
        data_start_ts -= pd.Timedelta(days=MAX_DAYS_FOR_HOURLY_DATA)
    df_all_data = pd.concat(df_list).sort_values('ts')
    return df_all_data[df_all_data['ts'] > pd.to_datetime(start_ts)]


def get_md_for_coins(coins, start_ts, end_ts):
    df_list = []
    if not isinstance(coins, list):
        coins = [coins]

    for coin in coins:
        this_coin_data = get_all_market_data(id=coin, start_ts=start_ts, end_ts=end_ts).set_index('ts')
        print(this_coin_data)
        df_list.append(this_coin_data)

    return pd.concat(df_list, axis=1).resample('1H').last()


if __name__ == "__main__":
    window_size = 24 * 7
    id_list = ['bitcoin', 'ethereum', 'solana']

    end_ts = pd.Timestamp.now()
    # end_ts = pd.Timestamp('12/18/2021')
    end_ts = end_ts.tz_localize(tz='US/Central').tz_convert(tz='utc')
    start_ts = end_ts - pd.Timedelta(days=MAX_DAYS_FOR_HOURLY_DATA)

    df_all_hourly_data = get_md_for_coins(coins=id_list, start_ts=start_ts, end_ts=end_ts)

    realized_vols_rolling_1w = df_all_hourly_data.pct_change().rolling(window_size).std() * ((24 * 365) ** 0.5) * 100

    plot_start_date = '1/1/2021'
    realized_vols_rolling_1w[plot_start_date:].plot(figsize=(16, 9))
