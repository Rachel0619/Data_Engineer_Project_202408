
import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
from time import time
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    file_name = url.split('/')[-1]

    os.system(f"wget {url} -O {file_name}")

    if file_name.endswith('.parquet'):
        parquit_file = pd.read_parquet(file_name)
        parquit_file.to_csv('yellow_trip_data.csv')
        df = pd.read_csv('yellow_trip_data.csv')
        df_iter = pd.read_csv('yellow_trip_data.csv', iterator=True, chunksize=100000)
    elif file_name.endswith('.csv'):
        df = pd.read_csv(file_name)
        df_iter = pd.read_csv(file_name, iterator=True, chunksize=100000)
    else:
        raise ValueError("Unsupported file format")

    # download the csv
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    df.head(0).to_sql(name=table_name, con=engine, if_exists="replace")

    while True:
        try:
            t_start = time()
            df_chunk = next(df_iter)
            df_chunk.to_sql(name=table_name, con=engine, if_exists="append")
            t_end = time()
            print("inserted another chunk..., took %.3f second" % (t_end-t_start))
        except StopIteration:
            print(f"Ingestion complete for {table_name}")
            break

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Ingest csv data to Postgres')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the result to')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()
    main(args)

