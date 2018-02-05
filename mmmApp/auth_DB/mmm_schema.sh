#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE ROLE mmmServerUser superuser;
    CREATE USER mmmServerUser;
    ALTER USER mmmServerUser with encrypted password 'mmmPassForServer';
    CREATE DATABASE mmm_jwt_auth;
    GRANT ALL PRIVILEGES ON DATABASE mmm_jwt_auth TO mmmServerUser;

    \connect mmm_jwt_auth;

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
