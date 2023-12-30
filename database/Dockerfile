FROM docker.io/postgres:16

COPY ./set_vars.sh /docker-entrypoint-initdb.d/
COPY ./create_tables.sql /docker-entrypoint-initdb.d/