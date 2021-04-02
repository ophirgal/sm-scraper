/usr/lib/postgresql/9.3/bin/postgres -D /var/lib/postgresql/9.3/main \
-c config_file=/etc/postgresql/9.3/main/postgresql.conf &
sleep 10 && psql -U cmsc828d -d smsdatabase -f ../sql_setup.sql;
python3 main.py
