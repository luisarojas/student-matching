FROM python:3.6
ADD ./requirements.txt /home/requirements.txt
WORKDIR /home/
RUN pip install -r requirements.txt
ADD ./ /home/
CMD python ./src/www/server.py
