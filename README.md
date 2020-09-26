# Ubiwhere_Challenge

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/8b53fffa7400419e9acea1b6518163ac)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tomas99batista/Ubiwhere_Challenge&amp;utm_campaign=Badge_Grade)

# Table of Contents  
- [Introduction](#Introduction)
- [Endpoints](#Endpoints)
- [Initial Data](#Initial_Data)
- [Documentation](#Documentation)
- [How to run & clear docker-compose](#Running)
- [Postman Collection](#Postman)

## Introduction
This challenge was propused by [Ubiwhere](https://www.ubiwhere.com/) to their backend-dev position. 
Developed in Python/Django, with the support of Django Rest Framework, JWT, Postgres + Postgis, Docker, Gunicorn and Postman.
It's an API to manage Occurrences.

## Endpoints

### API Occurrence URLS
- **POST**: Add Occurrence
    - `<ip_addr>:8000/api/occurrence/`


- **PATCH**: Update state of Occurrence(occurrence_id=pk)
- **DELETE**: Delete Occurrence(occurrence_id=pk)
- **GET**: Get Occurrence(occurrence_id=pk)
    - `<ip_addr>:8000/api/occurrence/<int:pk>/`


- **GET**: Filter Occurrences by author/caregory/distance to given point
    - `<ip_addr>:8000/api/occurrence/filter/`


- **GET**: Get All Occurrences
    - `<ip_addr>:8000/api/occurrence/all/`

### Auth URLS
- **POST**: Login - Retrieves Auth Token
    - `<ip_addr>:8000/api/login/`


- **POST**: Register - Creates new User
    - `<ip_addr>:8000/api/register/`


- **GET**: Get All Users
    - `<ip_addr>:8000/api/users/all/`


- **GET**: Get User by ID
- **DELETE**: Delete User by ID
    - `<ip_addr>:8000/api/user/<int:pk>/`


### Index (Endpoints table)
- `<ip_addr>:8000/`
![EndPoints](https://i.imgur.com/jqPmvPY.png)

## Initial_Data

### Occurrences
`{
  "occurrence_id": 1,
  "description": "Occurence - CONSTRUCTION - initial data, created by a initial user",
  "geographic_location": "POINT(25 -14)",
  "author": 1,
  "state": "To Validate",
  "category": "Construction",
  "creation_timestamp": "2020-09-25T17:06:57.001598Z",
  "update_timestamp": "2020-09-25T17:06:57.001598Z"
}`
  
`{
  "occurrence_id": 2,
  "description": "Occurence - INCIDENT - initial data, created by a initial user",
  "geographic_location": "POINT(23 -13)",
  "author": 1,
  "state": "To Validate",
  "category": "Incident",
  "creation_timestamp": "2020-09-25T17:06:57.001598Z",
  "update_timestamp": "2020-09-25T17:06:57.001598Z"
}`

### Users
**Superuser**
- _Username_: 'admin'
- _Password_: 'admin'

**User**
- _Username_: 'userteste'
- _Password_: 'userteste'

## Documentation
Available on `ubiwhere_challenge/docs/` there is documentation for the `models`, `serializers`, `views` and `urls`

## Running

__Requirements to run__: Have `docker` & `docker-compose` installed. You will also need Postman in order to run the Collection I prepared.

### Run containers
`docker-compose up -d --build`

### Clear containers
`docker-compose down -v`


## Postman
With the docker-compose running you can now test the endpoints with the given collection of Postman.

__URL__: <>
