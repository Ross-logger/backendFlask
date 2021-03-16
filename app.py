from flask import Flask, render_template, request, redirect, url_for, make_response, session
import json, random as rnd, requests, psycopg2, os, string, smtplib
from hashlib import md5
from email.message import EmailMessage
from datetime import datetime

site_key = os.environ['site_key']

conn = psycopg2.connect(dbname='d9phncea8bbook', user='irzyivcngwtzbb',
                        password='f12c32668291295574019ce41bb71332958deaf434ad0f67a4a10d378fd9d23d',
                        host='ec2-52-50-171-4.eu-west-1.compute.amazonaws.com', port=5432)
cur = conn.cursor()
# print(cur.execute("select * from test"))
#  print(cur.execute("CREATE TABLE users ( ID SERIAL primary key,time varchar(64),ip varchar(64), email varchar(64))"))
# print(cur.execute("DROP TABLE worker"))
# print(cur.fetchall())
# Make the changes to the database persistent
conn.commit()
app = Flask(__name__)
app.secret_key = 'yus1'

# cur.execute("CREATE TABLE worker ( ID SERIAL primary key,email varchar(64),time varchar(64),N int, p int,q int,status varchar(64),time_started varchar(64),time_ended varchar(64))")
# cur.execute("CREATE TABLE data(email varchar(64),password varchar(64),code varchar(64),status varchar(64))")
conn.commit()


@app.route("/task5/test/enable")
def captcha_enable():
    resp = make_response(render_template('enable.html'))
    resp.set_cookie("auto", "True")
    return resp


@app.route("/task5/test/disable")
def captcha_disable():
    resp = make_response(render_template('disable.html'))
    resp.set_cookie("auto", "False")
    return resp


# @app.route('/task5/test/enable')
# def enable():
#     session['enable'] = 'enable'
#     return redirect(url_for('sign_up'))
#
#
# @app.route('/task5/test/disable')
# def disable():
#     session['enable'] = 'disable'
#     return redirect(url_for('sign_up'))


@app.route("/task5/sign-up/", methods=["GET", "POST"])
def sign_up():
    if request.method == 'POST':
        captcha_response = request.form['g-recaptcha-response']
        site_key = "6Leig10aAAAAAOb62ZbsGklzVXmpWhHcMuwHhzRC"
        auto = request.cookies.get('auto')
        if auto == 'True':
            site_key = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        su = rnd.choice(string.ascii_letters) + rnd.choice(string.ascii_letters) + str(rnd.randint(1000, 10000))

        status, msg, msg2, msg3 = "ok", '', '', ''
        if is_human(captcha_response) == 'False':
            status, msg = "false", 'Botyara!'
        else:
            cur.execute(f"SELECT email from data WHERE email='{email}'")
            if cur.fetchone() is not None:
                msg3 = "This email adress already exists!"
                status = "false"
        conn.commit()
        if status == "ok":
            # email_msg = f"<p><a href=/task5/verification/{email}/{su}/>Congrats!Your activation link here: https://limp.herokuapp.com/task5/verification/{email}/{su}</a></p>"
            msg = EmailMessage()
            msg.set_content(
                "Congrats!Your activation link: " + 'https://limp.herokuapp.com/task5/verification/' + email + '/' + su)
            msg['Subject'] = 'Click to confirm your email'
            msg['From'] = 'no-reply@limp.herokuapp.com'
            msg['To'] = f'{email}'
            s = smtplib.SMTP(host='b.li2sites.ru', port=30025)
            s.send_message(msg)
            s.quit()
            cur.execute(
                f"INSERT INTO  data (email,password,code,status) values ('{email}','{md5(password.encode('utf-8')).hexdigest()}','{su}','not_veri')")
            conn.commit()
            return render_template('after_signup.html', url_veri=url_for('verification', email=email, code=s))
        return render_template('signup.html', site_key=site_key, status=status, msg=msg, msg2=msg2, msg3=msg3)

    if request.method == 'GET':
        auto = request.cookies.get('auto')
        if auto == 'True':
            site_key = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
        else:
            site_key = '6Leig10aAAAAAOb62ZbsGklzVXmpWhHcMuwHhzRC'
        return render_template('signup.html', site_key=site_key)


def is_human(captcha_response):
    if request.cookies.get('auto') == "True":
        secret_key = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
        site_key = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
    else:
        secret_key = '6Leig10aAAAAAGc9BuyWuqaSE5nLNja1HYkBPwmY'
        site_key = '6Leig10aAAAAAOb62ZbsGklzVXmpWhHcMuwHhzRC'

    captcha_data = {'secret': site_key, 'response': captcha_response}
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captcha_data)
    response_text = json.loads(response.text)
    return response_text['success']


@app.route("/task5/verification/<email>/<code>", methods=["GET", "POST"])
def verification(email, code):
    if request.method == 'POST':
        password = request.form.get('password')
        password2 = request.form.get('password2')
        cur.execute(f"SELECT count(status) from data WHERE email='{email}'")
        if password == password2:
            cur.execute(
                f"INSERT INTO  data (email,password,status) values ('{email}','{md5(password.encode('utf-8')).hexdigest()}','veri')")
            conn.commit()
            return redirect(url_for('task5'))
        else:
            msg = 'Passwords are not similar!Or you have already registred! '
            return render_template('veri.html', site_key=site_key, msg=msg, email=email)
    if request.method == 'GET':
        return render_template('veri.html', site_key=site_key, email=email)


@app.route("/task5/sign-in/", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        email = request.form.get('email')
        password = md5(request.form.get('password').encode()).hexdigest()
        status, msg, msg2, msg3 = "ok", "", "", ""
        session['user_email'] = email
        # print(session.get('user_email'))
        # and cur.fetchall(f"SELECT status from data where email='{email}'") != "veri"
        cur.execute(f"SELECT email from data WHERE email='{email}'")
        if cur.fetchone() is None:
            msg = "RETARD!You are not registred!"
            status = "false"
        elif status == "ok":
            cur.execute(f"SELECT password from data WHERE email='{email}' and status='veri'")
            if password != cur.fetchone()[0]:
                msg2 = "RETARD!Your password is wrong!"
                status = "false"
            else:
                return redirect(url_for('task5'))
        return render_template('login.html', status=status, msg=msg, msg2=msg2, msg3=msg3)
    if request.method == 'GET':
        return render_template('login.html')


@app.route('/task5/work/', methods=['GET', 'POST'])
def work():
    email = session['user_email']
    # if email is None:
    #     return redirect(url_for('sign_in'))
    if request.method == 'POST':
        n = request.form['n']
        time = datetime.now()
        cur.execute(
            f"INSERT INTO worker (email, time, n, p, q, status, time_started, time_ended) VALUES ('{email}', '', {n}, 0, 0, 'in queue', '{time}', '')")
        conn.commit()
        return redirect(url_for('work'))
    else:
        cur.execute(f"SELECT time, n, p, q, status, time_started, time_ended FROM worker WHERE email = '{email}'")
        ans = cur.fetchall()
        return render_template('worker.html', ans=ans)


@app.route("/task5/sign-out/")
def sign_out():
    session.pop('user_email', None)
    return redirect(url_for("sign_in"))


@app.route('/task5/')
def task5():
    email = session.get('user_email')
    print(email)
    ip = request.remote_addr
    time = datetime.now()
    cur.execute(f"INSERT INTO users (time, ip,email) values ('{time}','{ip}','{email}')")
    conn.commit()
    cur.execute(f"SELECT time,ip from users where email='{email}'")
    array = cur.fetchall()
    return render_template('task5.html', array=array)



if __name__ == '__main__':
    app.run(debug=True)
