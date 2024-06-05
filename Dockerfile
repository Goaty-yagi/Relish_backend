# Use Python 3.10 slim version on Debian Buster
FROM python:3.10-slim-buster

# Install Git
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

ENV PYTHONUNBUFFERED 1

# Create a directory for the project
RUN mkdir -p /root
WORKDIR /root

# Copy the requirements file and install dependencies
COPY requirements.txt /root/
RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install -r requirements.txt
