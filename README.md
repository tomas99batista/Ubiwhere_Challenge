# Ubiwhere_Challenge

## Docker

### Build Compose 
`docker-compose build`

### Run Compose
`docker-compose up -d`

`docker-compose up -d --build`

### Clear containers
`docker-compose down -v`

### Run with specific .yml
`docker-compose -f docker-compose.yml up --build`

### Criar Postgis DB
`docker run --name=postgres -d -e POSTGRES_USER=postgres -e POSTGRES_PASS=postgres -e POSTGRES_DBNAME=postgres -p 5432:5432 mdillon/postgis`
