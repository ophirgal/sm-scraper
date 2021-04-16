
FROM python:3.8

WORKDIR .

COPY . .

RUN python3.8 -m pip install pip --upgrade
RUN python3 -m pip install \
        flask \
        psycopg2 \
        requests


CMD python3 -m src.dashboard.server

## instructions:
# change dependencies above if needed
# change CMD line to run your main module; see how shu did it in `nlp.Dockerfile'
# `make dashboard`

