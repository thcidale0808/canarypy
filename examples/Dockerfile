FROM python:3.9-slim

# Required to run get SSL certs and perform health checks when locally run in docker-compose
RUN apt-get update -q && apt-get install -yq curl netcat-openbsd

RUN useradd -ms /bin/bash canarypy
RUN mkdir /var/log/myapp
WORKDIR /home/canarypy

USER canarypy:canarypy

ENV PATH="/home/canarypy/.local/bin:${PATH}"
ENV PYTHONPATH="/home/canarypy/.local/lib/python3.9/site-packages:${PYTHONPATH:-}"

RUN pip install canarypy

ENV PORT=8080
EXPOSE $PORT

CMD ["canarypy", "api", "start"]