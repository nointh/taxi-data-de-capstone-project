import pandas as pd
from time import time
from sqlalchemy import create_engine
import argparse
import os

def ingest(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    csv_name = 'output.csv'

    os.system(f'wget {url} -O {csv_name}')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'] )
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'] )

    df.to_sql(name=table_name, con=engine, if_exists='replace')

    while True:
        df = next(df_iter)
        t_start = time()
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'] )
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'] )
        df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
        t_end = time()
        print('Insert another chunk, took %.3f seconds' % (t_end-t_start))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest csv dataset to database")

    parser.add_argument('--user', help='Username for postgresql')
    parser.add_argument('--password', help='Password for postgresql')
    parser.add_argument('--host', help='Host for postgresql')
    parser.add_argument('--port', help='Port for postgresql')
    parser.add_argument('--db', help='Database name for postgresql')
    parser.add_argument('--table_name', help='Table name for postgresql')
    parser.add_argument('--url', help='URL that need for download for csv dataset')
    args = parser.parse_args()
    ingest(args)