

FROM ubuntu:16.04

# Add the PostgreSQL PGP key to verify their Debian packages.
RUN apt-key adv \
        --keyserver hkp://p80.pool.sks-keyservers.net:80 \
        --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8 \
    && echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > \
        /etc/apt/sources.list.d/pgdg.list \
    && apt-get update && apt-get install -y \
        python-software-properties \
        software-properties-common \
        postgresql-9.3 \
        postgresql-client-9.3 \
        postgresql-contrib-9.3 \
        postgresql-server-dev-9.3 \
        libpq-dev \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
        python3.8 \
        python3-pip \
    && pip3 install \
        flask \
        psycopg2 \
        requests


CMD python3 --version

## instructions:
# change dependencies above if needed
# change CMD line to run your main module; see how shu did it in `nlp.Dockerfile'
# `make dashboard`

