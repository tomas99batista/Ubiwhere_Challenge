# Ubiwhere_Challenge

## How to install

`$ python3 -m venv env`

`$ source ./venv/bin/activate`

`$ pip3 install -r requirements.txt`

## Docker

### Build Compose 
`docker-compose build`

### Run Compose
`docker-compose up -d`

### Criar Postgis DB
`docker run --name=postgis -d -e POSTGRES_USER=postgis -e POSTGRES_PASS=postgis -e POSTGRES_DBNAME=postgis -p 5432:5432 kartoza/postgis:9.6-2.4`
