python3 -m pip install -r requirements.txt;
psql -U cmsc828d -d smsdatabase -f sql_setup.sql;
python3 src/main.py localhost;
