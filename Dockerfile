from python:3.7

RUN mkdir /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

ADD . /app

CMD ['pytest', '-vls']

