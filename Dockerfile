from python:3.7 

RUN mkdir /app
RUN apt-get update && apt-get install -y vim graphviz

WORKDIR /app

RUN python -m pip install --upgrade pip

ADD requirements.txt requirements.test.txt /app/

RUN pip install pydot
RUN pip install -r requirements.txt
RUN pip install -r requirements.test.txt

ADD . /app

ENV IS_DOCKER=1
