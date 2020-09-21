# Ubiwhere_Challenge

## How to install

`$ virtualenv -p python3 venv`

`$ source ./venv/bin/activate`

`$ pip3 install -r requirements.txt`

## Docker

### Build Compose 
`docker-compose build`

### Run Compose
`docker-compose up -d`

### Criar Postgres DB

` docker run --name postgis_ubi_chall -d -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -d postgis/postgis`
