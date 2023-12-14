FROM docker.io/postgres:16

ENV POSTGRES_PASSWORD=chandlerb

COPY ./create_tables.sql /docker-entrypoint-initdb.d/
