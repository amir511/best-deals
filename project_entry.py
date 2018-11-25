import schedule
import subprocess
import os
from multiprocessing import Process


def run_django_server():
    subprocess.Popen(['python', 'manage.py', 'runserver'])


def schedule_and_run_crawling():
    task = lambda: subprocess.Popen(['python', 'crawl_and_update_db.py'])
    task() # Run once in the beginning
    schedule.every().hour.do(task)
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    p = Process(target=schedule_and_run_crawling)

    p.start()
    run_django_server()

    p.join()

