from flask import Flask, render_template, request, redirect, url_for, make_response, session
import json, random as rnd, requests, psycopg2, os, string, smtplib
from hashlib import md5
from email.message import EmailMessage
from datetime import datetime
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, render_template, redirect, request, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import scoped_session

import models
from database import Session, engine

site_keya = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'

conn = psycopg2.connect(dbname='d6rbu51aggngta', user='oomzugrngzshgq',
                        password='07ddf913052409e8ffb5fe1451a28504244e269ee506ffab18818a6ed513edc9',
                        host='ec2-54-74-77-126.eu-west-1.compute.amazonaws.com', port=5432)
cur = conn.cursor()
app = Flask(__name__)
app.secret_key = 'yus1'
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

models.Base.metadata.create_all(bind=engine)

app.session = scoped_session(Session)


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()


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


@app.route("/task5/sign-up/", methods=["GET", "POST"])
def sign_up():
    if request.method == 'POST':
        captcha_response = request.form['g-recaptcha-response']
        site_key = '6Leig10aAAAAAOb62ZbsGklzVXmpWhHcMuwHhzRC'
        auto = request.cookies.get('auto')
        if auto == 'True':
            site_key = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
        status, msg, msg2, msg3 = "ok", '', '', ''
        email = request.form.get('email')
        su = rnd.choice(string.ascii_letters) + rnd.choice(string.ascii_letters) + str(rnd.randint(1000, 10000))
        if is_human(captcha_response) == False:
            status, msg = "false", 'Botyara!'
        elif not email:
            msg3, status = "Pls fill all places", "false"
        peter = app.session.query(models.Users).filter_by(email=email).all()
        if peter != []:
            msg3, status = "This email adress already exists!", "false"
        if status == "ok":
            app.session.add(models.Users(email=email, code=su, status='not_veri'))
            app.session.commit()
            msg = EmailMessage()
            msg.set_content(
                "Congrats!Your activation link: " + 'https://limp.herokuapp.com/task5/verification/' + email + '/' + su)
            msg['Subject'] = 'Click to confirm your email'
            msg['From'] = 'no-reply@limp.herokuapp.com'
            msg['To'] = f'{email}'
            s = smtplib.SMTP(host='b.li2sites.ru', port=30025)
            s.send_message(msg)
            s.quit()
            return render_template('after_signup.html', url_veri=url_for('verification', email=email, code=su))
        return render_template('signup.html', site_key=site_key, status=status, msg=msg, msg2=msg2, msg3=msg3)

    if request.method == 'GET':
        auto = request.cookies.get('auto')
        if auto == 'True':
            site_key = site_keya
        else:
            site_key = '6Leig10aAAAAAOb62ZbsGklzVXmpWhHcMuwHhzRC'
        return render_template('signup.html', site_key=site_key)


def is_human(captcha_response):
    if request.cookies.get('auto') == "True":
        secret_key = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
    else:
        secret_key = '6Leig10aAAAAAGc9BuyWuqaSE5nLNja1HYkBPwmY'
    captcha_data = {'secret': secret_key, 'response': captcha_response}
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captcha_data)
    response_text = json.loads(response.text)
    return response_text['success']


@app.route("/task5/verification/<email>/<code>", methods=["GET", "POST"])
def verification(email, code):
    if request.method == 'POST':
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if password == password2:
            hash_pwd = generate_password_hash(password)
            app.session.add(models.Users(email=email, password=hash_pwd, status='veri'))
            app.session.commit()
            return redirect(url_for('task5'))
        else:
            msg = 'Passwords are not similar!Or you have already registred! '
            return render_template('veri.html', msg=msg, email=email)
    if request.method == 'GET':
        return render_template('veri.html', email=email)


@app.route("/task5/sign-in/", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        status, msg, msg2, msg3 = "ok", "", "", ""
        session['user_email'] = email
        peter = app.session.query(models.Users).filter_by(email=email, status='veri').first()
        if peter is None:
            msg = "RETARD!You are not registred!"
            status = "false"
        elif status == "ok":
            user_password = app.session.query(models.Users).filter_by(email=email, status='veri').first()
            if check_password_hash(password, user_password):
                msg2 = "RETARD!Your password is wrong!"
                status = "false"
            else:
                return redirect(url_for('task5'))
        return render_template('login.html', status=status, msg=msg, msg2=msg2, msg3=msg3)
    if request.method == 'GET':
        return render_template('login.html')


@app.route('/task5/work/', methods=['GET', 'POST'])
def work():
    email = session.get('user_email')
    if request.method == 'POST':
        n = request.form['n']
        time = datetime.now()
        app.session.add(models.Worker(email=email, time=time, status='Queued', n=n, p=0, q=0, time_started=time))
        app.session.commit()
        # cur.execute(
        #     f"INSERT INTO worker (email, time, N, p, q, status, time_started, time_ended) VALUES ('{email}', '', {n}, 0, 0, 'Queued', '{time}', '')")
        # conn.commit()
        return redirect(url_for('work'))
    else:
        peter = app.session.query(models.Worker).filter_by(email=email).all()
        app.session.commit()
        # cur.execute(
        #     f"SELECT time, n, p, q, status, time_started, time_ended FROM worker WHERE email = '{email}' ORDER BY time_started desc")
        # conn.commit()
    if peter != []:
        return render_template('worker.html', ans=reversed(peter))
    return render_template('worker.html')


@app.route("/task5/sign-out/")
def sign_out():
    session.pop('user_email', None)
    return redirect(url_for("sign_in"))


@app.route('/task5/')
def task5():
    email = session.get('user_email')
    ip = request.remote_addr
    time = datetime.now()
    app.session.add(models.Ips(email=email, ip=ip, time=time))
    app.session.commit()
    peter = app.session.query(models.Ips).filter_by(email=email).all()
    return render_template('task5.html', array=reversed(peter))


if __name__ == '__main__':
    app.run(debug=True)
