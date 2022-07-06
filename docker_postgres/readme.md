docker build -t test:pandas .

docker run -it test:pandas


docker run -it \
    -e POSTGRES_USER='root' \
    -e POSTGRES_PASSWORD='root' \
    -e POSTGRES_DB='ny_taxi' \
    -v ~$(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:13



docker run -it \
    -e PGADMIN_DEFAULT_EMAIL='admin@admin.com' \
    -e PGADMIN_DEFAULT_PASSWORD='root' \
    -p 8080:80 \
    dpage/pgadmin4


# note create network for connection between postgresql db and pgadmin
docker network create pg-network

docker run -it \
    -e POSTGRES_USER='root' \
    -e POSTGRES_PASSWORD='root' \
    -e POSTGRES_DB='ny_taxi' \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database \
    postgres:13

docker run -it \
    -e PGADMIN_DEFAULT_EMAIL='ngthnoi00@gmail.com' \
    -e PGADMIN_DEFAULT_PASSWORD='root' \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4

# convert ipynb to script py
jupyter nbconvert --to=script upload_data.ipynb

#run python script

python3 ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_data \
    --url=https://s3.amazonaws.com/nyc-tlc/csv_backup/yellow_tripdata_2021-01.csv \


docker build -t taxi_ingest:v001 .

docker run -it taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_data \
    --url=https://s3.amazonaws.com/nyc-tlc/csv_backup/yellow_tripdata_2021-01.csv \


# set up network for docker digestion to have it faster
docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
        --user=root \
        --password=root \
        --host=pg-database \
        --port=5432 \
        --db=ny_taxi \
        --table_name=yellow_taxi_data \
        --url=https://s3.amazonaws.com/nyc-tlc/csv_backup/yellow_tripdata_2021-01.csv \

