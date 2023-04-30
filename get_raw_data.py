from typing import Dict, List
import requests
from datetime import datetime, timedelta

from sqlalchemy import text
from financial.mysql.engine import engine
from financial.mysql.config import TABLE_NAME


SYMBOL_LIST = ["IBM", "AAPL"]
API_KEY = "FP2YERP92EYOGLET"
API = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&apikey={API_KEY}"



def get_two_weeks_data(symbol: str) -> List[Dict]:
    """
    hhh
    """
    result = []
    date_limit = datetime.today() - timedelta(days=14)

    resp = requests.get(API, params={"symbol": symbol})
    resp.raise_for_status()
    time_series_data = resp.json().get("Time Series (Daily)", {})

    for date_str, data in time_series_data.items():
        date = datetime.strptime(date_str, "%Y-%m-%d")
        if date < date_limit:
            break

        data = {
            "symbol": symbol,
            "date": date_str,
            "open_price": data["1. open"],
            "close_price": data["4. close"],
            "volume": data["6. volume"],
        }

        result.append(data)

    result.reverse()

    for data in result:
        save_to_db(data)

    # For Debug
    print(f"get_raw_data size: {len(result)}, result: {result}")

    return result


def save_to_db(data: Dict):
    """
    First, query whether the data has already existed in the database, 
    and then insert or update the database table

    Args:
        data: data to be upserted, it should be like {
            "symbol": "IBM",
            "date": "2023-04-30",
            "open_price": "166.6",
            "close_price": "166.6",
            "volume": "1111111",
        }
    
    Returns:
        None

    """

    date = data["date"]
    symbol = data["symbol"]
    open_price = data["open_price"]
    close_price = data["close_price"]
    volume = data["volume"]

    select_str = f"SELECT * FROM {TABLE_NAME} WHERE symbol='{symbol}' AND date='{date}';"
    insert_str = f"INSERT INTO {TABLE_NAME} (symbol, date, open_price, close_price, volume) " \
                 f"VALUES('{symbol}', '{date}', {open_price}, {close_price}, {volume});"
    update_str = f"UPDATE {TABLE_NAME} " \
                 f"SET symbol='{symbol}', date='{date}', open_price={open_price}, close_price={close_price}, volume={volume} " \
                 "WHERE id={primary_id};"

    with engine.connect() as conn:
        primary_id = -1
        result = conn.execute(text(select_str)).fetchone()

        if result:
            primary_id = result[0]
            # if we can find an existing record by symbol and date,
            # and its open_price, close_price and volume all equal to those of data, 
            # we think data is duplicated and should return.
            if str(result[3]) == open_price and str(result[4]) == close_price and str(result[5]) == volume:
                return

        if primary_id < 0:
            conn.execute(text(insert_str), data)
        else:
            conn.execute(text(update_str.format(primary_id=primary_id)), data)
        conn.commit()


if __name__ == "__main__":
    for symbol in SYMBOL_LIST:
        get_two_weeks_data(symbol)
