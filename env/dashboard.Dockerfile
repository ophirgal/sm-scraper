

FROM python:3.8

# Add the PostgreSQL PGP key to verify their Debian packages.
RUN pip3 install \
        flask \
        psycopg2 \
        requests


CMD python3 -m src.dashboard.server

## instructions:
# change dependencies above if needed
# change CMD line to run your main module; see how shu did it in `nlp.Dockerfile'
# `make dashboard`
