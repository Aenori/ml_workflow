from python:3.7

RUN mkdir /app
ADD requirements.txt requirements.test.txt /app/
RUN apt-get update && apt-get install -y graphviz vim

WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -r requirements.test.txt

ADD . /app

ENV IS_DOCKER=1

CMD pytest -vls

