import psycopg2
import datetime
import time
n = int(input())
def find_p_and_q(n):
    nums = list()
    w = 2
    while w < n:
        if n % w == 0:
            nums.append(w)
        w += 1
    for i in nums:
        for j in nums[::-1]:
            rez = i * j
            if rez < n:
                break
            if rez == n:
                return [i, j]
print(find_p_and_q(n))

def delete_row():
    cur.execute("DELETE FROM worker WHERE id = {} AND time_started = '{}';".format(str(i_d), str(time_started)))


conn = psycopg2.connect(dbname='d9phncea8bbook', user='irzyivcngwtzbb',
                        password='f12c32668291295574019ce41bb71332958deaf434ad0f67a4a10d378fd9d23d',
                        host='ec2-52-50-171-4.eu-west-1.compute.amazonaws.com', port=5432)
# CREATE TABLE worker (id integer, time varchar(255), n varchar(255), p varchar(255), q varchar(255), status varchar(255), time_started varchar(255), time_ended varchar(255))
while True:
    cur = conn.cursor()
    cur.execute("SELECT id, n, time_started FROM worker WHERE status = 'in queue';")
    ans = cur.fetchall()
    i = None
    for i in ans:
        i_d, start_num, time_started = i
        break
    if i is None:
        time.sleep(5)
        continue
    time_started = datetime.datetime.strptime(time_started, '%Y-%m-%d %H:%M:%S.%f')
    delete_row()
    conn.commit()
    cur.execute("INSERT INTO worker (id, time, n, p, q, status, time_started, time_ended) VALUES ({}, '', {}, 0, 0, 'in progress', '{}', '')".format
            (str(i_d), str(start_num), str(time_started)))
    conn.commit()
    p, q = find_p_and_q(start_num)
    time_ended = datetime.datetime.now()
    time_t = str(time_ended).split(' ')
    time_t = time_t[-1]
    delete_row()
    conn.commit()
    cur.execute \
        ("INSERT INTO worker (id, time, n, p, q, status, time_started, time_ended) VALUES ({}, '{}', {}, {}, {}, 'finished', '{}', '{}')".format
            (str(i_d), str(time_t), str(start_num), p, q, str(time_started), str(time_ended)))
    conn.commit()
    cur.close()
    time.sleep(5)