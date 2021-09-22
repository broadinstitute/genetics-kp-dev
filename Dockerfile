FROM python:3-alpine

LABEL author="Marc Duby, Broad Institute"
LABEL description="The Flannick's Lab's TRAPI Genetics KP"

# get/set the environment variables
ARG FLASK_PORT=fl_port
ENV FLASK_PORT ${FLASK_PORT}

# update the image
RUN apk add --update git

# Pull the code from git
RUN mkdir /home/CodeTest       
RUN cd /home/CodeTest 
RUN git clone -b md_mysql_batch https://github.com/broadinstitute/genetics-kp-dev /home/CodeTest/GeneticsPro
RUN cd /home/CodeTest/GeneticsPro

# expose the flask port
EXPOSE $FLASK_PORT

# set working directory
# WORKDIR /home/CodeTest/GeneticsPro/python-flask-server
WORKDIR /home/CodeTest/GeneticsPro/python-flask-server

# CMD cat /proc/version
CMD echo $FLASK_PORT 
