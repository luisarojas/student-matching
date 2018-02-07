#Set base image
FROM python

MAINTAINER Guilherme <guilherme.damasio@uoit.net>

#set env variables
ENV DB_PORT = 5432
ENV DB_NAME = mmm_jwt_auth
ENV DB_PSWD = mmmPassForServer
ENV DB_USER = mmmServerUser
ENV DB_HOST = auth_db
ENV SECRET_KEY = 8\xfdy\x19[\xae;C\x80\xeai\xc1{\xe1\xb76\xfaAsr\xe4\x15\x99\xa6

COPY mmm_auth_server .

RUN pip install -r requirements.txt
ENTRYPOINT ["python", "manage.py", "runserver", "-h", "0.0.0.0", "-p", "5000"]
