import psycopg2
import time
from math import ceil, sqrt
from datetime import datetime

conn = psycopg2.connect(dbname='d9phncea8bbook', user='irzyivcngwtzbb',
                        password='f12c32668291295574019ce41bb71332958deaf434ad0f67a4a10d378fd9d23d',
                        host='ec2-52-50-171-4.eu-west-1.compute.amazonaws.com', port=5432)
cur = conn.cursor()


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
            if added < multi-1:
                new_num += 1
                added += 1
            else:
                multi *= 10
                new_num = multi*start_num
                added = 0
            if new_num > 10**10:
                return None

def delete_row():
    cur.execute(f"DELETE FROM worker WHERE email = '{email}' AND time_started = '{str(time_started)}'")


while True:
    print('############ next cycle')
    cur.execute("SELECT email, n, time_started FROM worker WHERE status = 'in queue';")
    answer = cur.fetchall()
    print(answer)
    if answer != []:
        answer = answer[0]
        email = answer[0]
        start_num = answer[1]
        time_started = answer[2]
        print(start_num)
        time_started = datetime.strptime(time_started, '%Y-%m-%d %H:%M:%S.%f')
        delete_row()
        conn.commit()
        cur.execute("INSERT INTO worker (email, time, n, p, q, status, time_started, time_ended) VALUES ('{}', '', {}, 0, 0, 'in progress', '{}', '')".format(str(email), str(start_num), str(time_started)))
        conn.commit()
        res = worker(start_num)
        print(res)
        p, q = res[0], res[1]
        time_ended = datetime.now()
        print(time_ended)
        print(str(time_ended))
        time_t = str(time_ended).split(' ')
        time_t = time_t[-1]
        delete_row()
        conn.commit()
        cur.execute("INSERT INTO worker (email, time, n, p, q, status, time_started, time_ended) VALUES ('{}', '{}', {}, {}, {}, 'finished', '{}', '{}')".format(str(email), str(time_t), str(start_num), p, q, str(time_started), str(time_ended)))
        conn.commit()
    time.sleep(5)

