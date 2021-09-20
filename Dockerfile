FROM python:3-alpine

LABEL author="Marc Duby, Broad Institute"
LABEL description="The Flannick's Lab's TRAPI Genetics KP"

# update the image
# RUN apt-get update 
# RUN apt-get install -y git
RUN apk add --update git

# Pull the code from git
RUN mkdir /home/CodeTest       
RUN cd /home/CodeTest 
RUN git clone https://github.com/broadinstitute/genetics-kp-dev

# set working directory
WORKDIR /home/CodeTest

CMD cat /proc/version
