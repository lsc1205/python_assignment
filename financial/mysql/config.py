import os

HOST = os.environ.get("MYSQL_HOST", 'localhost')  # read mysql host from environment, default value is localhost
PORT = os.environ.get("MYSQL_PORT", 3306)         # read mysql port from environment, default value is 3306
USERNAME = os.environ.get("MYSQL_USER", 'root')   # read mysql user from environment, default value is root
PASSWORD = os.environ.get("MYSQL_PASSWORD", '123456')  # read mysql password from environment, default value is 123456
DB_NAME = 'python_assignment'
TABLE_NAME = "financial_data"
DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'