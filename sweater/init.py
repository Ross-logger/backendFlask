from flask import Flask, render_template, request, redirect, url_for, make_response, session
import json, random as rnd, requests, psycopg2, os, string, smtplib
from hashlib import md5
from email.message import EmailMessage
from datetime import datetime
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, render_template, redirect, request, url_for, flash
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash


conn = psycopg2.connect(dbname='d6rbu51aggngta', user='oomzugrngzshgq',
                        password='07ddf913052409e8ffb5fe1451a28504244e269ee506ffab18818a6ed513edc9',
                        host='ec2-54-74-77-126.eu-west-1.compute.amazonaws.com', port=5432)
cur = conn.cursor()
conn.commit()

app = Flask(__name__)
app.secret_key = 'yus1'
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://oomzugrngzshgq:07ddf913052409e8ffb5fe1451a28504244e269ee506ffab18818a6ed513edc9@ec2-54-74-77-126.eu-west-1.compute.amazonaws.com:5432/d6rbu51aggngta'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
conn.commit()
login_manager = LoginManager(app)
if __name__ == '__main__':
    app.run(debug=True)

    from flask import Flask, render_template, request, redirect, url_for, make_response, session
    import json, random as rnd, requests, psycopg2, os, string, smtplib
    from hashlib import md5
    from email.message import EmailMessage
    from datetime import datetime
    from werkzeug.middleware.proxy_fix import ProxyFix
    from flask import Flask, render_template, redirect, request, url_for, flash
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
    from werkzeug.security import check_password_hash, generate_password_hash

    site_keya = os.environ['site_keya']

    conn = psycopg2.connect(dbname='d6rbu51aggngta', user='oomzugrngzshgq',
                            password='07ddf913052409e8ffb5fe1451a28504244e269ee506ffab18818a6ed513edc9',
                            host='ec2-54-74-77-126.eu-west-1.compute.amazonaws.com', port=5432)
    cur = conn.cursor()
    conn.commit()

    app = Flask(__name__)
    app.secret_key = 'yus1'
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgres://oomzugrngzshgq:07ddf913052409e8ffb5fe1451a28504244e269ee506ffab18818a6ed513edc9@ec2-54-74-77-126.eu-west-1.compute.amazonaws.com:5432/d6rbu51aggngta'
    db = SQLAlchemy(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    conn.commit()
    login_manager = LoginManager(app)


    class data(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(64), nullable=False)
        password = db.Column(db.String(256))
        code = db.Column(db.String(64))
        status = db.Column(db.String(64))


    class worker(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(64), nullable=False)
        time = db.Column(db.String(64), nullable=False)
        N = db.Column(db.Integer, nullable=False)
        p = db.Column(db.Integer, nullable=False)
        q = db.Column(db.Integer, nullable=False)
        status = db.Column(db.String(64), nullable=False)
        time_started = db.Column(db.String(64))
        time_ended = db.Column(db.String(64))


    class users(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        time = db.Column(db.String(64))
        ip = db.Column(db.String(64))
        email = db.Column(db.String(64))


    @login_manager.user_loader
    def load_user(user_id):
        return data.query.get(user_id)


    db.create_all()


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
            print(captcha_response)
            site_key = "6Leig10aAAAAAOb62ZbsGklzVXmpWhHcMuwHhzRC"
            auto = request.cookies.get('auto')
            if auto == 'True':
                site_key = site_keya
            email = request.form.get('email')
            password = request.form.get('password')
            password2 = request.form.get('password2')
            su = rnd.choice(string.ascii_letters) + rnd.choice(string.ascii_letters) + str(rnd.randint(1000, 10000))
            status, msg, msg2, msg3 = "ok", '', '', ''
            if is_human(captcha_response) == False:
                status, msg = "false", 'Botyara!'
            elif not email:
                msg3 = "Pls fill all places"
                status = "false"
            peter = users.query.filter_by(email=email).first()
            if peter is not None:
                msg3 = "This email adress already exists!"
                status = "false"
            conn.commit()
            if status == "ok":
                msg = EmailMessage()
                msg.set_content(
                    "Congrats!Your activation link: " + 'https://limp.herokuapp.com/task5/verification/' + email + '/' + su)
                msg['Subject'] = 'Click to confirm your email'
                msg['From'] = 'no-reply@limp.herokuapp.com'
                msg['To'] = f'{email}'
                s = smtplib.SMTP(host='b.li2sites.ru', port=30025)
                s.send_message(msg)
                s.quit()
                new_user = users(email=email, code=su, status='not_veri')
                db.session.add(new_user)
                db.session.commit()
                return render_template('after_signup.html', url_veri=url_for('verification', email=email, code=s))
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
            site_key = site_keya
        else:
            secret_key = '6Leig10aAAAAAGc9BuyWuqaSE5nLNja1HYkBPwmY'
            site_key = '6Leig10aAAAAAOb62ZbsGklzVXmpWhHcMuwHhzRC'

        captcha_data = {'secret': site_key, 'response': captcha_response}
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captcha_data)
        response_text = json.loads(response.text)
        print(response_text)
        return response_text['success']


    @app.route("/task5/verification/<email>/<code>", methods=["GET", "POST"])
    def verification(email, code):
        if request.method == 'POST':
            password = request.form.get('password')
            password2 = request.form.get('password2')
            if password == password2:
                hash_pwd = generate_password_hash(password)
                new_user = users(email=email, password=hash_pwd, status='veri')
                db.session.add(new_user)
                db.session.commit()
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
            password = md5(request.form.get('password').encode()).hexdigest()
            status, msg, msg2, msg3 = "ok", "", "", ""
            session['user_email'] = email
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
        email = session.get('user_email')
        if request.method == 'POST':
            n = request.form['n']
            time = datetime.now()
            cur.execute(
                f"INSERT INTO worker (email, time, N, p, q, status, time_started, time_ended) VALUES ('{email}', '', {n}, 0, 0, 'Queued', '{time}', '')")
            conn.commit()
            return redirect(url_for('work'))
        else:
            cur.execute(
                f"SELECT time, n, p, q, status, time_started, time_ended FROM worker WHERE email = '{email}' ORDER BY time_started desc")
            conn.commit()
            ans = cur.fetchall()
        if ans != []:
            elapsed = ans[0][6]
            return render_template('worker.html', ans=ans, elapsed=elapsed)
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
        cur.execute(f"INSERT INTO users (time, ip,email) values ('{time}','{ip}','{email}')")
        conn.commit()
        cur.execute(f"SELECT time,ip from users where email='{email}' ORDER BY id desc ")
        array = cur.fetchall()
        return render_template('task5.html', array=array)


    if __name__ == '__main__':
        app.run(debug=True)
