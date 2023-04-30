from flask import request
from sqlalchemy import text

from mysql.config import TABLE_NAME
from mysql.engine import engine

from . import api
from .util import response_decorator


@api.route("/statistics", methods=["GET"])
@response_decorator
def get_statistics():
    start_date, end_date, symbol = get_params(request.args)
    open_avg, close_avg, volume_avg = query_data(start_date, end_date, symbol)
    open_avg = open_avg or 0.0
    close_avg = close_avg or 0.0
    volume_avg = volume_avg or 0

    return {
        "data": {
            "start_date": start_date,
            "end_date": end_date,
            "symbol": symbol,
            "average_daily_open_price": open_avg,
            "average_daily_close_price": close_avg,
            "average_daily_volume": int(volume_avg)
        }
    }


def get_params(params):
    """
    Read paramters from flask request.

    Args:
        params: flask request paramter, it should be like {
            "start_date": str,  # e.g., "2023-01-01"
            "end_date": str,    # e.g., "2023-05-14"
            "symbol": str,      # e.g., "IBM"
        }
    
    Returns:
        start_date: str,
        end_date: str,
        symbol: str

    """
    start_date = params["start_date"]
    end_date = params["end_date"]
    symbol = params["symbol"]

    return start_date, end_date, symbol




def query_data(start_date, end_date, symbol):
    """
    Query data from financial table according to the given contiditon.

    Args:
        start_date: str,  # e.g., "2023-01-01"
        end_date: str,    # e.g., "2023-05-14"
        symbol: str,      # e.g., "IBM"
    
    Returns:
        result: List[tuple]

    """

    sql_str = f"SELECT avg(open_price), avg(close_price), avg(volume) FROM {TABLE_NAME} "
    sql_str += f" WHERE date >= '{start_date}' AND "
    sql_str += f" date <= '{end_date}' AND "
    sql_str += f" symbol='{symbol}';"

    # print("sql_str: ", sql_str)

    select_statement = text(sql_str)

    with engine.connect() as conn:
        result = conn.execute(select_statement).fetchone()

        return result
