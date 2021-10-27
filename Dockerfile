FROM python:3-alpine

LABEL author="Marc Duby, Broad Institute"
LABEL description="The Flannick's Lab's TRAPI Genetics KP"

# update the image
RUN apk add --update git
RUN apk add --update bash

# Pull the code from git
RUN mkdir /home/CodeTest       
RUN cd /home/CodeTest 
# RUN git clone -b md_mysql_batch https://github.com/broadinstitute/genetics-kp-dev /home/CodeTest/GeneticsPro
RUN git clone https://github.com/broadinstitute/genetics-kp-dev /home/CodeTest/GeneticsPro
RUN cd /home/CodeTest/GeneticsPro

# install python libraries
RUN pip3 install PyMySQL==0.10.1
RUN pip3 install gunicorn
RUN pip3 install connexion==2.7.0

# expose the flask port
EXPOSE $FLASK_PORT

create the logs directory
RUN mkdir /home/CodeTest/GeneticsPro/python-flask-server/logs

# set working directory
# WORKDIR /home/CodeTest/GeneticsPro/python-flask-server
WORKDIR /home/CodeTest/GeneticsPro/python-flask-server

# CMD cat /proc/version
CMD gunicorn -w 2 --bind 0.0.0.0:$FLASK_PORT openapi_server.__main__:app --timeout 3600
# CMD . /home/CodeTest/GeneticsPro/Test/echo_env.txt

