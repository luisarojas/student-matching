#Set base image
FROM postgres

MAINTAINER Guilherme <guilherme.damasio@uoit.net>

#set schema
ENV POSTGRES_DB mmm_auth_db

#Save script in order to create the DB/Tables
COPY mmm_schema.sh /docker-entrypoint-initdb.d/
