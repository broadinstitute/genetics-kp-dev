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

# get/set the environment variables
# NOTE: set this below checkout code to speed up testing (can use cached tag for checkout)

ARG fl_port
ENV FLASK_PORT=8080

ARG db_host
ENV DB_HOST=localhost

ARG db_user
ENV DB_USER=genetics-rds-admin

ARG db_passwd
ENV DB_PASSWD=aocaik7Peib2eiquoosh

ARG db_schema
ENV DB_SCHEMA=genetics_kp_schema

ARG db_cache_schema
ENV DB_CACHE_SCHEMA=genetics_kp_schema

ARG db_results_limit
ENV DB_RESULTS_LIMIT=150

ARG tran_max_query_size
ENV TRAN_MAX_QUERY_SIZE=100000

ARG tran_url_normalizer
ENV TRAN_URL_NORMALIZER=https://nodenormalization-sri.renci.org/get_normalized_nodes

# expose the flask port
EXPOSE 8080

# create the logs directory
# RUN mkdir /home/CodeTest/GeneticsPro/python-flask-server/logs

# set working directory
# WORKDIR /home/CodeTest/GeneticsPro/python-flask-server
WORKDIR /home/CodeTest/GeneticsPro/python-flask-server

# CMD cat /proc/version
CMD gunicorn -w 2 --bind 0.0.0.0:8080 openapi_server.__main__:app --timeout 3600
# CMD . /home/CodeTest/GeneticsPro/Test/echo_env.txt

