# Ubiwhere_Challenge

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/8b53fffa7400419e9acea1b6518163ac)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tomas99batista/Ubiwhere_Challenge&amp;utm_campaign=Badge_Grade)

## Initial Data

### Users

#### Superuser
user: 'admin'
pwd: 'admin'

#### Normaluser
user: 'usertestecreator'
pwd: 'usertestecreator'

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
