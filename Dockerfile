from python:3.7 

RUN mkdir /app
RUN apt-get update && apt-get install -y graphviz vim

WORKDIR /app

RUN python -m pip install --upgrade pip
ADD requirements.txt requirements.test.txt /app/
RUN pip install -r requirements.txt
RUN pip install -r requirements.test.txt

ADD . /app

ENV IS_DOCKER=1

ADD jupyter_notebook_config.json /root/.jupyter

CMD jupyter notebook --ip=0.0.0.0 --port=8080 --allow-root 

