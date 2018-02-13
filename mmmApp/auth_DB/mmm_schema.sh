#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --set=newuser="$DB_USER" --set=newuserpswd="'""$DB_PSWD""'" --set=newdbname="$DB_NAME"<<-EOSQL
    CREATE ROLE :'newuser' superuser;
    CREATE USER :'newuser';
    ALTER USER :'newuser' with encrypted password :'newuserpswd';
    CREATE DATABASE :'newdbname';
    GRANT ALL PRIVILEGES ON DATABASE :'newdbname' TO :'newuser';

    \connect :'newdbname';

    CREATE TABLE users(
    	ID 		BIGSERIAL PRIMARY KEY	NOT NULL,
	EMAIL		CHAR(255)		UNIQUE NOT NULL,
	PASSWORD	CHAR(255)		NOT NULL,
	REGISTERED_ON	TIMESTAMP		NOT NULL,
	ADMIN		BOOLEAN			NOT NULL	DEFAULT FALSE
    );
    
    CREATE TABLE blacklist_tokens(
	ID		BIGSERIAL PRIMARY KEY	NOT NULL,
	TOKEN		CHAR(500)		UNIQUE NOT NULL,
	BLACKLISTED_ON	TIMESTAMP		NOT NULL
    );
EOSQL
