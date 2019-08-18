import sys
import time

from upload_data_to_db import add_data_to_db

while True:
    print("CRAWLING")
    sys.stdout.flush()
    add_data_to_db()
    print("CRAWLING FINISHED")
    sys.stdout.flush()
    time.sleep(60 * 10)
