#
# example Dockerfile for https://docs.docker.com/engine/examples/postgresql_service/
#

FROM ubuntu:16.04

# Add the PostgreSQL PGP key to verify their Debian packages.
# It should be the same key as https://www.postgresql.org/media/keys/ACCC4CF8.asc
# Add PostgreSQL's repository. It contains the most recent stable release
#  of PostgreSQL.
# Install ``python-software-properties``, ``software-properties-common`` and PostgreSQL 9.5
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
        postgresql-9.5 \
        postgresql-client-9.5 \
        postgresql-contrib-9.5 \
        postgresql-server-dev-9.5 \
        libpq-dev \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
        python3.8 \
        python3-pip \
    && pip3 install \
        flask \
        psycopg2

# Note: The official Debian and Ubuntu images automatically ``apt-get clean``
# after each ``apt-get``

# Run the rest of the commands as the ``postgres`` user created by the ``postgres-9.5`` package when it was ``apt-get installed``
USER postgres

# Create a PostgreSQL role named ``docker`` with ``docker`` as the password and
# then create a database `docker` owned by the ``docker`` role.
# Note: here we use ``&&\`` to run commands one after the other - the ``\``
#       allows the RUN command to span multiple lines.
RUN /etc/init.d/postgresql start \
    && psql --command "CREATE USER cmsc828d WITH SUPERUSER PASSWORD 'pword';" \
    && createdb -w -O cmsc828d smscraper \
    && service postgresql stop

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
# And add ``listen_addresses`` to ``/etc/postgresql/9.5/main/postgresql.conf``
RUN echo "host  all  all  0.0.0.0/0  trust" >> /etc/postgresql/9.5/main/pg_hba.conf \
    && echo "host  all  cmsc828d  127.0.0.1/32  trust" >> /etc/postgresql/9.5/main/pg_hba.conf \
    && echo "host  all  cmsc828d  ::1/0  trust" >> /etc/postgresql/9.5/main/pg_hba.conf \
    && sed -i -e 's/md5/trust/g' /etc/postgresql/9.5/main/pg_hba.conf \
    && sed -i -e 's/peer/trust/g' /etc/postgresql/9.5/main/pg_hba.conf \
    && echo "listen_addresses='*'" >> /etc/postgresql/9.5/main/postgresql.conf \
	&& echo "dynamic_shared_memory_type=none" >> /etc/postgresql/9.5/main/postgresql.conf

COPY ./data/smscraper/smscraper.sql ./data/smscraper/smscraper.tsv /data/
RUN service postgresql restart \
    && psql -U cmsc828d -d smscraper -f /data/smscraper.sql \
    && service postgresql stop


# Expose the PostgreSQL port
EXPOSE 5432


# Add VOLUMEs to allow backup of config, logs and databases
# VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# Set the default command to run when starting the container
CMD ["/usr/lib/postgresql/9.5/bin/postgres", "-D", "/var/lib/postgresql/9.5/main", "-c", "config_file=/etc/postgresql/9.5/main/postgresql.conf"]


## instructions:
# change dependencies/setup above if needed
# `make db`
# `psql -h localhost -p 5432 -U cmsc828d -d smscraper` from another terminal
