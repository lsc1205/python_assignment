import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.statistics import query_data, get_params

if __name__ == "__main__":
    test_data_list = [
        {
            "start_date": "2023-01-27",
            "end_date": "2023-04-27",
            "symbol": "IBM"
        },
        {
            "start_date": "",
            "end_date": "2023-04-27",
            "symbol": "IBM"
        }
    ]

    for data in test_data_list:
        try:
            data_list = query_data(*get_params(data))
            print(data_list)
        except Exception as e:
            print(e)