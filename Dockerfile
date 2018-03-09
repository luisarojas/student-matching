FROM python:3.6
ADD ./src/ /home/src/
ADD ./python-requirements.txt /home/
WORKDIR /home/
RUN pip install -r python-requirements.txt
CMD python ./src/www/server.py
