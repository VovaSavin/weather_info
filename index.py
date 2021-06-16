import schedule
import time

from sql_querry import main


schedule.every().day.at("09:00:00").do(main)


while True:
    schedule.run_pending()
    time.sleep(1)
