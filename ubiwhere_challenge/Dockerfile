# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
    # when set to 1 removes prints (stdout)
ENV PYTHONUNBUFFERED 1 

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libc-dev geos-dev

# GDAL
RUN apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/main openssl \
    build-base cmake musl-dev linux-headers
RUN apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing gdal-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]