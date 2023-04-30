import math
import datetime

from flask import request
from sqlalchemy import text

from mysql.config import TABLE_NAME
from mysql.engine import engine

from . import api
from .util import response_decorator


@api.route("/financial_data", methods=["GET"])
@response_decorator
def get_financila_data():
    start_date, end_date, symbol, limit, page = get_params(request.args)
    data_list = query_data(start_date, end_date, symbol, limit, page)
    data, count = construct_result(data_list)

    return {
        "data": data,
        "pagination": {
            "count": count,
            "page": page,
            "limit": limit,
            "pages": math.ceil(count/limit)
        }
    }


def get_params(params):
    """
    Read paramters from flask request.

    Args:
        params: flask request paramter, it should be like {
            "start_date": str,  # e.g., "2023-01-01", optional
            "end_date": str,    # e.g., "2023-05-14", optional
            "symbol": str,      # e.g., "IBM", optional
            "limit": int,       # e.g., 3
            "page": int         # e.g., 2
        }
    
    Returns:
        start_date: str,
        end_date: str,
        symbol: str,
        limit: int,
        page: int

    """
    start_date = params.get("start_date")
    end_date = params.get("end_date")
    symbol = params.get("symbol")
    limit = int(params.get("limit", 5))
    page = int(params.get("page", 1))

    return start_date, end_date, symbol, limit, page


def query_data(start_date, end_date, symbol, limit, page):
    """
    Query data from financial table according to the given contiditon.

    Args:
        start_date: str,  # e.g., "2023-01-01", optional
        end_date: str,    # e.g., "2023-05-14", optional
        symbol: str,      # e.g., "IBM", optional
        limit: int,       # e.g., 3
        page: int         # e.g., 2
    
    Returns:
        result: List[tuple]

    """

    sql_str = f"SELECT *, count(*) over() as c FROM {TABLE_NAME} "
    where_condition = ""

    if start_date:
        where_condition += f" date >= '{start_date}' AND "
    if end_date:
        where_condition += f" date <= '{end_date}' AND "
    if symbol:
        where_condition += f" symbol='{symbol}' AND "

    if where_condition:
        where_condition = " WHERE " + where_condition[:-4]
        sql_str += where_condition

    sql_str += " ORDER BY id ASC "
    sql_str += f" LIMIT {limit} OFFSET {limit*(page-1)};"\

    # print("sql_str: ", sql_str)

    select_statement = text(sql_str)

    with engine.connect() as conn:
        result = conn.execute(select_statement).fetchall()

        return result


def construct_result(data_list):
    """
    Convert sql result to the format of api response 

    Args:
        data_list: List[tuple], it should be like [
        (id, symbol, date, open_price, close_price, volume, count)
        ]
    
    Returns:
        result: List[Dict], it should be like {
                "symbol": str,
                "date": str,
                "open_price": str,
                "close_price": str,
                "volume": str,
            }
        count: int, count of all records without panigation

    """
    count = 0
    result = []
    for data in data_list:
        date: datetime.date = data[2]
        
        result.append(
            {
                "symbol": data[1],
                "date": date.strftime("%Y-%m-%d"),
                "open_price": str(data[3]),
                "close_price": str(data[4]),
                "volume": str(data[5]),
            }
        )
        count = data[6]

    return result, count
