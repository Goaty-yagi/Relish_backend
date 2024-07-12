# Use Python 3.10 slim version on Debian Buster
FROM python:3.10-slim-buster

# Install Git
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app/src

# Create a directory for the project
RUN mkdir -p /app
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install -r requirements.txt

# Copy the rest of your application code
COPY . /app

# Run Gunicorn
CMD ["gunicorn", "src.root.wsgi:application", "--bind", "0.0.0.0:8000"]
