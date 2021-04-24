FROM python:3.8

# define environment variable(s)
ENV HOST_OS=DEFAULT

RUN python3.8 -m pip install pip --upgrade
RUN pip3 install \
        flask \
        psycopg2 \
        requests


CMD python3 -m src.dashboard.server --host-os=$HOST_OS

## instructions:
# change dependencies above if needed
# change CMD line to run your main module; see how shu did it in `nlp.Dockerfile'
# `make dashboard`
