import psycopg2
import requests
import argparse
import os

def getConnection(db_host, databaseName='smscraper'):
    connection = psycopg2.connect(user="postgres",
                                    host=db_host,
                                    port="5432",
                                    database=databaseName)
    return connection

def back_up(db_host, base_file_name):
    connection  = getConnection(db_host)
    cursor = connection.cursor()
    
    cursor.execute(
        "COPY scraped_data TO " + "'"+ 
         os.environ['PROJECT_DN'] + "/env/data/smscraper/db_backup_scraped_data.tsv';"
    )
    connection.commit()
    cursor.execute(
        "COPY key_words TO " + "'"+ 
         os.environ['PROJECT_DN'] + "/env/data/smscraper/db_backup_key_words.tsv';"
    )
    connection.commit()
    cursor.execute(
        "COPY entities TO " + "'"+ 
         os.environ['PROJECT_DN'] + "/env/data/smscraper/db_backup_entities.tsv';"
    )
    connection.commit()


if __name__ == '__main__':	
    parser = argparse.ArgumentParser()
    parser.add_argument('--host-os', default='mac', type=str, choices=['windows', 'mac', 'linux'])
    parser.add_argument('--base-file-name', default='db_backup', type=str)
    args = parser.parse_args()
    host_os = args.host_os
    base_file_name = args.base_file_name
    db_host = 'localhost' if host_os == 'linux' else '172.28.0.9'

    back_up(db_host, base_file_name)

