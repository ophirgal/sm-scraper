FROM ubuntu:18.04
RUN apt-get update && apt-get install -y gnupg dirmngr wget
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common postgresql-12 postgresql-client-12

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
# And add ``listen_addresses`` to ``/etc/postgresql/12/main/postgresql.conf``
RUN echo "host  all  all  0.0.0.0/0  trust" >> /etc/postgresql/12/main/pg_hba.conf \
    && echo "host  all  postgres  127.0.0.1/32  trust" >> /etc/postgresql/12/main/pg_hba.conf \
    && echo "host  all  postgres  ::1/0  trust" >> /etc/postgresql/12/main/pg_hba.conf \
    && sed -i -e 's/md5/trust/g' /etc/postgresql/12/main/pg_hba.conf \
    && sed -i -e 's/peer/trust/g' /etc/postgresql/12/main/pg_hba.conf \
    && echo "listen_addresses='*'" >> /etc/postgresql/12/main/postgresql.conf

# Run the rest of the commands as the `postgres` user
USER postgres

RUN /etc/init.d/postgresql start \
    && createdb -w -O postgres smscraper \
    && service postgresql stop

# Expose the PostgreSQL port
EXPOSE 5432

COPY ./data/smscraper/smscraper.sql ./data/smscraper/smscraper.tsv /data/
RUN service postgresql restart \
    && psql -U postgres -d smscraper -f /data/smscraper.sql \
    && service postgresql stop

# Create a PostgreSQL role named `docker` with `docker` as the password
# and then create a database `docker` owned by the ``docker` role.
CMD /etc/init.d/postgresql start \
    && psql -U postgres -d smscraper
    
