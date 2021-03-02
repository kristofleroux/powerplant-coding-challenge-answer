# Python 3.8
FROM python:3.8-buster
LABEL author="Kristof J Leroux"

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV LD_LIBRARY_PATH /usr/lib:/usr/local/lib

RUN apt-get upgrade && apt-get update
RUN apt-get --assume-yes install coinor-cbc
RUN rm -rf /tmp/*

# Packages that we need
COPY requirements.txt /app/
WORKDIR /app

# Copy all the files from current source directory(from your system) to
# Docker container in /app directory
COPY . /app

RUN chmod 777 ./entrypoint.sh

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# We want to start app.py file. (change it with your file name)
# Argument to python command
EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
