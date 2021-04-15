

FROM ubuntu:16.04

# Add the PostgreSQL PGP key to verify their Debian packages.
RUN apt-get update && apt-get install -y \
        python3.8 \
        python3-pip \
    && pip3 install \
        flask \
        psycopg2 \
        requests


CMD python3 -m src.dashboard.server

## instructions:
# change dependencies above if needed
# change CMD line to run your main module; see how shu did it in `nlp.Dockerfile'
# `make dashboard`

