import psycopg2
import time
from math import ceil, sqrt
from datetime import datetime

from models import *
from sqlalchemy.orm import scoped_session
from database import Session, engine

conn = psycopg2.connect(dbname='d62q832uhh9225', user='urgttpxzaoisdo',
                        password='5fa49425b2ca75ba17f382fb0a94b6fe2c4156585c7a407953cb55b7524cb8ad',
                        host='ec2-54-195-76-73.eu-west-1.compute.amazonaws.com', port=5432)
cur = conn.cursor()
database = Session()


def find_prime_factors(n):
    n = int(n)

    ans = []
    pos = False

    for i in range(2, ceil(sqrt(n))):
        if n % i == 0:
            for j in range(2, ceil(sqrt(i)) + 1):
                if i % j == 0:
                    pos = False
                    break
                if j == ceil(sqrt(i)):
                    pos = True
            for j in range(2, ceil(sqrt(n / i)) + 1):
                if (n / i) % j == 0:
                    pos = False
                    break
                if j == ceil(sqrt(i)):
                    pos = True
            if pos:
                ans.append(i)
                ans.append(n / i)
            break

    if pos:
        if n == 1:
            return None
        elif len(ans) == 0:
            # result = str(int(sqrt(n))) + " " + str(int(sqrt(n)))
            result = [int(sqrt(n)), int(sqrt(n))]
            return result
        else:
            # result = str(int(ans[0])) + " " + str(int(ans[1]))
            result = [int(ans[0]), int(ans[1])]
            return result
    else:
        return None


def worker(n):
    start_num = int(n)
    new_num = start_num
    multi = 1
    added = 2
    length = len(str(start_num))

    while True:
        result = find_prime_factors(new_num)
        if result is not None and str(new_num)[:length] == str(start_num)[:length]:
            return result
        else:
            if added < multi - 1:
                new_num += 1
                added += 1
            else:
                multi *= 10
                new_num = multi * start_num
                added = 0
            if new_num > 10 ** 10:
                return None


# def delete_row():
#     database.query(Worker).filter_by(email=email, time_started=time_started).delete()

    # cur.execute("DELETE FROM worker WHERE email= '{}' AND time_started = '{}';".format(email, str(time_started)))


while True:
    print('############ next cycle')
    answer = database.query(Worker).filter_by(status='Queued')
    # cur.execute("SELECT email, n, time_started FROM worker WHERE status = 'Queued';")
    # answer = cur.fetchall()
    for att in answer:
        att.status = 'Progressing'
        database.add(att)
        database.commit()
        time_started = time.time()
        res = worker(att.n)
        p, q = res[0], res[1]
        time_ended = time.time()
        elapsed = round(time_ended - time_started, 8)
        att.time_ended, att.status, att.p, att.q, = elapsed, 'Done', p, q
        print(time_ended)
        database.add(att)
        database.commit()
        # delete_row()
        time_t = time.time()
        time_ended = time.time()
        # delete_row()
    time.sleep(5)
