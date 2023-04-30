# Project Description

This project provides simple APIs to query the stock price trends and statistics of a given company.

## Table of contents
* [Tech Stack](#tech-tack)
* [Usage](#usage)
* [Discussion](#discussion)


## Tech Stack
Project is created with:
* Git: Version control
* Docker: Package and deploy application
* Flask: API Service
* SqlAlchemy + MySQL: Data persistence

```
python_assignment
│  docker-compose.yml
│  Dockerfile                  # dockerfile for api service
│  get_raw_data.py             # get raw financial data and store them in database
│  README.md
│  README_N.md
│  requirements.txt            # dependencies
│  schema.sql                  # sql statement for create financial_data table
│
└─financial
    │  app.py                  # flask app entrance
    │  __init__.py
    │
    ├─api                      # api entrance
    │      financial_data.py   # financial data query api
    │      statistics.py       # financial statistics query api
    │      util.py             # error handling decorator
    │      __init__.py
    │
    ├─mysql                    # database abstraction for python
    │      config.py           # mysql config file
    │      engine.py           # sqlalchemy engine
    │      __init__.py
    │
    └─test                     # tests for apis
            financial_data_test.py # tests for functions in financial_data module
            statistics_test.py     # tests for functions in statistics module
            __init__.py
```
### Dependencies
```bash
requests     # requests is one of most popular python libraries to send http requests, so we choose to use it. 
flask        # Light weighted and popular web framework
PyMySQL      # Dependency of sqlalchemy
cryptography # Used for mysql connection
sqlalchemy   # Efficient and high-performing python database toolkit. We can use it to connect mysql and execute sql statements.
```

## Usage
1. Launch the api service and mysql in docker. The database and table used to store stock price information will be automatically created.
```bash
$ docker-compose up           
```
2. After launch, the database table is empty, so we should retrieve some stock data from API provided by AlphaVantage and store them in local db.
```
$ python get_raw_data.py       
```
3. Then, we can query data through APIs.
```bash
# HOST: http://localhost:5000

# Financial data API
# path: /api/financial_data
# method: GET
# request:
# {
#     "start_date": str,  # e.g., "2023-01-01", optional
#     "end_date": str,    # e.g., "2023-05-14", optional
#     "symbol": str,      # e.g., "IBM", optional
#     "limit": int,       # e.g., 3
#     "page": int         # e.g., 2
# }
# response:
# {
#     "data": [
#         {
#             "symbol": str,
#             "date": str,
#             "open_price": str,
#             "close_price": str,
#             "volume": str,
#         }
#     ],
#     "pagination": {
#         "count": int,
#         "page": int,
#         "limit": int,
#         "pages": int
#     },
#     "info": {'error': ''}
# }
# example:
curl -X GET 'http://localhost:5000/api/financial_data?start_date=2023-01-01&end_date=2023-05-14&symbol=IBM&limit=3&page=2'


# Financial statistics API
# path: /api/statistics
# method: GET
# request:
# {
#     "start_date": str,  # e.g., "2023-01-01"
#     "end_date": str,    # e.g., "2023-05-14"
#     "symbol": str,      # e.g., "IBM"
# }
# response:
# {
#     "data": [
#         {
#           "start_date": str,
#           "end_date": str,
#           "symbol": str,
#           "average_daily_open_price": float,
#           "average_daily_close_price": float,
#           "average_daily_volume": int
#         }
#     ],
#     "pagination": {
#         "count": int,
#         "page": int,
#         "limit": int,
#         "pages": int
#     },
#     "info": {'error': ''}
# }
# example:
curl -X GET 'http://localhost:5000/api/statistics?start_date=2023-01-01&end_date=2023-05-31&symbol=IBM'

```

## Discussion
API key storage method:
### Local development

Directly hard-coded in the python file.

### Production environment 
