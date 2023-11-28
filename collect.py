import requests
import json
import mysql.connector
import os

from datetime import datetime
from datetime import timedelta

def parseResponse(response):
    mydb = mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_DB']
    )

    mycursor = mydb.cursor()
    q = 'INSERT INTO dayaheadprices (id, zone, start, end, price, local_price) VALUES (0, \'SE3\', %s, %s, %s, %s)'
    for hour in response:
        start = hour['time_start']
        end = hour['time_end']
        price = hour['EUR_per_kWh']
        local_price = hour['SEK_per_kWh']
        data = (start, end, price, local_price)
        try:
            mycursor.execute(q, data)
        except mysql.connector.Error as my_error:
            print(my_error)

    mydb.commit()

def main():
    tomorrow = datetime.now() + timedelta(days=1)
    print(f'Y {tomorrow.year} M {tomorrow.month} D {str(tomorrow.day).zfill(2)}')
    url = 'https://www.elprisetjustnu.se/api/v1/prices/' + str(tomorrow.year) + '/' + str(tomorrow.month).zfill(2) + '-' + str(tomorrow.day).zfill(2) + '_SE3.json'

    r = requests.get(url, allow_redirects=True)
#   if r.status_code == 200:
#       parseResponse(r.json())


if __name__ == '__main__':
    main()