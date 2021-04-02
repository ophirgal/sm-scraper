import subprocess
import multiprocessing
import sys
import time

def dashboard_process():
    arg = 'localhost' if 'localhost' in sys.argv else ''
    subprocess.call(['python3', 'dashboard/server.py', arg])


def scraper_process():
    subprocess.call(['python3', 'scraper/scraper.py'])


if __name__ == '__main__':
    print('waiting for database to start up')
    time.sleep(10) # wait a few seconds for the DB to start up
    multiprocessing.Process(name='dashboard_process',
                            target=dashboard_process).start()
    multiprocessing.Process(name='scraper_process',
                            target=scraper_process).start()
