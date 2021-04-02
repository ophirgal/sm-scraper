#
# example Dockerfile for https://docs.docker.com/engine/examples/postgresql_service/
#

FROM ubuntu:16.04

COPY requirements.txt .
COPY sql_setup.sql .

# Add the PostgreSQL PGP key to verify their Debian packages.
# It should be the same key as https://www.postgresql.org/media/keys/ACCC4CF8.asc
# Add PostgreSQL's repository. It contains the most recent stable release
#  of PostgreSQL.
# Install ``python-software-properties``, ``software-properties-common`` and PostgreSQL 9.3
#  There are some warnings (in red) that show up during the build. You can hide
#  them by prefixing each apt-get statement with DEBIAN_FRONTEND=noninteractive
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
    && python3 -m pip install -r requirements.txt


# Note: The official Debian and Ubuntu images automatically ``apt-get clean``
# after each ``apt-get``

# Run the rest of the commands as the ``postgres`` user created by the ``postgres-9.3`` package when it was ``apt-get installed``
USER postgres

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
# And add ``listen_addresses`` to ``/etc/postgresql/9.3/main/postgresql.conf``
RUN echo "host  all  all  0.0.0.0/0  trust" >> /etc/postgresql/9.3/main/pg_hba.conf \
    && echo "host  all  cmsc828d  127.0.0.1/32  trust" >> /etc/postgresql/9.3/main/pg_hba.conf \
    && echo "host  all  cmsc828d  ::1/0  trust" >> /etc/postgresql/9.3/main/pg_hba.conf \
    && sed -i -e 's/md5/trust/g' /etc/postgresql/9.3/main/pg_hba.conf \
    && sed -i -e 's/peer/trust/g' /etc/postgresql/9.3/main/pg_hba.conf \
    && echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf


# Create a PostgreSQL role and
# then create a database owned by the role.
# Note: here we use ``&&\`` to run commands one after the other - the ``\``
#       allows the RUN command to span multiple lines.
RUN /etc/init.d/postgresql start \
    && psql --command "CREATE USER cmsc828d WITH SUPERUSER PASSWORD 'pword';" \
    && createdb -w -O cmsc828d smsdatabase

# By default, listen on port 5000
EXPOSE 5000/tcp

# add /src folder and as working directory
COPY src /src
WORKDIR /src

# Set the default command to run when starting the container
CMD ["/bin/bash", "start.sh"]

