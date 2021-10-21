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
RUN git clone git@github.com:azadeheskandari/genetics-kp-dev.git /home/CodeTest/GeneticsPro
RUN cd /home/CodeTest/GeneticsPro

# install python libraries
RUN pip3 install PyMySQL==0.10.1
RUN pip3 install gunicorn
RUN pip3 install connexion==2.7.0

# get/set the environment variables
# NOTE: set this below checkout code to speed up testing (can use cached tag for checkout)
ARG fl_port
ENV FLASK_PORT=$fl_port

ARG db_host
ENV DB_HOST=$db_host

ARG db_user
ENV DB_USER=$db_user

ARG db_passwd
ENV DB_PASSWD=$db_passwd

ARG db_schema
ENV DB_SCHEMA=$db_schema

ARG db_cache_schema
ENV DB_CACHE_SCHEMA=$db_cache_schema

ARG db_results_limit
ENV DB_RESULTS_LIMIT=$db_results_limit

ARG tran_log_file
ENV TRAN_LOG_FILE=$tran_log_file

ARG tran_max_query_size
ENV TRAN_MAX_QUERY_SIZE=$tran_max_query_size

ARG tran_url_normalizer
ENV TRAN_URL_NORMALIZER=$tran_url_normalizer

# expose the flask port
EXPOSE $FLASK_PORT

# create the logs directory
# RUN mkdir /home/CodeTest/GeneticsPro/python-flask-server/logs

# set working directory
# WORKDIR /home/CodeTest/GeneticsPro/python-flask-server
WORKDIR /home/CodeTest/GeneticsPro/python-flask-server

# CMD cat /proc/version
CMD gunicorn -w 2 --bind 0.0.0.0:$FLASK_PORT openapi_server.__main__:app --timeout 3600 --log-file $TRAN_LOG_FILE --capture-output
# CMD . /home/CodeTest/GeneticsPro/Test/echo_env.txt

