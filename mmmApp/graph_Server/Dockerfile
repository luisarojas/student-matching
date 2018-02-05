#Set base image
FROM python

MAINTAINER Guilherme <guilherme.damasio@uoit.net>

#set env variables
ENV DB_PSWD = mmmPassForGraphServer
ENV DB_USER = mmmServerUser
ENV DB_HOST = graph_db

COPY mmm_graph_server .

RUN pip install -r requirements.txt
ENTRYPOINT ["python", "graph_server.py"]
