FROM python:3.9-slim

# Required to run get SSL certs and perform health checks when locally run in docker-compose
RUN apt-get update -q && apt-get install -yq curl

RUN useradd -ms /bin/bash canarypy
RUN mkdir /var/log/myapp
WORKDIR /home/canarypy

COPY ./canarypy/api /home/canarypy/canarypy/api
COPY requirements.txt /home/canarypy
COPY setup.py /home/canarypy
COPY ./canarypy/alembic.ini /home/canarypy
COPY ./alembic /home/canarypy/alembic

RUN chown -R canarypy:canarypy /home/canarypy
#RUN chmod +x /home/canarypy/canarypy/api/run.py

USER canarypy:canarypy
#--no-cache-dir
RUN pip install -r requirements.txt

RUN pip install -e .

ENV PORT=8080
EXPOSE $PORT

ENTRYPOINT ["/home/canarypy/canarypy/api/run.py"]
