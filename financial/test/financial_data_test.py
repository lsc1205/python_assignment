import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
import traceback

from api.financial_data import get_params, query_data, construct_result


if __name__ == "__main__":
    test_data_list = [
        {
            "start_date": "",
            "end_date": "2023-04-27",
            "symbol": "IBM",
            "limit": 10,
            "page": 1
        },
        {
            "start_date": "",
            "end_date": "",
            "symbol": "IBM",
            "limit": 5,
            "page": 2
        },
        {
            "start_date": "",
            "end_date": "",
            "symbol": "",
            "limit": 4,
            "page": 2
        },
        {
            "start_date": "",
            "end_date": "",
            "symbol": "",
            "limit": 0,
            "page": 2
        }
    ]

    for data in test_data_list:
        try:
            data_list = query_data(*get_params(data))
            result, count = construct_result(data_list)
            print({
                "data": result,
                "pagination": {
                    "count": count,
                    "page": data["page"],
                    "limit": data["limit"],
                    "pages": math.ceil(count/data["limit"])
                }
            })
        except Exception as e:
            print(e)
            # traceback.print_exc()

