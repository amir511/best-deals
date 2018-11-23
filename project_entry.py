import schedule
import subprocess
import os
from multiprocessing import Process

def schedule_and_run_crawling():
    task = lambda : subprocess.Popen(['python', 'crawl_and_update_db.py'])
    schedule.every(5).minutes.do(task)
    while True:
        schedule.run_pending()

def run_django_server():
    subprocess.Popen(['python', 'manage.py', 'runserver'])

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    p1 = Process(target=run_django_server)
    p2 = Process(target=schedule_and_run_crawling)
    
    p1.start()
    p2.start()

    p1.join()
    p2.join()