FROM python:3.6
ADD . /home/
WORKDIR /home/
RUN pip install -r requirements.txt
CMD python ./src/www/server.py
