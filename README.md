# Ubiwhere_Challenge

![Django CI](https://github.com/tomas99batista/Ubiwhere_Challenge/workflows/Django%20CI/badge.svg)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/8b53fffa7400419e9acea1b6518163ac)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tomas99batista/Ubiwhere_Challenge&amp;utm_campaign=Badge_Grade)

# Table of Contents  
-  [Introduction](#Introduction)
-  [Endpoints](#Endpoints)
-  [Initial Data](#Initial_Data)
-  [Installation](#Installation)
-  [Tests](#Tests)
-  [Documentation](#Documentation)
-  [Swagger](#Swagger)
-  [Postman Collection](#Postman)
-  [Continuous Integration](#CI)
-  [Author](#Author)

## Introduction
This challenge was proposed by [Ubiwhere](https://www.ubiwhere.com/) to their backend-dev position. 
Developed in Python/Django, with the support of Django Rest Framework, JWT, Postgres + Postgis and Docker.
It's an API to manage Occurrences.

## Endpoints

### API Occurrence URLS
-  **POST**: Add Occurrence
    - `<ip_addr>:8000/api/occurrence/`

-   **PATCH**: Update state of Occurrence(occurrence_id=pk)
-   **DELETE**: Delete Occurrence(occurrence_id=pk)
-   **GET**: Get Occurrence(occurrence_id=pk)
    -  `<ip_addr>:8000/api/occurrence/<int:pk>/`

-  **GET**: Filter Occurrences by author/caregory/distance to given point
    -  `<ip_addr>:8000/api/occurrence/filter/`


-  **GET**: Get All Occurrences
    -  `<ip_addr>:8000/api/occurrence/all/`

### Auth URLS
-  **POST**: Login - Retrieves Auth Token
    -  `<ip_addr>:8000/api/login/`

-  **POST**: Register - Creates new User
    -  `<ip_addr>:8000/api/register/`


-  **GET**: Get All Users
    -  `<ip_addr>:8000/api/users/all/`


-  **GET**: Get User by ID
-  **DELETE**: Delete User by ID
    -  `<ip_addr>:8000/api/user/<int:pk>/`


### Index (Endpoints table)
-  `<ip_addr>:8000/`
![EndPoints](https://i.imgur.com/jqPmvPY.png)

## Initial_Data
You can always access `<ip_addr>:8000/admin/` to see the data.

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

## Installation

__Requirements to run__: Have `docker` & `docker-compose` installed.

### Clone the repository
Clone this repo to your local machine using https://github.com/tomas99batista/Ubiwhere_Challenge.git

### Run containers
`docker-compose up -d --build`

### Clean containers
`docker-compose down -v`

## Swagger
There is a swagger available on `<ip_addr>:8000/swagger/`. 
In order to test the endpoints (as a normal_user or as a super_user), you first must obtain the Auth Token by logging in (using the endpoint on Swagger) and then go to "Authorize", insert the the token, saving as: `Bearer <Token>`, as seen on image:

![Saving Auth Token](https://i.imgur.com/bK2SlLh.png)

## Postman
With the docker-compose running you can now test the endpoints with the given collection of Postman.

*URL*: <https://documenter.getpostman.com/view/9124304/TVKHVaue>

It's possible to select between 2 environments: `admin_environment`, where the user is a superuser and, therefore, can DELETE and PATCH; and `normal_user_environment`, where the access is limited to DELETE and PATCH.

![Postman](https://i.imgur.com/pdAQMnO.png)

## Tests
There are 2 types of tests: tests to the Occurence model (`tests/test_models.py`) and to the API views (`tests/test_views.py`).

## Documentation
Available on `ubiwhere_challenge/docs/` there is documentation for the `models`, `serializers`, `views` and `urls`.

## CI
There is an workflow checking if build state on every commit to master. It can be seen on <https://github.com/tomas99batista/Ubiwhere_Challenge/actions>

## Author
Thank you,
[Tomás Batista](https://github.com/tomas99batista)
