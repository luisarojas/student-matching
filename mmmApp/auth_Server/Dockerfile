#Set base image
FROM python

MAINTAINER Guilherme <guilherme.damasio@uoit.net>

#set env variables
ENV DB_PORT = 5432
ENV DB_NAME = mmm_jwt_auth
ENV DB_PSWD = mmmPassForServer
ENV DB_USER = mmmServerUser
ENV DB_HOST = auth_db

COPY mmm_auth_server .

RUN pip install -r requirements.txt
ENTRYPOINT ["python", "manage.py", "runserver", "-h", "0.0.0.0", "-p", "5000"]
