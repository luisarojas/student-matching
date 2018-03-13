#Set base image
FROM postgres

MAINTAINER Guilherme <guilherme.damasio@uoit.net>

#set schema
ENV POSTGRES_DB mmm_auth_db
ENV DB_USER mmmserveruser
ENV DB_PSWD mmmPassForServer
ENV DB_NAME mmm_jwt_auth

#Save script in order to create the DB/Tables
COPY mmm_schema.sh /docker-entrypoint-initdb.d/
