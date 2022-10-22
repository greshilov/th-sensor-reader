import os


USERNAME = os.getenv("INFLUXDB_USER")
PASSWORD = os.getenv("INFLUXDB_PASSWORD")
DATABASE = os.getenv("INFLUXDB_DB")
BUCKET = f"{DATABASE}/autogen"
