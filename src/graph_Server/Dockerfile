#Set base image
FROM python

#set env variables
ENV DB_PSWD = mmmPassForGraphServer
ENV DB_USER = mmmServerUser
ENV DB_HOST = graph_db
ENV SERVER_PORT = 5002

COPY mmm_graph_server .

RUN pip install -r requirements.txt
ENTRYPOINT ["python", "server.py"]
