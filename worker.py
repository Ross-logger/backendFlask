import psycopg2
import time, requests
from math import ceil, sqrt
from datetime import datetime
import flask

conn = psycopg2.connect(dbname='d9phncea8bbook', user='irzyivcngwtzbb',
                        password='f12c32668291295574019ce41bb71332958deaf434ad0f67a4a10d378fd9d23d',
                        host='ec2-52-50-171-4.eu-west-1.compute.amazonaws.com', port=5432)

n = int(input())


def find_prost(n):
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
    new_num = n
    multi = 1
    added = 2
    length = len(str(n))

    while True:
        result = find_prost(n)
        if result is not None and str(new_num)[:length] == str(n)[:length]:
            return result
        else:
            if added < multi - 1:
                new_num += 1
                added += 1
            else:
                multi *= 10
                new_num = multi * n
                added = 0
            if new_num > 10 ** 10:
                return None

print(worker(n))


def delete_row():
    cur.execute(f"DELETE FROM worker WHERE email = '{str(email)}' AND time_started = '{str(time_started)}'")


while True:
    cur = conn.cursor()
    cur.execute(f"SELECT email, n, time_started FROM worker WHERE status = 'in ochered'")
    ans = cur.fetchall()
    i = None
    for i in ans:
        email, n, time_started = i
        break
    if i is None:
        time.sleep(5)
        continue
    time_started = datetime.strptime(time_started, '%Y-%m-%d %H:%M:%S.%f')
    delete_row()
    conn.commit()
    cur.execute(
        f"INSERT INTO worker (email, time, n, p, q, status, time_started, time_ended) VALUES ('{str(email)}', '', '{str(n)}', '0', '0', 'in progress', '{str(time_started)}', '')")
    conn.commit()
    list = worker(n)
    p = list[0]
    q = list[1]
    time_ended = datetime.now()
    time_t = str(time_ended).split(' ')
    time_t = time_t[-1]
    delete_row()
    conn.commit()
    cur.execute(
        f"INSERT INTO worker (email, time, n, p, q, status, time_started, time_ended) VALUES ('{str(email)}', '{str(time_t)}', '{str(n)}', '{p}', '{q}', 'finished', '{time_started}', '{time_ended}')")
    conn.commit()
    cur.close()
    print('next cycle')
    time.sleep(5)
